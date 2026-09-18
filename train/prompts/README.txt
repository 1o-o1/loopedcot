Short-exemplar few-shot blocks used only at harvest time to produce the second candidate chain
(chain B). They never appear in a training prompt or at evaluation, so they cost no prompt tokens
in any reported number.

Provenance: copied byte-for-byte from work/spikes/s34_budget/prompts/ (identical to the pair in
work/spikes/s33_anytime/p0/). One question-and-answer pair per exemplar, four per file, each
answer three lines or fewer so chain B is short by construction.

train/harvest.py --prompt=short reads <run root>/prompts/prompts_short_<src>.txt when that file
exists and falls back to the copy here otherwise.
