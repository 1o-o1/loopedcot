"""Fix 1 (PP3b): chain storage (write_chains/chain_path) and --resume-from-chains's
prefill-and-continue bookkeeping (seed_from_chain, and the forced-decode positions/cap accounting
it feeds into).

`OuroAdapter.decode`'s forced-continuation branch needs a real Ouro checkpoint to exercise for
real, which this environment cannot load (no GPU, no cached weights). What IS exercised here, on
CPU with no checkpoint, is the production code itself:
  * write_chains / chain_path: the sidecar file, its schema, and its resume semantics
  * seed_from_chain: the resumed trace and the tail-window seed a forced state needs
  * OuroAdapter.decode's actual wait-injection loop, driven by a tiny SCRIPTED fake model that
    stands in for the checkpoint -- every position/offset/cap computation below is the real one.
NOT exercised: the real Ouro weights/tokenizer, the KV-cache implementation
(UniversalTransformerCache), and generate.py's own gen_pass()/--resume-from-chains wiring (a nested
closure inside prod.generate.main, not unit-testable without a full CLI + model + tasks-data setup).

  python -m pytest tests/test_chains.py -q
  python tests/test_chains.py
"""
import json
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch                                                          # noqa: E402

from prod.common import load_ckpt, read_jsonl                         # noqa: E402
from prod.generate import chain_path, seed_from_chain, write_chains   # noqa: E402
from prod.models.ouro import (OuroAdapter, TAIL_WINDOW, make_stopper, # noqa: E402
                              new_forced_states)


# ------------------------------------------------------------------ chain_path / write_chains
def test_chain_path_has_no_tag_no_shard():
    p = chain_path("/out", "ouro_1_4b_base", "gsm8k", 4)
    assert p == os.path.join("/out", "chains_ouro_1_4b_base_gsm8k_k4.jsonl")
    p2 = chain_path("/out", "ouro_1_4b_base+lora_arm", "gsm8k", 4)
    assert "+" not in p2                       # same replace("+", "-") rule as every other file


def test_write_chains_schema_and_resume_skip():
    tmp = tempfile.mkdtemp()
    try:
        rws = [{"idx": 100}, {"idx": 101}]
        enc = [[1, 2, 3], [4, 5]]
        # `done` is required: write_chains never stores a truncated (unfinished) trace as a chain
        cur = {0: {"ids": [10, 11, 12, 13], "done": True}, 1: {"ids": [20, 21], "done": True}}
        st = {0: (3, "hash_line"), 1: (None, None)}     # 1: no marker found -> whole trace
        n, path = write_chains(tmp, "toy_model", "toy_task", 4, rws, enc, cur, st, bw=16)
        assert n == 2 and os.path.exists(path)
        rows = {r["idx"]: r for r in read_jsonl(path)}
        assert rows[100]["chain_ids"] == [10, 11, 12]         # cut at natural_stop = 3
        assert rows[100]["natural_stop"] == 3
        assert rows[100]["n_prompt_tokens"] == 3
        assert rows[100]["batch_width"] == 16
        assert rows[101]["chain_ids"] == [20, 21]             # no marker -> the whole trace
        assert rows[101]["natural_stop"] is None
        import hashlib
        assert rows[100]["prompt_sha256"] == hashlib.sha256(
            json.dumps(enc[0]).encode("utf-8")).hexdigest()

        # a second call (simulating a resumed job) must not duplicate or overwrite idx 100/101, and
        # must append a genuinely new problem -- the same resume semantics as the cells file.
        rws2 = [{"idx": 100}, {"idx": 102}]
        cur2 = {0: {"ids": [999], "done": True}, 1: {"ids": [30, 31, 32], "done": True}}   # idx100 ignored (present)
        st2 = {0: (1, "x"), 1: (3, "y")}
        n2, _ = write_chains(tmp, "toy_model", "toy_task", 4, rws2, enc, cur2, st2, bw=16)
        assert n2 == 1
        rows_after = {r["idx"]: r for r in read_jsonl(path)}
        assert len(rows_after) == 3
        assert rows_after[100]["chain_ids"] == [10, 11, 12]      # untouched by the second call
        assert rows_after[102]["chain_ids"] == [30, 31, 32]
        have = load_ckpt(path, lambda r: int(r["idx"]))
        assert set(have) == {100, 101, 102}
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ------------------------------------------------------------------ seed_from_chain
def test_seed_from_chain_ids_and_tail_window():
    pieces = ["p%d" % i for i in range(100)]
    chain_row = {"chain_ids": list(range(50))}
    ids, tail_seed = seed_from_chain(chain_row, pieces, TAIL_WINDOW)
    assert ids == list(range(50))
    assert len(tail_seed) == min(TAIL_WINDOW, 50)
    assert tail_seed == [pieces[i] for i in range(50 - TAIL_WINDOW, 50)]


def test_seed_from_chain_shorter_than_window():
    pieces = ["p%d" % i for i in range(10)]
    ids, tail_seed = seed_from_chain({"chain_ids": [1, 2, 3]}, pieces, TAIL_WINDOW)
    assert ids == [1, 2, 3]
    assert tail_seed == ["p1", "p2", "p3"]


# ------------------------------------------------------------------ tiny fake model: the real
# forced-decode injection loop, prefill-and-continue positions and cap accounting
class _Logits(object):
    def __init__(self, t):
        self.logits = t


class ScriptedModel(torch.nn.Module):
    """Stands in for the checkpoint: at absolute sequence position P, `forward` predicts
    `script.get(P, 0)` as the argmax next token, exactly the way a real model's logits would drive
    OuroAdapter.decode -- this lets the test dictate the "generation" deterministically without a
    real checkpoint, and so exercise decode()'s actual position/cap bookkeeping."""

    def __init__(self, script, vocab_size):
        super().__init__()
        self.script = script
        self.vocab_size = vocab_size
        self.dummy = torch.nn.Parameter(torch.zeros(1))          # for next(parameters()).device

    def forward(self, input_ids=None, attention_mask=None, position_ids=None,
               past_key_values=None, use_cache=None, cache_position=None, logits_to_keep=None):
        b, lq = input_ids.shape
        want = int(cache_position[-1].item()) + 1
        tok = self.script.get(want, 0)
        logits = torch.full((b, lq, self.vocab_size), -10.0)
        logits[:, -1, tok] = 10.0
        return _Logits(logits)


class _FakeTok(object):
    pad_token_id = 0


def _make_adapter(script, vocab_size, k):
    ad = OuroAdapter.__new__(OuroAdapter)          # skip __init__ (no repo lookup needed)
    ad.model = ScriptedModel(script, vocab_size)
    ad.tok = _FakeTok()
    ad._k = k
    ad._pieces = ["p%d" % i for i in range(vocab_size)]
    ad._cache_factory = lambda b, maxlen: None
    ad.chat_template = True                        # simplest stopper: x in eos_ids
    return ad


def test_resume_from_chain_prefill_then_wait_injection_positions_and_cap():
    """The scenario --resume-from-chains creates: a chain of 3 tokens is prefilled with the
    prompt, off = len(chain) = 3, and the model's very FIRST newly generated token (scripted to be
    the eos id) must trigger the stopper at absp = off exactly -- proving the resumed run rediscovers
    the natural stop at the correct position, not one token early or late."""
    enc = [1, 2, 3, 4, 5]                                    # prompt: 5 tokens
    chain_ids = [10, 11, 12]                                 # resumed chain: 3 tokens
    L = len(enc) + len(chain_ids)                            # 8: the prefill length
    EOS, WAIT0, WAIT1 = 999, 500, 501
    # position L -> the first generated token (scripted to hit the stop). L+1's own prediction (20)
    # is scripted deliberately -- it is discarded, never emitted, because the pending Wait token
    # still queued at that step wins (the real rule: whatever the model would say is ignored while
    # a wait injection is draining). L+2, L+3 are the first two predictions to actually reach `x`.
    script = {L: EOS, L + 1: 20, L + 2: 21, L + 3: 22}
    ad = _make_adapter(script, vocab_size=1000, k=4)

    pieces = ad._pieces
    tail_seed = seed_from_chain({"chain_ids": chain_ids}, pieces, TAIL_WINDOW)[1]
    st = new_forced_states(1)[0]
    st["off"] = len(chain_ids)                     # exactly generate.py's own seeding rule
    st["tail"].extend(tail_seed)

    stopper = make_stopper(chat_template=True, pieces=pieces, eos_ids=[EOS], task="gsm8k")
    n_new = 4
    gen, states, dt = ad.decode([enc + chain_ids], n_new, 4, [EOS], stopper=stopper,
                                wait_ids=[WAIT0, WAIT1], states=[st])

    assert gen[0] == [WAIT0, WAIT1, 21, 22]         # the wait pair, then 20 dropped, 21+22 land
    assert len(gen[0]) == n_new                              # cap accounting: exactly n_new emitted
    s = states[0]
    assert s["natural_stop_pos"] == len(chain_ids)           # = 3, the resumed boundary exactly
    assert s["natural_stop_reason"] == "tok_%d" % EOS
    assert s["n_forced_continuations"] == 1
    assert s["forced_positions"] == [[len(chain_ids), "tok_%d" % EOS, EOS]]
    assert s["off"] == len(chain_ids) + n_new                # off advances by exactly n_new
    resumed_trace = chain_ids + gen[0]
    assert len(resumed_trace) == len(chain_ids) + n_new == 7
    # cap accounting the readout jobs rely on: a cap below the natural stop cuts INSIDE the chain
    # (no injected content); a cap at/above it necessarily includes the Wait continuation.
    assert min(len(resumed_trace), 2) == 2 and resumed_trace[:2] == chain_ids[:2]
    assert min(len(resumed_trace), 5) == 5 and resumed_trace[3] == WAIT0


if __name__ == "__main__":
    fs = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for f in fs:
        f()
        print("ok", f.__name__)
    print("%d test functions" % len(fs))
