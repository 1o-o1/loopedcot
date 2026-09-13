# Provenance of every file in prod/tasks/data/

Written by `prod/tasks/freeze.py`. Nothing here is authored by the production package; each file is
copied from the spike that measured it, and `hashes.json` records the sha256 of each one.

| file | source | note |
|---|---|---|
| prompt_gsm8k.txt | s28_transfer_tasks/prompts/svamp.txt | the S9a 4-shot GSM8K prefix, written by s28_download.py from openai/gsm8k train rows 0-3 with s9a_common's own format string |
| prompt_svamp.txt | same file | S28 uses the GSM8K prefix for SVAMP by design |
| prompt_math500.txt | s13_box_grid/artifacts/math500_prompt.json ("prefix_text") | frozen because S13's math_shots() reads EleutherAI/hendrycks_math (config algebra), which is not cached on either machine and would silently fall back to a different source |
| prompt_aqua.txt, prompt_csqa.txt | s28_transfer_tasks/prompts/*.txt | Wei et al. 2022 CoT exemplars |
| prompt_arc.txt | s28_transfer_tasks/prompts/arc.txt | THREE AGENT-WRITTEN exemplars in the BBH style (not from a published prompt set); labelled as such wherever ARC numbers appear |
| prompt_bbh_*.txt | s26_bbh/prompts/*.txt | the official BIG-Bench-Hard cot prompt with the canary line and the "-----" separator dropped, which is what the BBH repo's own evaluation does |
| rows_bbh_*.jsonl | s26_bbh/artifacts/bbh_*.jsonl | 250 rows = the whole BBH task |
| rows_aqua.jsonl | s28_transfer_tasks/artifacts/data_aqua.jsonl | 254 rows = the whole test split |
| rows_svamp.jsonl, rows_csqa.jsonl, rows_arc.jsonl | s28 spike file (300 rows), replaced at `--extend` by the full split | built by `load_dataset(...).shuffle(seed=20260908)`, s28_download.py's own selection rule, with the spike file asserted to be a byte-identical prefix |
| rows_gsm8k.jsonl, rows_math500.jsonl | datasets, dataset order | written at `--extend` |

## PP3 additions

Four evaluation sets added in PP3: `rows_strategyqa.jsonl`, `rows_bbh.jsonl` (pooled over ten BBH
subtasks), `rows_mmlu.jsonl`, `rows_hellaswag.jsonl`. Full provenance, resolved dataset revisions and
the exact draw rules are in `sources.json`.

| prompt file | exemplars from | agent-written? |
|---|---|---|
| prompt_strategyqa.txt | three multi-hop yes/no exemplars invented for this package, not drawn from the StrategyQA data | yes |
| prompt_bbh_boolean_expressions.txt | BIG-Bench-Hard `cot-prompts/boolean_expressions.txt` | no |
| prompt_bbh_multistep_arithmetic_two.txt | BIG-Bench-Hard `cot-prompts/multistep_arithmetic_two.txt` | no |
| prompt_bbh_word_sorting.txt | BIG-Bench-Hard `cot-prompts/word_sorting.txt` | no |
| prompt_bbh_navigate.txt | BIG-Bench-Hard `cot-prompts/navigate.txt` | no |
| prompt_bbh_causal_judgement.txt | BIG-Bench-Hard `cot-prompts/causal_judgement.txt` | no |
| prompt_bbh_temporal_sequences.txt | BIG-Bench-Hard `cot-prompts/temporal_sequences.txt` | no |
| prompt_mmlu_stem.txt | three exemplars invented for this package | yes |
| prompt_mmlu_humanities.txt | three exemplars invented for this package | yes |
| prompt_mmlu_social_sciences.txt | three exemplars invented for this package | yes |
| prompt_mmlu_other.txt | three exemplars invented for this package | yes |
| prompt_hellaswag.txt | three exemplars invented for this package | yes |

The six new `prompt_bbh_*.txt` files are the official BIG-Bench-Hard CoT prompts fetched from
`https://raw.githubusercontent.com/suzgunmirac/BIG-Bench-Hard/main/cot-prompts/<task>.txt` with the
canary line and the `-----` separator dropped, the same transformation as the four already-frozen
`prompt_bbh_*.txt` files; the transformation was checked to reproduce all four of those files byte
for byte.

FLAN's 5-shot chain-of-thought MMLU exemplars could not be fetched and are not believed to exist in
the named sources: `google-research/FLAN` `flan/v2/cot_data/` holds only nine CoT source datasets
(aqua, creak, ecqa, esnli, gsm8k, qasc, qed, sensemaking, strategyqa) with no MMLU file,
`Muennighoff/flan` has no file matching `mmlu` or `cot`, and `SirNeural/flan_v2`'s `cot_*.jsonl.gz`
are those same nine datasets. MMLU is a held-out evaluation benchmark in FLAN. The four
`prompt_mmlu_*.txt` files are therefore AGENT-WRITTEN, as are `prompt_strategyqa.txt` and
`prompt_hellaswag.txt`; label them as such wherever StrategyQA, MMLU or HellaSwag numbers appear.

`rows_bbh.jsonl` holds 2437 rows, not 2500: BBH's `causal_judgement` task has only 187 examples
(the same count in `lukaemon/bbh` and in the official `bbh/causal_judgement.json`). The other nine
subtasks contribute 250 rows each. No row was invented or repeated to reach a round number.
