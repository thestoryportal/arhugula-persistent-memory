# D-C10r-seal — Codex design review of fence v13

Reviewer: Codex, reviewing the supplied design against the current implementation.
Model: GPT-6 family; the exact deployed model identifier is not exposed in this session.
Effort: adversarial source review and deterministic offline checks; the configured sampling effort is not exposed in this session.
Date: 2026-10-06 (America/Denver).
Target: `docs/C10R_LOOP_SEALING_V13.md`, DRAFT v1, and the Step A instructions in `results/c10r_seal_codex_brief.md`.

**Verdict: FIX-FIRST.** Decisions 1–2 do not establish the stated read boundary, and the proposed lexical rule fails the design's own negative controls. Step B was not entered. This review is the only deliverable required on the brief's blocking branch; no implementation or v13 probe report is claimed.

Scope: F1 condition C10, the Write Engine and post-write behavioral verification cells in `docs/SPEC_E2E_GROUND_TRUTH.md` §§B/F/G. This is an optimizer-isolation review, not an experiment verdict or an F1 closure. I read the design, both exposure/mirroring notes, the loop source and wrappers, the equivalence checker, the loop README/program, `docs/AUTORESEARCH.md`, and the earlier sandbox probe record. Existing probe results are historical evidence, not fresh v13 tests.

## Numbered findings

1. **BLOCKING — The 3-gram rule accepts all the recorded mirrors and the old dev prompt.**

   Locations: `docs/C10R_LOOP_SEALING_V13.md:12` and `:20`; `experiments/track_c/c10e_bandknob.py:52`; old sandbox `73f78ce:edit.py:36` and `:37`; `experiments/track_c/autoresearch_c10/prepare.py:69`.

   **EVIDENCE-SHOWS:** I read the actual `edit.py` objects for experiments 3–9 with `/usr/bin/git show`, parsed them with `ast`, and compared every string literal with the harness's three `PTEST` literals. After lowercasing, removing the subject slot, and tokenizing words, every file has **zero** overlapping held-out word 3-grams. The rule accepts the canonical write prompt, but also every prohibited prompt listed below:

   | Literal | Overlapping held-out 3-grams |
   |---|---|
   | `{}'s capital is the city of` | none |
   | `When you travel to {}, the capital is the city of` | none |
   | `The largest city and capital of {} is the city of` | none |
   | `{} is a country whose capital is the city of` | none |
   | old `DEV_PROMPT`: `{} has a capital called` | none |
   | canonical: `The capital of {} is the city of` | none |
   | lexical-only cleaned dev candidate: `{} names its capital` | none |

   The last candidate establishes lexical acceptance only; it is not an approved seed or a semantic-blindness claim. Checking all AST literals, rather than only the `PROMPTS` assignment, does not rescue the proposed rule. The precise per-commit output and a reproducible check are below.

   **Exact fix:** keep the 3-gram rule as a limited lexical check, and add a sealed, normalized deny-set containing the recorded prohibited prompt literals and old dev prompt. Freeze those negative fixtures before implementation, alongside the canonical positive fixture and the selected cleaned dev fixture. Require the same trusted checker to reject each negative fixture. Alternatively revise the rule with a demonstrated detector that meets those fixtures; do not declare the current rule sufficient or silently drop §2.1's requirement. Return a generic refusal and source location, without printing a held-out phrase or matched n-gram. Author-blindness cannot make an existing known mirror acquire a missing 3-gram.

2. **BLOCKING — Two allow-lists separate the agent's direct tools from wrappers, but the wrappers execute agent-authored code with access to the secrets.**

   Locations: `docs/C10R_LOOP_SEALING_V13.md:11`; `experiments/track_c/autoresearch_c10/sandbox_settings.py:169`, `:183`, and `:191`; `run.sh:21`; `edit.py:16`; `prepare.py:63`, `:85`, and `:222` (all loop-relative filenames in this item).

   **EVIDENCE-SHOWS:** `run.sh` starts the editable `edit.py` under the wrapper's Seatbelt profile. That profile's privileges also reach its scorer subprocess. `edit.py` imports `prepare`, and `prepare` imports the entire evaluation-bearing harness as `H` before running the recipe. Thus the editor can both open files allowed to the wrapper and inspect the already-imported module's globals. A separate scorer that never imports `edit.py` protects scoring from recipe monkey-patching; it does not hide evaluation text from the editor.

   I demonstrated the in-memory route using a **stdlib-only stub** of `prepare.H`. A recipe containing no current `_FORBIDDEN` substring and no held-out 3-gram recovered all three template strings by enumerating `vars(H)`. No real `prepare`, harness, engine, torch, or model was imported. This is a proof of the shared-namespace route, not a live Seatbelt or GPU test. Removing file-read permission after importing the harness would leave this route open.

   The policy formats can carry two different lists: the JSON `sandbox.filesystem.allowRead` / file-tool permissions and the separately generated Seatbelt allow rules are distinct outputs. However, `fence` itself is currently a broad read allowance (`sandbox_settings.py:62`, `:155`, `:200`). Removing a new sealed-file entry from the agent list is insufficient while that parent allowance survives. Give the agent an explicit deny for the entire sealed subtree and the reference extract, in **both** Bash and Read-tool policies, with exact-file patterns for files. Whitelist the readable wrapper/profile/settings files individually, or verify that narrower sealed-subtree denials override the parent in each layer. File-tool parent denies cannot be reopened by an allow.

   **Exact fix:** revise the execution boundary before implementation. The process executing arbitrary recipe code must receive neither the sealed-file read privileges nor an evaluator-bearing `H` module, including evaluation functions whose `__globals__` expose the templates. Only a trusted scorer/checker process may read the harness's evaluation stimuli and sealed data. Define a template-free editor runtime and the trusted handoff explicitly, while leaving the canonical harness and engine unchanged. Include that runtime/loading boundary in the later equivalence check. Add a no-model adversarial recipe probe that attempts both file reads and namespace introspection through the same wrapper dispatch used by a run. A direct agent `cat` denial alone does not verify decision 1.

3. **BLOCKING — Removing the sandbox harness copy leaves the current import path broken unless the loader changes.**

   Locations: `docs/C10R_LOOP_SEALING_V13.md:11`; `experiments/track_c/autoresearch_c10/launch.sh:62` and `:75`; `prepare.py:85`; `sandbox_settings.py:54` and `:173`; `results/autoresearch_c10_sandbox_probe.md`, “Fence v5” and “Fence v6”.

   **EVIDENCE-SHOWS:** the current loader inserts the program's `experiments/track_c` directory and performs a normal `import c10e_bandknob`. The Seatbelt allow-list opens the harness as an individual file, while its containing directory remains denied. The recorded v5 direct test found `importlib.util.find_spec` returned `None` for that denied path entry; the sandbox copy was the working fallback. The design removes that copy without specifying a replacement loader.

   **I-INFER:** keeping the current loader after that removal will fail to resolve the harness in the wrapper. This was not re-run against a v13 profile, because v13 is not implemented.

   **Exact fix:** in the trusted scorer/bootstrap established by item 2, verify the canonical file's hash and load it by its exact filename with an explicit importlib file spec. Preserve whatever module registration its imports require. Do not reopen `experiments/track_c` or its shared `__pycache__`. Give the editor only the approved runtime, not this loaded module. Test exact-file loading with a harmless dummy module under an equivalent directory-denied/file-allowed profile; leave real-model equivalence to the program session. Keep the real harness hash check on every trusted load, including resumes.

4. **ADVISORY — Decision 5a needs a concrete rule for each policy layer; its TMPDIR fallback does not establish that shell capture moves.**

   Locations: `docs/C10R_LOOP_SEALING_V13.md:15`; `experiments/track_c/autoresearch_c10/sandbox_settings.py:96`, `:110`, `:153`, `:161`, and `:176`; `results/autoresearch_c10_sandbox_probe.md`, “Probe 11 (first run)” and “Fence v4”.

   **EVIDENCE-SHOWS:** the generator reopens the whole `/private/tmp/claude-501` tree and enumerates existing foreign children as later denies. The current generated profile/settings still do this. Children created after generation are absent. The earlier probe recorded that denying the whole root broke Claude's shell-output capture (`cat: stdout: Operation not permitted`). The generator identifies capture folders by a slug of the sandbox or fence cwd. Python's `TMPDIR` is a separate variable.

   Seatbelt can express a subtree deny followed by narrower own-folder allowances; retain the metadata allowances needed to resolve `/tmp` and `/private/tmp`, and narrow **writes** as well as reads. The existing Bash policy also uses nested runtime reopenings. Read-tool rules have the different deny-always-wins behavior: a parent-tree deny plus an own-folder allow is not an exception for those tools. No supported, tested file-tool exclusion pattern for this particular “all children except own” rule was supplied or verified here.

   **Exact fix:** specify and test the actual read/write rules separately for Seatbelt, Bash and the file tools. If using the fallback, establish a supported way to relocate Claude's actual shell/task capture directory as well as Python temporary files; changing or exporting `TMPDIR` alone is not evidence that capture moved. A fence-owned temp *container* needs an explicitly writable child, since the fence itself is write-denied. Tests must create an unrelated child **after** settings generation, try both `/tmp` and `/private/tmp` spellings, and positively verify own capture, temp creation and cleanup. Treat that result as pending, rather than claiming either that the fallback works or that the CLI cannot support it.

5. **BLOCKING — A new session does not make the same adaptively used templates a fresh promotion holdout.**

   Locations: `docs/C10R_LOOP_SEALING_V13.md:14` and `:28`; `results/autoresearch_c10_heldout_mirroring_2026-10-06.md`, “Implications”; old sandbox `73f78ce:edit.py:30`, `:34`, and `:35`.

   **EVIDENCE-SHOWS:** the relaunch retains a recipe selected during experiments scored against these same three templates, and retains their historical scores. Removing prompt literals and starting a clean conversation removes direct textual exposure going forward. It does not remove the past adaptive selection encoded in the recipe. The mirroring note already requires a fresh sealed set for promotion.

   **Exact fix:** retain these three templates as sealed optimizer validation inputs, with the explicit scores-by-index exception in decision 6. Remove the §3 assertion that they become a fresh promotion set “again” after resealing. Promotion still requires a separate, pre-registered holdout never used to select this recipe or exposed to its authors. This changes the interpretation, not the canonical harness or current optimization metric. Keep the historical test-adjacency banner and the candidates-only rule.

6. **ADVISORY — Distinguish instrument equivalence from the cleaned candidate baseline, and bind the new trusted inputs into the launch gate.**

   Locations: `docs/C10R_LOOP_SEALING_V13.md:12`, `:14`, and `:23`; `experiments/track_c/autoresearch_c10/check_equivalence.py:15`, `:21`, `:32`, and `:70`; `launch.sh:26`, `:57`, and `:74`; `docs/AUTORESEARCH.md`, “Context isolation and permissions” and “The fence”.

   **EVIDENCE-SHOWS:** the checker compares the program-side `edit.py` with the harness's original baseline, requiring equal projectors and bitwise-equal edited tensors. `73f78ce` has `KL_FACTOR=0.125`, `PRESERVE_WEIGHT=4.0`, `GAIN=1.25`, and an `eigh` projector; removing its mirrored prompts does not make that recipe the original baseline. Replacing the reference `edit.py` with the cleaned optimizer seed would change what this comparison means and is expected to fail its unchanged recipe criterion. Conversely, leaving the reference alone while seeding the new repository separately needs a launcher change: `launch.sh:57` currently recopies the program-side `edit.py` whenever the sandbox branch is `autoresearch/master`.

   **Exact fix:** keep a fixed reference recipe for instrument equivalence and a separately identified cleaned optimizer seed. Verify the new loader/scorer against the fixed reference; score the cleaned seed separately as its new baseline. Prevent relaunch from overwriting that seed. Extend the manifest/gate beyond today's three hashes to cover the sealed stimuli, trusted checker/loader and seed provenance, keeping sealed contents outside agent-readable records. Archive the old equivalence record before the program session's rerun. Keep the existing PASS-and-current-source gate; defer the new equivalence and baseline scoring to that session.

   The first sealed-loop row must be compared against the cleaned seed's recorded baseline, not the old `7/72` envelope in `docs/AUTORESEARCH.md`. Also resolve the design's “two-stage” wording against the actual selected object: `73f78ce` contains a single layer-write loop with the preserve term and gain; it does not contain a second-stage write. Preserve the selected commit's actual non-prompt changes, rather than silently importing another discarded experiment.

7. **ADVISORY — Finish the launch, wrapper, diagnostic and seed details without widening access.**

   Locations: `experiments/track_c/autoresearch_c10/launch.sh:10`, `:23`, `:57`, and `:95`; `run.sh:8` and `:12`; `setup.sh:4` and `:7`; `kill_run.sh:8` and `:25`; `prepare.py:33`, `:76`, and `:252`; `program.md:15` and `:17`; loop `README.md:15`, `:30`, and `:56`.

   **Exact fixes:**

   - Update every sandbox path together, including all three wrappers and their PID/cwd checks. If the fence path changes, update the reference-extract constant, excluded commands and program instructions together. Keep exact command/profile validation in `kill_run.sh` while accepting either the new sandbox cwd or the exact resolved engine cwd; do not broaden it to arbitrary Python jobs in the engine directory. Use fake PID/process fixtures for review, without signalling the busy science jobs.
   - The existing experiment-process regex omits `c10s_sharedz_*`, the jobs the brief identifies as currently using the GPU. Require the exclusive-GPU gate to recognize those jobs and the equivalence/location-control jobs before any later launch. Do not invoke `run.sh` or `setup.sh` for a no-GPU probe: their first executable check performs an MPS operation. Use a disposable harmless probe entrypoint under the intended profiles instead.
   - Make lexical validation a trusted pre-execution check. A rejection before executing `edit.py` can be definitive; a check inside `prepare` can be bypassed by top-level recipe code before its import. Keep refusal messages free of protected text. Moving `_FORBIDDEN` alone also leaves the locality literal `is described as` in the readable `prepare.py:252`; place protected evaluation materialization on the trusted scoring side if decision 2 intends to seal that stimulus too.
   - Seed only the reviewed, cleaned working files into a new independent git object database. Do not clone or import old objects/reflogs, logs, `runs`, `__pycache__` or graft caches. Preserve the old sandbox unchanged. `PYTHONDONTWRITEBYTECODE=1` prevents new Python bytecode writes; it does not remove existing bytecode or disable graft's own caches. Update the README's copied-harness description and direct-run instructions, and `program.md:17` so initialization preserves the sanitized historical TSV and banner. Existing 5-column TSV shape should remain consistent with the loop's logger.

## Offline evidence and reproduction

The commands used only file reads, `/usr/bin/git show`, AST parsing, string processing and a fabricated runtime namespace. The two inspected source digests were:

```text
canonical harness SHA-256:
1f6be5811d7e58f3ebda16867a4a174b1cf24d47f9a2514cf9c3f9d29f18e695
old sandbox 73f78ce:edit.py SHA-256:
c89d80c09f2e97490ed30cda22e2a001d551e74a7df5d62585c741fc3b06abcf
```

Recorded negative-control results:

```text
exp 3 afcb2cb: rejected 0/2 noncanonical PROMPTS; DEV_PROMPT=None
exp 4 a26863d: rejected 0/2 noncanonical PROMPTS; DEV_PROMPT=None
exp 5 1206a7c: rejected 0/2 noncanonical PROMPTS; DEV_PROMPT=None
exp 6 9940c0a: rejected 0/2 noncanonical PROMPTS; DEV_PROMPT=None
exp 7 ae66823: rejected 0/2 noncanonical PROMPTS; DEV_PROMPT=None
exp 8 e475185: rejected 0/4 noncanonical PROMPTS; old DEV_PROMPT accepted
exp 9 73f78ce: rejected 0/2 noncanonical PROMPTS; old DEV_PROMPT accepted
all_string_literal_hits=[] for every one of the seven commits
existing identifier/blocklist hits for the namespace demo: []
proposed string-literal 3gram hits for the namespace demo: []
runtime stub recovered all three heldout strings: True
```

Reproduce from this worktree with the following standard-library-only command. It deliberately parses the harness as text and never imports any project module:

```bash
/opt/homebrew/bin/rtk proxy .venv/bin/python -B - <<'PY'
import ast, pathlib, re, subprocess, sys, types

root = pathlib.Path.cwd()
loop = root / 'experiments/track_c/autoresearch_c10'
old = '/Volumes/memit/llm-database-poc-mirror/autoresearch_sandbox_c10'

def constant(tree, name):
    return next(ast.literal_eval(node.value) for node in tree.body
                if isinstance(node, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == name
                        for t in node.targets))

harness = ast.parse((root / 'experiments/track_c/c10e_bandknob.py').read_text())
templates, canon = constant(harness, 'PTEST'), constant(harness, 'CANON')
assert len(templates) == 3

def grams(text):
    words = re.findall(r'[a-z0-9]+',
                       re.sub(r'\{[^{}]*\}', ' ', text.casefold()))
    return {tuple(words[i:i+3]) for i in range(len(words)-2)}

sealed = set().union(*(grams(text) for text in templates))
commits = [(3, 'afcb2cb'), (4, 'a26863d'), (5, '1206a7c'),
           (6, '9940c0a'), (7, 'ae66823'), (8, 'e475185'), (9, '73f78ce')]
for exp, commit in commits:
    proc = subprocess.run(['/usr/bin/git', '-C', old, 'show',
                           f'{commit}:edit.py'], capture_output=True,
                          text=True, check=True)
    assert proc.stdout.strip(), commit
    tree = ast.parse(proc.stdout)
    hits = [node.lineno for node in ast.walk(tree)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)
            and grams(node.value) & sealed]
    print(f'exp {exp} {commit}: all_string_literal_hits={hits}')
    assert hits == []
for label, text in [('canonical', canon),
                    ('old DEV_PROMPT', '{} has a capital called'),
                    ('lexical-only clean dev candidate', '{} names its capital')]:
    print(f'{label}: overlapping_3grams={sorted(grams(text) & sealed)}')

forbidden = constant(ast.parse((loop / 'prepare.py').read_text()), '_FORBIDDEN')
recipe = '''def apply_edit(facts):
    import sys
    runtime = sys.modules["pre" + "pare"]
    data = vars(getattr(runtime, chr(72)))
    return [value for value in data.values()
            if isinstance(value, list) and len(value) == 3
            and all(isinstance(text, str) and "{}" in text for text in value)]
'''
raw_hits = [word for word in forbidden if word in recipe]
literal_hits = [node.lineno for node in ast.walk(ast.parse(recipe))
                if isinstance(node, ast.Constant) and isinstance(node.value, str)
                and grams(node.value) & sealed]
assert 'prepare' not in sys.modules
stub = types.ModuleType('prepare')
stub.H = types.SimpleNamespace(PTEST=templates, CANON=canon)
sys.modules['prepare'] = stub
scope = {}
exec(compile(recipe, '<stdlib-runtime-exposure-demo>', 'exec'), scope)
recovered = scope['apply_edit']([])
del sys.modules['prepare']
print('existing identifier/blocklist hits:', raw_hits)
print('proposed string-literal 3gram hits:', literal_hits)
print('runtime stub recovered all three heldout strings:', recovered == [templates])
assert not raw_hits and not literal_hits and recovered == [templates]
assert 'torch' not in sys.modules and 'c10e_bandknob' not in sys.modules
print('STDLIB_ONLY: no project imports, no torch, no model load, no GPU work')
PY
```

## Disposition

The design is not ready for Step B. Items 1, 2, 3 and 5 require corrections to the design before implementing it. Items 4, 6 and 7 specify the unresolved implementation and verification details, with the policy-expression limits distinguished from proven failures.

No target-model load, GPU/MPS operation, equivalence run, baseline score, loop launch, advisor/model call, or disposable Claude session was run. The protected science files, engine and harness were not modified; no old sandbox was deleted or rewritten; no commit was made. No v13 profile or sealed sandbox was built. Consequently this review does not claim the direct Seatbelt test, probe-agent test, equivalence PASS, cleaned baseline, or advisor pass required before a future launch. The brief explicitly ends this branch after Step A.
