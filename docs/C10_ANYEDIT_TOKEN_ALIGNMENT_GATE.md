# C10 AnyEdit Token Alignment Gate

**Date:** 2026-06-26  
**Status:** PASSED for current A7 stimuli; mandatory prereg/harness gate.  
**Reviewer context:** external advisor-review returned `FIX-FIRST` until this gate was specified and checked.

## Question

Upstream AnyEdit tokenizes `answer` standalone while later computing keys over `question + answer`. If those tokenizations disagree at the continuation suffix, an AnyEdit pilot could produce a false rescue or false failure.

## Check

Tokenizer-only, no GPU/model edit:

- tokenizer: `Qwen/Qwen2.5-3B` at revision `3aab1f1954e9cc14eb9509a215f9e5ca08227a9b`
- prompt template: `The capital of {} is the city of`
- arm: current C10 A7 coined-coined values, N=24
- tested answer formatting:
  - bare answer, e.g. `Vindex Vask`
  - leading-space answer, e.g. ` Vindex Vask`

For each subject/value, compare:

1. `tok(answer, add_special_tokens=False)`
2. suffix of `tok(question + answer, add_special_tokens=False)` with the same length

## Result

| answer formatting | suffix alignment | token length range | `window_size=1` windows | `window_size=2` windows | `window_size=3` windows | `window_size=50` windows |
|---|---:|---:|---:|---:|---:|---:|
| bare | 24/24 | 4-7 | 4-7 | 2-4 | 2-3 | 1 |
| leading-space | 24/24 | 4-6 | 4-6 | 2-3 | 2 | 1 |

The alignment concern does not block the C10 AnyEdit prereg if the harness enforces this check. The intended harness format should be **leading-space answer** because it preserves natural continuation text after `city of`; bare answer can align but produces malformed text such as `city ofVindex...`.

## Binding Gate For The Pilot

Before any edit run, the harness must emit and validate, for every request:

- answer token IDs;
- `question + answer` suffix token IDs;
- exact decoded answer/suffix text;
- window boundaries for every planned `window_size`;
- `lookup_idxs` derived from those windows.

Abort if any answer IDs differ from the continuation suffix, if decoded text is malformed, or if a claimed per-token/window condition creates only one window for A7.

