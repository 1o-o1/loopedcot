"""`prod.generate` end to end on CPU with a STUB checkpoint: a natural-stop job that writes a chains
sidecar, then a `--continue-chains` job over it, in both modes.

This is the wiring `tests/test_continue_chains.py` cannot reach (selection, seeding, the
continued cut rule, the copy of the old grid, the new header, resume) driven through `main()`. The
stand-in is a character-level tokenizer and an adapter whose `decode` follows a per-row SCRIPT, so
every position, cut, cap and read-out below is computed by the production code.

  python -m pytest tests/test_continue_chains_e2e.py -q
  python tests/test_continue_chains_e2e.py
"""
import hashlib
import json
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prod import generate as G                                          # noqa: E402
from prod.common import read_header                                     # noqa: E402

TAG_ID, EOS_ID = 1000, 1001
THINK = "</think>"
TASK = "gsm8k"                 # its stop strings are ["\n\nQuestion:", "Final Answer:"]
STOPS = ["\n\nQuestion:", "Final Answer:"]
# the two scripts, in the order the stub emits them after the generation prompt
PLAN_STOPS = "Work it out. #### 7" + THINK + " So the answer is 7.\n\nQuestion: next"
PLAN_RUNS = "keep reasoning. " * 40            # no stop string, no tag: runs to the horizon
ANSWER = " 7<|eos|>"
HOR1, CAPS1 = 64, [0, 8, 16, 64]


def _piece(i):
    return THINK if i == TAG_ID else ("<|eos|>" if i == EOS_ID else chr(i))


def _encode(text):
    out = []
    for j, part in enumerate(str(text).split(THINK)):
        if j:
            out.append(TAG_ID)
        for ch in part:
            out.append(TAG_ID if False else ord(ch))
    return out


class CharTok(object):
    eos_token_id = EOS_ID
    pad_token_id = 0

    def __call__(self, text, add_special_tokens=False):
        return {"input_ids": _encode(text)}

    def decode(self, ids, clean_up_tokenization_spaces=True, skip_special_tokens=False):
        return "".join(_piece(int(i)) for i in ids)

    def convert_tokens_to_ids(self, t):
        return TAG_ID if t == THINK else None

    def apply_chat_template(self, msgs, tokenize=False, add_generation_prompt=True,
                            enable_thinking=True):
        return "<u>" + msgs[0]["content"] + "</u><a>"


TOK = CharTok()


class FakeAd(object):
    """An Ouro-shaped adapter whose decode follows the script of the row it is given."""
    family = "ouro"
    chat_template = True
    add_special_tokens = False
    max_positions = None
    batch_cap = 8
    tok = TOK

    def load(self):
        pass

    def set_depth(self, k):
        self._k = int(k)
        return {"k": int(k)}

    def meta(self):
        return {"name": "ouro_1_4b_think", "chat_template": True}

    def passes_per_token(self, k):
        return 2 * int(k)

    def kv_bytes_per_token(self, k):
        return 1024

    def batch_for(self, k, seq):
        return self.batch_cap, 0.0

    def stop_ids(self):
        return []

    def wait_ids(self):
        return _encode("Wait,")

    @staticmethod
    def _plan(prompt_text):
        """Which script this row follows: half the problems stop at the think tag, half run on."""
        q = prompt_text.split("<a>")[0]
        h = int(hashlib.sha256(q.encode("utf-8")).hexdigest(), 16)
        return PLAN_STOPS if h % 2 == 0 else PLAN_RUNS

    def decode(self, seqs, n_new, k, eos_ids, stop_strings=None, row_ids=None, **kw):
        eset = {int(x) for x in (eos_ids or ())}
        gen = []
        for s in seqs:
            text = TOK.decode(s)
            if text.endswith("Final Answer:"):
                script = _encode(ANSWER)
            else:
                # what the row has already generated is everything after the generation prompt
                sofar = text.split("<a>")[-1]
                plan = self._plan(text)
                script = _encode(plan[len(sofar):]) if plan.startswith(sofar) else _encode(plan)
            out, tail = [], ""
            for x in script:
                if len(out) >= int(n_new):
                    break
                out.append(int(x))
                if int(x) in eset:
                    break
                tail = (tail + _piece(int(x)))[-64:]
                if stop_strings and any(ss in tail for ss in stop_strings):
                    break
            gen.append(out)
        return gen, 0.01


def _run(tmp, *extra):
    argv = ["--model=ouro_1_4b_think", "--task=%s" % TASK, "--k=1", "--out=%s" % tmp,
            "--caps=%s" % ",".join(str(c) for c in CAPS1), "--no-extra-caps",
            "--horizon=%d" % HOR1, "--n=6", "--batch-width=4"] + list(extra)
    return G.main(argv)


def _rows(path):
    return [json.loads(x) for x in open(path, encoding="utf-8") if x.strip()
            and not x.startswith('{"_header"')]


def _setup(tmp):
    """The natural-stop grid and its chains sidecar, produced by prod.generate itself."""
    old_get = G.get
    G.get = lambda *a, **kw: FakeAd()
    try:
        meta = _run(tmp)
    finally:
        G.get = old_get
    return meta


def test_natural_then_continue_think_tag_then_horizon():
    tmp = tempfile.mkdtemp()
    old_get = G.get
    try:
        m0 = _setup(tmp)
        old_p = os.path.join(tmp, "cells_ouro_1_4b_think_%s_natural_k1.jsonl" % TASK)
        chain_p = os.path.join(tmp, "chains_ouro_1_4b_think_%s_k1.jsonl" % TASK)
        assert m0["complete"] and os.path.exists(old_p) and os.path.exists(chain_p)
        old_rows = _rows(old_p)
        assert len(old_rows) == 6 * len(CAPS1)
        old_bytes = open(old_p, "rb").read()
        chain_bytes = open(chain_p, "rb").read()
        # the natural grid: some rows cut AT the think tag, the rest ran to the horizon
        by = {}
        for r in old_rows:
            by.setdefault(r["row_idx"], r)
        tagged = [r for r in by.values() if r["stop_marker"] == THINK]
        ran = [r for r in by.values() if r["stop_marker"] is None]
        assert tagged and ran and len(tagged) + len(ran) == 6
        assert all(r["natural_stop"] == HOR1 for r in ran)
        # the three new fields are on every row of an ORDINARY job too
        assert all("chain_tail" in r and "own_answer_span" in r for r in old_rows)
        assert {r["stop_reason"] for r in old_rows} == {"think_tag", "horizon"}
        t = [r for r in old_rows if r["stop_reason"] == "think_tag" and r["B"] == 64][0]
        assert t["chain_tail"].endswith("#### 7")           # the cut text, up to the tag
        assert t["own_answer_span"] and t["trace_answer"] == "7"
        assert t["own_answer_span"][1] - t["own_answer_span"][0] == 1      # the "7" itself

        # ---------------------------------------------------------- think_tag continuation
        G.get = lambda *a, **kw: FakeAd()
        m1 = _run(tmp, "--continue-chains=think_tag")
        new_p = os.path.join(tmp, "cells_ouro_1_4b_think_%s_natural2_k1.jsonl" % TASK)
        assert m1["complete"] and os.path.exists(new_p)
        assert open(old_p, "rb").read() == old_bytes        # the source grid is untouched
        assert open(chain_p, "rb").read() == chain_bytes    # so is the chains sidecar
        hdr = read_header(new_p)
        assert hdr["continue_chains"] == "think_tag"
        assert hdr["continue_chains_path"] == chain_p
        assert hdr["continue_old_horizon"] == HOR1
        assert hdr["continue_n_continued"] == len(tagged)
        assert os.path.basename(hdr["continue_source_cells"]) == os.path.basename(old_p)
        new_rows = _rows(new_p)
        assert len(new_rows) == 6 * len(CAPS1)              # the whole grid, copied or regenerated
        tag_idx = {r["row_idx"] for r in tagged}
        cont_rows = [r for r in new_rows if r.get("continued")]
        assert cont_rows and {r["row_idx"] for r in cont_rows} <= tag_idx
        for r in cont_rows:
            old_stop = by[r["row_idx"]]["natural_stop"]
            assert r["B"] > old_stop                        # only the caps above the old stop
            assert r["n_cut"] > old_stop                    # the cut grew past the tag
            assert r["stop_reason"] == "stop_string:\n\nQuestion:"
            assert THINK in r["chain_tail"]                 # the tag is INSIDE the chain now
            assert r["continue_boundary"] == old_stop + 1   # the tag was put back
        # a cap at or below the old stop is the OLD row, verbatim but for the provenance fields
        low = [r for r in new_rows if r["row_idx"] in tag_idx and not r.get("continued")]
        assert low
        for r in low:
            o = [x for x in old_rows if x["row_idx"] == r["row_idx"] and x["B"] == r["B"]][0]
            assert r["B"] <= by[r["row_idx"]]["natural_stop"]
            assert r["copied_from"] == os.path.basename(old_p)
            assert r["continued_problem"] is True
            assert (r["pred"], r["correct_v2"], r["n_cut"], r["answer_text"]) == \
                (o["pred"], o["correct_v2"], o["n_cut"], o["answer_text"])
        # a row this mode did not select is copied at EVERY cap
        notsel = [r for r in new_rows if r["row_idx"] not in tag_idx]
        assert len(notsel) == len(ran) * len(CAPS1)
        assert all(r["continued_problem"] is False and r["chain_tail"] is None for r in notsel)
        assert all("stop_reason" in r for r in new_rows)
        # every row of the file says which grid it belongs to, copied or not
        assert {r["protocol"] for r in new_rows} == {"natural2"}
        assert {r["protocol_base"] for r in new_rows} == {"natural"}
        assert {r.get("copied_protocol") for r in new_rows} == {None, "natural"}

        # resume: a second run of the same job writes nothing and stays complete
        n_before = len(new_rows)
        m1b = _run(tmp, "--continue-chains=think_tag")
        assert m1b["complete"] and len(_rows(new_p)) == n_before

        # ---------------------------------------------------------- horizon continuation
        m2 = G.main(["--model=ouro_1_4b_think", "--task=%s" % TASK, "--k=1", "--out=%s" % tmp,
                     "--caps=0,8,16,64,128", "--no-extra-caps", "--horizon=128", "--n=6",
                     "--batch-width=4", "--continue-chains=horizon",
                     "--protocol-tag=natural3"])
        h_p = os.path.join(tmp, "cells_ouro_1_4b_think_%s_natural3_k1.jsonl" % TASK)
        assert m2["complete"] and os.path.exists(h_p)
        assert open(old_p, "rb").read() == old_bytes
        hrows = _rows(h_p)
        assert len(hrows) == 6 * 5
        hh = read_header(h_p)
        assert hh["continue_chains"] == "horizon" and hh["continue_n_continued"] == len(ran)
        hcont = [r for r in hrows if r.get("continued")]
        ran_idx = {r["row_idx"] for r in ran}
        assert {r["row_idx"] for r in hcont} == ran_idx     # exactly the rows that ran on
        for r in hcont:
            assert r["B"] == 128 and r["n_cut"] == 128 and r["n_trace"] == 128
            assert r["stop_reason"] == "horizon"
            assert r["continue_boundary"] == HOR1           # no tag is inserted in this mode
        # the think-tag rows are copied whole, and a continued row's caps <= 64 are the old rows
        assert all(not r.get("continued") for r in hrows if r["row_idx"] in tag_idx)
        # B=128 does not exist in the source grid: on a row that was not continued the cut is the
        # same natural stop at 64 and at 128, so that read-out is SHARED, not regenerated
        shared = [r for r in hrows if r["row_idx"] in tag_idx and r["B"] == 128]
        assert len(shared) == len(tagged)
        for r in shared:
            assert r["shared_cut_from_B"] == 64 and r["n_cut"] == by[r["row_idx"]]["natural_stop"]
        for r in [x for x in hrows if x["row_idx"] in ran_idx and x["B"] <= HOR1]:
            o = [x for x in old_rows if x["row_idx"] == r["row_idx"] and x["B"] == r["B"]][0]
            assert (r["pred"], r["n_cut"], r["answer_text"]) == (o["pred"], o["n_cut"],
                                                                 o["answer_text"])
        # the sidecar is never rewritten by a continuation job
        assert open(chain_p, "rb").read() == chain_bytes
        assert json.load(open(os.path.join(
            tmp, "meta_ouro_1_4b_think_%s_natural3_k1.json" % TASK),
            encoding="utf-8"))["chains_written"] == 0
    finally:
        G.get = old_get
        shutil.rmtree(tmp, ignore_errors=True)


def test_continuation_refuses_to_overwrite_or_to_run_on_the_forced_protocol():
    tmp = tempfile.mkdtemp()
    old_get = G.get
    try:
        G.get = lambda *a, **kw: FakeAd()
        for bad in (["--continue-chains=horizon", "--protocol-tag=natural"],
                    ["--continue-chains=horizon", "--protocol=forced"],
                    ["--continue-chains=think_tag"],           # no chains sidecar in an empty dir
                    ["--continue-chains=think_tag", "--tag-loops"]):
            try:
                _run(tmp, *bad)
            except SystemExit:
                continue
            raise AssertionError("expected SystemExit for %s" % bad)
        # horizon mode at the OLD horizon would continue nothing: it is refused rather than run
        d = tempfile.mkdtemp()
        try:
            _setup(d)
            G.get = lambda *a, **kw: FakeAd()
            try:
                _run(d, "--continue-chains=horizon", "--protocol-tag=natural2h")
            except SystemExit:
                pass
            else:
                raise AssertionError("horizon mode at the old horizon must be refused")
        finally:
            shutil.rmtree(d, ignore_errors=True)
    finally:
        G.get = old_get
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    fs = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for f in fs:
        f()
        print("ok", f.__name__)
    print("%d test functions" % len(fs))
