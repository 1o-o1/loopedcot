Short-exemplar few-shot blocks used only when the chains are generated, to produce the
second candidate chain
(chain B). They never appear in a training prompt or at evaluation, so they cost no prompt tokens
in any reported number.

Provenance: copied byte-for-byte from s34_budget/prompts/ (identical to the pair in
s33_anytime/p0/). One question-and-answer pair per exemplar, four per file, each
answer three lines or fewer so chain B is short by construction.

train/chains.py --prompt=short reads <run root>/prompts/prompts_short_<src>.txt when that file
exists and falls back to the copy here otherwise.

aqua.txt, csqa.txt, svamp.txt and arc.txt are the STANDARD exemplar blocks of the shared evaluation
harness, read by s28_common.task_prompt(). They are the prompts the grid and gate V1 use, and they
are pinned per task by sha256 in the target manifest. Copied byte-for-byte from
s28_transfer_tasks/prompts/.
