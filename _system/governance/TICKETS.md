# TICKETS — the atomic-ticket workflow, from an approved plan to merged master
Job: how one approved plan becomes many atomic tickets that fresh builders implement in parallel lanes and that ship, train and land without hand work; which tool owns each stage; the traps each stage has already sprung; the gaps still open.
Routed from the root CLAUDE.md (twin: AGENTS.md). Written 2026-10-16 from the sweep `L/w1opt/staged/tickets-doc/INVENTORY.md` (the audit, one row per component; this file is the guide for the moment of decision). Tags `[R12]` and `[G7]` point at that inventory's rule and gap numbers.

## The goal

Operator, 2026-10-16, verbatim: "The goal of all of this work is that Atomic tickets complete end to end in no more than 15 minutes."

- Measure every ticket from its `dispatch` row to its `merged` row and report the minutes against 15, in every estimate and every report. A ticket over 15 gets its cause written down (§ Ledger and metrics), because an overrun with no named cause comes back on the next ticket.
- Merges land in one `train.sh` CI cycle for all ready PRs. Never estimate, plan or run merges one after another: ten PRs that reach `ready` together land in one candidate, one CI run, one gate call (train.sh:2-5). The sentence *"T319 lands, then T320, then..."* prices the train at ten times its real cost, and the plan built on it is wrong before it starts.

## The belt

Picture the workflow as one conveyor belt: plan → cut → lane → brief → build → ship → train → land → release. Each station is a script, and each script leaves marks that the next station reads: a ledger row, a `verdict.sha` written before the review, a ready marker, a lock dir, a recorded merge-base, an allow file with a reason in it.

A step done by hand takes the ticket off the belt. A `git commit` in a lane, a `gh pr merge`, a `cp` over a live tool, a verdict file edited after the fact: each one skips the station that writes the marks. The next station then either refuses, which is the cheap outcome, or trusts a mark that no longer describes the ticket, which is the expensive one: a GO reused for code nobody reviewed, a cleanup that never ran, a merge on master with no name on it. None of these raise an alarm. They surface days later as a mystery that the next session spends hours on.

So at every stage, ask first: *which station owns this, and am I about to do its job by hand?* The answer is almost always "a script owns it; run the script."

## Roots and names

Every path in this file is written from one of these roots. Paste the preamble before running a command from this file:

```sh
L=/Volumes/memit/corpus-consolidation-toolkit/workspace/runs/20261013-overnight/G-build/LEAN
M=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory
S=/Users/robertrhu/.claude/skills/atomic-ticketizer
```

- `L` = the LEAN folder: workflow tools (`L/tools`), ticket folders, staged MAESTRO steps.
- `M` = the main checkout on master (MAESTRO's working copy and cwd).
- `S` = the atomic-ticketizer skill. `/Users/robertrhu/.codex/skills/atomic-ticketizer` is a symlink to it, so Claude (`/atomic-ticketizer`) and Codex (`$atomic-ticketizer`) read one copy (S/SKILL.md:100). The skill reads S/agents/openai.yaml for its Codex interface.
- `W` = `L/w1opt`, the folder of the tool steps 301-327 and of the staging area.
- TD = one ticket folder: PLAN.md, tickets/, reviews/, ledger.tsv, the briefs, METRICS.md. In a command, put the folder's absolute path where TD appears. Examples: `L/w1opt/followup-318` (current), `L/w1opt`, `L/part2` (Part 2 wave 1), `L/recut` (ICM v2.1 recut).
- `<T>` = a ticket id (T318) = its plan step number. Branch `tk/<T>`, lane `/Volumes/memit/llmdb-lanes/tk-<T>`.
- MEM = /Users/robertrhu/.claude/projects/-Volumes-memit-llm-database-poc-mirror-arhugula-persistent-memory/memory. HO = /Volumes/memit/corpus-consolidation-toolkit/workspace/runs/20261013T114331Z-2ec28dcb/icm-v2 (handoffs HANDOFF-STEP50 through STEP59).

The tools stay where they are. `L/tools` and the skill are outside every repo and not version-controlled, by operator decision (2026-10-16, stopping a move into the repo: "Is any of this necessary?"). Durable means, in the operator's words, "the workflow that we are running with those skills/tools are clearly known through the ICM repo structure for agents to leverage when relevant": CLAUDE.md routing → this file → the absolute paths above. Recovery is the `.bak-*` backups and install_staged.sh. Do not propose moving L/tools or the skill into the repo [G1].

## Who does what

- Operator: approves a plan (the `Approved:` line), starts or pauses waves, grants allow rules. Wave 2 (T204 T205 T217 T271 T209 T218 T210 T213 T215) stays paused until the operator says start [R52].
- MAESTRO: writes plans and briefs, cuts, makes lanes, dispatches, verifies builder work itself, ships, rules on every NO-GO, alone writes allow files, runs the train, stages and installs MAESTRO steps. Only MAESTRO merges, and only through the gate.
- Builder or fixer: one fresh agent per ticket or fix round. Works only in its lane, writes only the ticket's `write` list, never commits, pushes or merges.
- Pre-review: `L/tools/prereview.sh`, model gpt-6.1-sol at medium effort, the same packet as Astra plus the fault_kit attacks.
- Astra: `L/tools/astra.sh`, model gpt-6-astra at high effort, one binding round, only on `astra: true` tickets.

## Stage 1 — Plan (TD/PLAN.md)

The plan shape is in S/SKILL.md §1. What the skill does not say, and what has cost re-cuts:

- The first line is `Approved: <short pointer>`, written only after the operator approves, and never by you on your own reading of "sounds good". A draft carries no `Approved:` line at all: the cut's regex (S/scripts/tickets.py:19) accepts any text after it, so a placeholder like `Approved: pending` passes as an approval. Keep the line a short pointer and put the operator's quotes in an "Approval record" section of the plan, because the approval text is copied into every ticket and counts toward the 2048-byte cap; dry-run a cut in scratch to check the cap [R11].
- One step = `## Step N: <observable result>`, with `write:` (at most 4 files), `test:`, `out:`, optional `deps:`, `reads:`, `astra:`. The heading becomes the commit message and the PR title (tickets.py:250, :254), so write it as a result anyone can check, not as a task name [R12].
- `out:` holds the step's requirements as numbered sentences, `(1) ... (2) ...`, as Steps 318-324 in `L/w1opt/followup-318/PLAN.md` do. Numbers let the reviewer, the prober and MAESTRO's ruling name a requirement by number. S/SKILL.md §1 says the same since Step 326 (installed 2026-10-17); its template line is `out: (1) <one checkable requirement> (2) <the next one>`.
- Number new steps after the last used id, across all TDs: ids become branch names, and the close finds a dependency by its `T0NN:` commit subject, so a reused number collides with history [R10].
- Width rule: at most 2 steps may write any one file, counted over every ticket in the TD, merged ones included (tickets.py:14, :184). When a third writer is needed, move a not-yet-built ticket's write into a new leaf file; do not raise the cap, because the cap is what lets lanes run in parallel without merge conflicts. Two steps that write one file also get an automatic dependency in plan order (tickets.py:76-79), so they never run in parallel: the second waits for the first to merge, which adds a wave and a full ticket's minutes to the estimate. Follow-ups that need a hub file whose two writers already merged go in a TD of their own, which the cap counts separately (STEP41 ruling, `L/recut/followup/`; plan 318 likewise lives in `L/w1opt/followup-318`) [R14].
- `test:` strings: anchor unittest output as `grep -qE "Ran [1-9][0-9]* tests? in [0-9.]+s +OK *$"`. Unanchored, `discover` of a missing file prints "Ran 0 tests ... OK" and a skipped method prints "OK (skipped=1)", and both pass as GREEN [R17].
- `astra: yes` only for gate, validator or destructive code, and such a step writes its own new test file (the cut refuses otherwise).
- MAESTRO steps (changes to L/tools or the skill) go in the same plan under `## MAESTRO step N:`. That heading does not match the cut's `## Step N:` pattern (tickets.py:20), so the cut never turns them into tickets; they follow § MAESTRO steps. But a field line (`write:` `test:` `out:` `deps:` `astra:` `reads:`, also as a `- ` or `* ` bullet, tickets.py:21) under a MAESTRO heading still attaches to the `## Step` before it (tickets.py:46-54): it fails the cut as "given twice" or silently adds the field to that ticket. Write MAESTRO step sections with no line that starts with a field name; use numbered items, as Steps 325-327 do.

## Stage 2 — Cut (`tickets.py cut ... --base`)

```sh
git -C /Volumes/memit/llmdb-lanes/base checkout -q --detach origin/master   # refresh the base first
python3 -B $S/scripts/tickets.py cut TD/PLAN.md TD/tickets --base /Volumes/memit/llmdb-lanes/base
```

- `--base` is required and must be the clean detached checkout `/Volumes/memit/llmdb-lanes/base`, never M: M is always dirty, and the cut refuses a base with uncommitted changes. The base is refreshed by hand only; a stale base judges "the test fails on the base" against an old master, so refresh it before every cut [R8] [G18].
- The cut runs every step's test on the base (600 s each) and refuses one that already passes. When it refuses, the test is not testing the change: name a new test class, or give a follow-up its own test file [R9]. Its other refusals (more than 4 files, a third writer, two parallel tickets on one file, a cycle, a trivial test, an oversized ticket, an astra step without its own new test file) are listed in S/SKILL.md §2.
- The output dir must be empty. Keep a superseded cut beside it as `tickets.cutN-superseded` rather than deleting it.
- On a new plan, show the operator the cut output (a few tickets) before GO [R13].
- After a hand edit of a ticket file, run `python3 -B $S/scripts/tickets.py check TD/tickets --base /Volumes/memit/llmdb-lanes/base`.
- `tickets.py ready TD/tickets --merged T316,T317 --running T318` lists the tickets whose deps have merged. Both lists are comma-separated (tickets.py:286-287), and an unknown `--merged` id fails (tickets.py:214-215). Pass every dispatched, unmerged ticket in `--running` so nothing is dispatched twice.
- The cut writes `TD/tickets` with one `TD/tickets/<T>.json` per step (keys id goal plan approval write deps test out astra rules, plus reads).

## Stage 3 — Lanes (`mklane.sh`)

```sh
zsh $L/tools/mklane.sh T319 TD
```

- One lane per ticket: a worktree of M at `/Volumes/memit/llmdb-lanes/tk-<T>` on branch `tk/<T>`, from freshly fetched origin/master, as a non-cone sparse checkout (mklane.sh:9: `/*`, minus `/experiments/` except `/experiments/*/CONTEXT.md`, minus `/knowledge/` except `/knowledge/**/*.md`, minus `/_archive/`), widened by the 16 files in `L/tools/t012-widen.txt` that tests read, with `/code/memit/vendor/notebooks/` excluded (mklane.sh:11). It logs `dispatch` to TD/ledger.tsv. About 43-50 MB instead of 6.5 GB, which is what lets ten lanes fit on the disk [R15].
- Use mklane.sh, not `git worktree add` by hand (which S/SKILL.md:64 still shows [G10]): a `/code`-only lane is too narrow for tests that read `knowledge/specs/*.md`, and guard_mutants refuses the vendor notebook symlinks, so a hand lane fails at ship, not at dispatch [R15].
- No `uv run` in a lane. It makes an 824 MB `.venv` inside the lane, and the pre-commit hook's first interpreter is the lane's `.venv` (pre-commit:15), so a venv without yaml and markdown_it blocks the close commit. If one appears, probe `<lane>/.venv/bin/python -c 'import yaml, markdown_it'` before close; `git worktree remove` clears it [R16]. The one interpreter for builders, gates, hygiene and the sampler is `M/.venv/bin/python -B`.
- The pre-commit hook is live in M and in every lane (`git config core.hooksPath = code/ops/git/hooks`, file `M/code/ops/git/hooks/pre-commit`): it blocks stale generated state, stale fingerprints, a staged closure that is not PASS, secrets, and a non-default index. So a ticket that changes the hook is a production change, and commits are plain `git commit` with no paths, `-a` or `-i` (tickets.py:245-250 does this) [R19]. The closure check fails on an untracked file inside a staged folder; never chain a heredoc after `git commit &&`, because when the hook blocks, the heredoc never runs and a later step reads a missing file [R20].

## Stage 4 — Briefs

The live builder template is `L/w1opt/brief-template.md` (paths, context, RED/GREEN, the guard_mutants revert step at line 22, the 45% handoff rule, the forbidden list, a 60-line reply). `L/tools/template-brief-builder.md` is a stale copy: a concrete T020 brief with no guard_mutants step. Use it only for the wave-1 review rules it quotes (fdsafe, Refusal, git config rulings) [G8]. `L/w1opt/mkbrief.py` fills the template for T301-T305 only (mkbrief.py:6); later briefs are written by hand in its shape as `TD/brief-<T>.md` (example: `L/w1opt/followup-318/brief-T318.md`). The template is written for W: for any other TD, change the ticket and plan paths (`L/w1opt/tickets/`, `L/w1opt/PLAN.md` lines 11-18, brief-template.md:5-6), the approval quote ("Approve", 2026-10-16, :12) and the "Your step is a tool step ... fixtures" context (:13). A builder reads all of it as true of its own ticket.

You will be about to dispatch, the last brief will be open, and you will think *"copy T318's brief, change the ticket id."* Diff it against `L/w1opt/brief-template.md` first. A copied brief carries the last ticket's lessons and misses the template's newer ones, and the builder cannot know which (HO/HANDOFF-STEP59.md:42).

Every brief:
- names only the files the builder may read; builders do not grep LEAN or /Volumes/memit recursively, because a wide search costs their context and finds stale copies (L/tools/ticketizer is one) [R44];
- carries the 45% handoff rule and caps the reply at 30-60 lines; builders cannot see their context gauge, and long replies cost MAESTRO ~10k each across ten lanes [R44];
- gives test commands with `PYTHONPATH=code`, after MAESTRO has run each named suite once on master with a positive control, because without `PYTHONPATH` a suite fails on import before and after the change and the comparison passes while 17 tests break [R18];
- names an API only after MAESTRO has probed it on the interpreter (`os.waitid` is absent on this macOS Python 3.11) [R47];
- for the guard_mutants gate: the gate runs the ticket test in a lane copy with no `.git`, so a test must not read the lane's git history; put a git-based oracle in a `__main__` mode MAESTRO runs at ship. Never export GIT_DIR into the gate: a test that writes git would write the real lane (MEM/lean-ticket-lane-traps.md:46);
- tells the builder to use its own TMPDIR, because all lanes share the host temp folder and one lane's cleanup or lsof trail lands on another's;
- for a split ticket: its tests must not constrain the tickets after it (T318's tests compared all operator modules and would have failed 320-324); check the API against the following tickets before dispatch (HO/HANDOFF-STEP59.md:43).

Historical briefs kept for shape only, run by nothing: `L/tools/brief-item5.md` (tickets.py item 5, built in the copy L/tools/ticketizer), `L/tools/brief-item6.md` (created ship.sh and test_ship.sh), `L/tools/brief-part2-draft.md` (Part 2 plan draft); `L/tools/mkfixbriefs.py` wrote the Part 2 wave-1 fix briefs into `L/part2` (brief-<T>-fix<n>.md, lane text `/Volumes/memit/llmdb-lanes/tk-@T@`, `/Volumes/memit/llmdb-lanes/tk-T203`) and reads `L/part2/extra-fd-binding.md`.

## Stage 5 — Build (builder, then MAESTRO verifies)

The builder follows S/references/worker.md: write list only; RED (the test fails for the reason the step names, else `blocked`); GREEN; one fix, then `halted`; no commit.

- Revert check on every ticket, astra or not: guard_mutants with `--base "$(git merge-base HEAD origin/master)"` and a new `--out` per run (the tool never overwrites one). Each survivor gets a killing test or a reason in the reply; MAESTRO alone allow-lists. The ship gate runs the same command and stops on any survivor (worker.md:10-11) [R27]. `M/code/ops/review/guard_mutants.py`: one mutant per guard (raise-remove, flag-drop, regex-zero, except-class, except-remove, negate-if, write-loop) in fd-safe scratch copies; exit 0 all killed or allowed, 1 a survivor, 2 a refusal.
- Builder revert runs that use `subprocess.run(shell=True, timeout=...)` orphan grandchildren that later block hygiene; use exec, or a timeout that ends the whole run [R34].
- Builders use `M/code/tests/fault_kit.py` attacks and, for filesystem tools, `M/code/ops/migrate/fdsafe.py` helpers (wave-1 rulings).

The builder says GREEN. You will think *"done, ship it."* That is the moment to verify instead, because the builder's GREEN was on its own TMPDIR and its own reading of the step:
- run the ticket test yourself on the lane, on the host TMPDIR (`/var/folders/...`), not only TMPDIR=/private/tmp, and expect Linux CI to run it once more [R36];
- read `git -C <lane> status --porcelain` against the write list;
- read the kill table, and check the gate's mutant count per file: master's gate made 0 mutants in `mutant_ops/base.py`, so "0 survived" there proved nothing (HO/HANDOFF-STEP59.md:44);
- log a `verified` row (§ Ledger and metrics).

## Stage 6 — Fix rounds (after `blocked`, `halted`, or a NO-GO)

Review gets one round (S/SKILL.md:88-95, S/references/reviewer.md:12-18). MAESTRO rules on each NO-GO in `TD/reviews/<T>/RULING.md`: it accepts or rejects each finding and names the kill set by mutant id (M01...). Survivors outside the kill set are out of scope. A tests-only fix is verified by MAESTRO itself (the reviewer's reproduction and each mutant in the kill set); a second Astra round is only for a fix to a hook that gates every commit, or a fix that rewrites a check [R38]. A pre-review NO-GO also returns to a ruling and a fixer before Astra ever runs (ship.sh:73-74).

- The fix brief is `TD/brief-<T>-fix<n>.md`, in the shape of `L/tools/template-brief-fix.md` (ruling sections, kill set, frozen assertions; T020-specific text, adapt it). A fresh fixer per round.
- A ticket whose new mutant changes an existing suite's exact expectations (T319 vs test_guard_mutants_lines.py, T323 vs test_guard_mutants.py) needs a MAESTRO ruling that widens its write list and bounds the edits (`L/w1opt/followup-318/reviews/wave-b/RULING.md`); without it check 1b stops the ship with 5. CI runs none of these suites [G4], so MAESTRO runs all of them on a scratch merge of the ready lanes before the train.
- Rank reviewer NOTEs by "can it lose data", not only "can it give a wrong PASS": a candidate-delete NOTE filed as non-blocking was later reproduced as a lost candidate [R39].
- Several findings of one class in a pre-review NO-GO: rule the class and order a mechanical sweep of the whole file, with the sweep oracle positive-controlled on a known-bad head, instead of one fix per finding and another round per fix [R40].
- A Claude review in place of Astra is a one-off for one named ticket, never a rule and never carried into a handoff as "same for the next step" [R41].
- Never edit a review file after anything pinned it (a verdict, a ruling, a packet): a consumer that hashed it stops on the drift, or worse, trusts a changed record. Add a new note file instead [R43]. Earlier rounds are renamed, not rewritten (`astra-round5.md`, `prereview-round2.md`).
- A lane cut before a dependency merged lacks it. Before a fix brief names a newly merged helper, check `git -C <lane> merge-base --is-ancestor <dep> HEAD`; if not, merge origin/master into the lane first [R21].
- A fixer that reports done while its background work still runs: stop it, then pin the lane hashes before you verify, or you verify a lane that is still changing [R46].
- After a tests-only fix, Astra's frozen mutant trees under `TD/reviews/<T>/work` still hold the old test: tell the next round to rebuild them [R35].
- The fix is committed by re-shipping. You will look at the fixed lane and think *"two files, I'll `git add` and `git commit` it myself."* The classifier denies it, and if it did not, the commit would skip the allowlist check and the ledger. `ship.sh` runs `tickets.py close`, which commits, pushes, and then fails harmlessly at `gh pr create` because the PR exists; ship.sh accepts that when the open PR's branch holds the new head [R7].
- Re-ship arguments: copy SPECREF and SEAM from `TD/reviews/<T>/packet.md` ("Spec and background" / "Seam"), or from `TD/ship-args-<T>.txt`; never rewrite them from memory. A wrong seam points Astra at the wrong boundary [R5].

## Stage 7 — Ship (`ship.sh`)

```sh
zsh $L/tools/ship.sh TD T318 "$SPECREF" "$SEAM" "<NOTE>" > TD/ship-T318.log 2>&1; echo "ship rc=$?"
```

Run it with the shell's cwd = M, the Bash tool's background mode, and output to a log. Each of those has bitten:
- cwd = M, because gh resolves the repository from the working directory, and astra.sh's `gh pr diff` and `gh pr checks` inherit it (ship.sh:7, astra.sh:18) [R3].
- Background mode, never `&` or `disown`: a disowned ship sends no completion notice, and you are left polling. If it happens, watch TD/ledger.tsv for `done` or `stop` [R1].
- Never pipe a ship into `tail`: tail's exit 0 reported three stopped ships as "completed 0". Redirect to a log, echo the rc, read the ledger [R4].
- Do not write a `pgrep -f ship.sh` waiter: it matches its own shell. ship.sh holds its own locks; launch it directly [R25].
- Start a close with ship.sh. After a hand `tickets.py close`, ship.sh's re-ship path handles only an unchanged lane (commit fails, clean status, HEAD equals the remote, ship.sh:369-382) [R6].

What one ship does, in order (each step appends a TD/ledger.tsv row; the first failure stops it):
1. `start`: reads `TD/tickets/<T>.json` and `TD/PLAN.md` (refuses without them), `astra` true/false, the Step number.
2. Merge-base: once, when the write list has a product `.py` or a test file (`git merge-base HEAD origin/master`); no base, stop 2.
3. Gate 1a, guard mutants (Step 310): guard_mutants on each write-list `.py` not named `test_*`, with the ticket test, cwd = the lane, `--base` = that merge-base (T317: only changed lines are mutated). An earlier `TD/reviews/<T>/mutants.json` is kept as `mutants.json.N`. Survivors not listed in `TD/reviews/<T>/mutant-allow.json` (`[{"id": ..., "reason": ...}]`) stop the ship with 4.
4. Check 1b, existing test files (Step 325, installed 2026-10-16): each write-list test file (`^test_|_case`, tickets.py TEST_FILE) that exists at the base is diffed against it, uncommitted edits included. A deleted or changed line, a binary diff, or a deleted file gives a `tests` row with rc 5, and the ship stops with 5. A file new since the base is not checked; add-only passes with a `tests 0` row. MAESTRO alone may allow an edit in `TD/reviews/<T>/test-edit-allow.json` (`{"path": "reason"}`) [R28].
5. The ticket test once more, only to time it; then `close` (S/scripts/tickets.py close: branch check, deps in base, allowlist, GREEN test, commit, push, PR). The close row carries the PR URL and the timing.
6. The prober (Step 326, installed 2026-10-17 in record mode): on every ticket (Astra or not, a reused GO too), right after close, ship.sh starts `$PROBER` in its own process group with Astra's six arguments (ship.sh:394-415). It takes one Astra slot under the same admission (an `admit` row "for the probe"). The prober is astra.sh with `REVIEW_OUT=probe` and `REVIEW_PROMPT=S/references/prober.md` on PROBE_MODEL/PROBE_EFFORT (ship.sh:19). It numbers the `out:` requirements, disables each one in a scratch copy, runs the ticket test, and writes `TD/reviews/<T>/probe.md` (first line `VERDICT: GO` or `VERDICT: NO-GO`, survivors as `R(n) | requirement | edit | result`), with `TD/reviews/<T>/probe.out` (its output) and `TD/reviews/<T>/probe.end` (its exit time). Pre-review and Astra run beside it; it is reaped before the ready marker, or by a stop, which logs its row first (ship.sh:47-49). The `probe` row ends `| N.N min` (launch to the prober's exit; the admission wait is in the `wait` rows).
   - `PROBE=record` (the default): the row only. rc = the prober's exit, or 3 when it exits 0 with no `VERDICT: GO|NO-GO` first line written by this run; a NO-GO row has rc 0 and the verdict in the detail, as prereview and astra rows do. A prober that cannot run (no Step number, admission failed, no reviews dir) gives `probe 2 "...; prober not run"` and the ship goes on (ship.sh:166).
   - `PROBE=gate`: judged like Astra: a non-zero exit stops with it, anything but GO stops with 3, a prober that cannot run stops 2, and a ticket with no Step number is refused before close (ship.sh:239). Any other PROBE value, also `PROBE=''`, stops 2 before close (ship.sh:238).
   - `PROBER=''` runs no prober and never reads PROBE: the ship as it was before Step 326.
   - Before each reviewer starts, an earlier `TD/reviews/<T>/<OUT>.md` is renamed to `<OUT>.md.prev-<utc>[.N]`, never edited (aside(), ship.sh:81-94), so a verdict counts only when this run wrote it.
7. For `astra: true`: reuse a GO when `TD/reviews/<T>/verdict.md` is newer than `TD/reviews/<T>/verdict.sha` and that sha is the lane head (ship.sh:390-392). Else admission (below), one Astra slot, then `prereview` and `astra` rows; a verdict whose first line is not `VERDICT: GO`, or that this run did not write (an earlier file is moved aside before the reviewer starts, ship.sh:81-94), stops with 3.
8. `ready`: the marker `L/tools/ready/<T>` (keys T PR LANE HEAD TD READY_AT), written as `L/tools/ready/.<T>.<pid>` and moved, so the train never reads half a marker. The ship exits 0. With TRAIN=0 instead, it lands this PR alone (§ Land).

The stop at 4 or 5 is the gate working. You will see one survivor in an obviously equivalent spot, or a one-line test change that "only renames", and think *"allow it and move on, the ticket is at minute 14."* Write the allow entry only with the reason a reviewer would accept, in the file the ship reads; the reason is the record of why the gate was overruled. More often the right move is a killing test or a ruling. Allow files are MAESTRO's alone: a builder that writes one has graded its own exam.

An independent Astra review runs before `PROBE=gate` is turned on (Step 326 ruling 15, `L/w1opt/staged/326/review-claude-r3/RULING.md`). Step 326 was installed after a Claude review and a mechanical check, with no round-4 Astra review (an operator one-off). You will read four record-mode probe rows that caught real gaps and think *"the trial is done, set PROBE=gate."* A gate that stops every ticket on a reviewer no independent review has passed puts its own defects on every lane. Record the trial in METRICS.md, get the Astra review, then switch.

Exit codes: 0 ready (or done with TRAIN=0); 2 usage or infrastructure (bad args, a PROBE value other than record or gate, a sampler or git failure, no merge-base, a malformed allow file); 3 a review verdict is not GO; 4 guard survivors; 5 an existing test file lost or changed lines. A failing sub-tool's own rc passes through too: a reviewer that exited non-zero (ship.sh:109), guard_mutants exit 2 (ship.sh:303-305), a failed close (ship.sh:371-380), land and cleanup with TRAIN=0 (ship.sh:451-482).

Admission for Astra (Step 308): `M/code/agents/compute_sample.py --once` (the absolute `-B` path, because check_gpu's EXEMPT row for the sampler matches only that form) must show load1 < `ASTRA_LOAD_MAX` (10), mem free > 20%, swap not grown since `L/tools/compute.last`, research_blockers = 0, memit free >= 20 GiB. Use research_blockers, never check_gpu "ok": team pythons always block check_gpu (`M/code/lab/runners/c10w_p2_gate.py` lists them; EXEMPT rows need an absolute script token) [R33]. While admission or all `ASTRA_MAX` (6) slots `L/tools/astra.slot.<i>` are busy, the ship logs `wait` and sleeps 15 s; pre-review and Astra run inside one slot; ship.sh releases it right after the review (ship.sh:421), and the EXIT trap (ship.sh:219) is the fallback.

Reviews: astra.sh writes into `TD/reviews/<T>`: `TD/reviews/<T>/pr.diff`, `TD/reviews/<T>/checks.txt`, `TD/reviews/<T>/<OUT>.sha` (head, before the review), packet.md (or `<OUT>-packet.md`), then `codex exec -s workspace-write -C work` writes `TD/reviews/<T>/<OUT>.md` and `TD/reviews/<T>/<OUT>.log`, for OUT = verdict, prereview or probe. With `REVIEW_PROMPT` set (the prober), the prompt file's text replaces the packet, with `{{T}}` `{{PR}}` `{{STEP}}` `{{TD}}` `{{SPECREF}}` `{{SEAM}}` `{{DIFF}}` `{{CHECKS}}` `{{HEAD}}` `{{LANE}}` `{{W}}` `{{NOTE}}` filled in literally; a placeholder left over is exit 2 (astra.sh:5-6). Such a review has its own work dir and diff/checks files, named after OUT, so it can run beside another one. The reviewer's only writable root is `TD/reviews/<T>/work`, with TMPDIR `TD/reviews/<T>/work/tmp`; the lane stays read-only. The packet points at S/references/reviewer.md, `TD/PLAN.md` "## Step N", and SPECREF paths relative to `/Volumes/memit/corpus-consolidation-toolkit/workspace/runs/20261013-overnight/`. Astra's TD defaults to `L/recut` when TD is unset (ship.sh sets it). Codex pre-review can hit the OpenAI content filter; ship.sh then fails closed, because the earlier verdict was moved aside and the run wrote none [R42].

Locks: a killed ship can leave `L/tools/land.lock` or an `L/tools/astra.slot.<i>` dir. Check `ps` for a live ship, train or codex first, then rmdir it by hand (ship.sh:195-196) [R32]. One slot has leaked since 11:47 on 2026-10-16 [G2].

## Stage 8 — Train (`train.sh`)

```sh
zsh $L/tools/train.sh > <your scratch dir>/train.log 2>&1; echo "train rc=$?"   # cwd = M
```

Run it from cwd = M, Bash background mode. train.sh:21 says "Run it from anywhere"; that comment is wrong [G6]. Its gh calls (train.sh:163, :243, :279) resolve the repo from the cwd, and from L it stops at once with "gh pr view N failed: no git remotes found". The marker stays in `L/tools/ready/`, so a re-run from M is safe [R2].

What one train does, under `L/tools/land.lock`:
- Returns markers a dead train left in `L/tools/ready/claimed`, then claims every `L/tools/ready/T<->` into `L/tools/ready/claimed/` (`L/tools/ready/claimed/T<->`); a re-ship during the train writes a new `L/tools/ready/<T>` that waits for the next train.
- Checks each PR is OPEN at its marker HEAD; a PR that is not gets `stop` and its marker goes to `L/tools/ready/stopped/<T>` (folder `L/tools/ready/stopped`).
- Merges the heads `--no-ff` in READY_AT order onto origin/master in its own worktree `/Volumes/memit/llmdb-lanes/land-<id>` on branch `land/<utc>-<n>`, pushes it (ci.yml:5 runs CI on `land/**`), and runs `M/code/ops/git/git_merge_gate.py --batch --candidate land/<id> PRS --apply`, which waits for candidate CI (480 s) and prints a JSON report.
- PASS: for each PR, the cleanup ship.sh would have done (`land`, `merged`, `lane`, `branch` rows), but only when the lane is clean and its HEAD and branch tip are the marker HEAD inside origin/master; the marker moves to `L/tools/ready/landed`. Then the candidate worktree and branch go, hygiene runs once, and each PR gets `done`.
- Candidate CI failure, confirmed by a failed run: the batch splits in halves down to one PR, which gets `stop` with the run link. A merge conflict: that PR gets `wait` and stays ready. Any other refusal halts the train with nothing cleaned.
- After the gate merges, the train fetches and fast-forwards M (`git -C M merge --ff-only origin/master`, train.sh:158) before any cleanup; a failed fast-forward halts it with nothing cleaned (train.sh:160). The usual cause is a dirty tracked file in M that the merge touches. The PRs are merged by then: commit or move the dirty file, fast-forward M by hand, then clean up each lane and branch the way the train would (below).
- No markers: exit 0 at once (train.sh:265). A malformed marker, a symlinked one, or one still in claimed/ halts the train with 2 before it acts (train.sh:85-100, :268-271).
- A TRANSIENT gate report (the two hygiene refusals, nothing merged) is retried up to 6 times, 20 s apart (train.sh:230-237). MERGED_TRANSIENT (merged, then a transient refusal) goes on to cleanup (train.sh:138, :241).
- A merged PR whose lane fails `owned` (dirty lane, detached HEAD, a branch tip that moved) gets `stop`; its lane and branch are kept and its marker goes to stopped/ (train.sh:168-169). A claimed marker that was never used, whose slot was re-shipped meanwhile, also goes to stopped/ (train.sh:43-48).
- Recovering a marker from `L/tools/ready/stopped/<T>`: fix the cause, then re-ship the ticket; ship.sh writes a fresh marker (an unchanged lane re-ships). Do not move the old marker back by hand: its HEAD and READY_AT describe the earlier attempt. For hand cleanup of a merged PR's lane and branch, the single-command allow rules are `git worktree remove /Volumes/memit/llmdb-lanes/<lane>`, `git branch -D tk/<T>` and `git push origin --delete tk/<T>` (settings.json:31, :33, :35), one command per call, never chained [R23].
- Last line: `train done: landed N, waiting N (conflict), stopped N`.

One train lands every ready PR in one CI cycle; that is how a batch of tickets meets the 15-minute goal together. You will have one PR ready and two still in Astra and think *"land this one now."* Usually wait for the others: a second train costs a second CI cycle. Land alone only when the others are far behind.

## Stage 9 — Land (the gate, and the TRAIN=0 path)

The merge gate is the only merge path, and MAESTRO is the only caller: train.sh calls it in batch mode; with `TRAIN=0`, ship.sh calls `L/land.sh PR LANE`, which waits up to 20 minutes for CI on the lane head, runs the single-PR gate, and on the gate's two stale-base wordings merges origin/master into the lane, pushes and retries once. ship.sh then fast-forwards M the same way (ship.sh:458-462) and stops on a failure, with the PR already merged; recover as for the train. The full merge rule and the cooperative rule the gate relies on are in `_system/governance/MERGING.md`.

You will see green checks on a PR and think *"CI is green, `gh pr merge` is one command."* That is the moment. The gate's lock binds only the writers that take it; a hand merge races every one of them, skips the cleanup marks the next train reads, and the damage lands on master with no name on it.

- Land one PR per land.sh call; a loop of land.sh calls was denied, and so was a combined `worktree remove && branch -D && push --delete` (Git Destructive) [R23].
- The gate refuses while extra branches exist, so hygiene runs first; after `gh pr update-branch` the local branch is behind and the gate reports MERGED_WITH_FAILURE [R51].
- land.sh's CI wait hides gh errors and reports "none" after 20 minutes [G14].

## Stage 10 — Release (cleanup, hygiene, builders)

- Lanes and branches are removed by train.sh (`worktree remove` without --force, then `update-ref -d` against the marker HEAD) or by ship.sh with TRAIN=0. Do not remove a lane by hand while its marker is claimed or its PR is open. (close_unit.py, named in older memory, belongs to the 14 Oct package era and is not part of this flow; `tickets.py close` plus the train replace it.)
- `M/code/ops/git/git_hygiene.py --apply` keeps worktrees and deletes only eligible merged branches. It refuses on incomplete lsof evidence ("lsof cwd unreadable or unavailable") while any process sits in a vanishing temp dir or in a lane or reviews dir, and the gate refuses when "hygiene protection evidence changed before merge" (a parallel close moved a branch). ship.sh and train.sh retry both refusals 6 times, 20 s apart (ship.sh:64, train.sh:133, :195). ship.sh never retries a PR that is already merged: it logs `land` "merged; land.sh refused after the merge" and goes on with rc 0 to cleanup (ship.sh:65-68). A hung orphan test (ppid 1, far past its suite's runtime) is a permanent cause: kill it. Run your own probes from your scratch dir, not under reviews/ or a lane [R22].
- One builder per ticket. Release it after its unit: TaskStop a subagent builder; clear a Codex builder with `/quit` and relaunch, never `/new`, which joins the old conversation [R45].

## Stage 11 — MAESTRO steps (changing the workflow tools)

A MAESTRO step changes `L/tools`, `L/land.sh` or the skill. It is built against stub suites in a staged copy, never edited live. install_staged.sh covers only files whose live twin is in `L/tools` (step 5); `L/land.sh`, the skill and any new file go by hand (step 5b).

1. Stage in `L/w1opt/staged/<STEP>/` (the staging area `L/w1opt/staged/`; steps 307-313, 325, 326 are there): `<b>.new` copies (`L/w1opt/staged/<STEP>/<b>.new`), NOTES.md, the stager's brief.
2. Stub suites: `L/tools/test_ship.sh` (124 `check` call sites, 134 checks when run after Step 325) runs a copy `L/tools/ship.sh<SUF>` against recording stubs in a mktemp tree; `L/tools/test_train.sh` (56 checks) does the same for `L/tools/train.sh<SUF>`. A staged suite runs against the staged `.new`. Positive control: the new cases fail against the live script.
3. Real-scale dry run: run each new or changed gate on a real lane and a real-size file before install. Fixture-green gates refused real lanes on vendor symlinks, and a whole-file mutation stopped every edit [R29].
4. A change to the land path (train.sh, land.sh, the gate) gets a fresh decorrelated reviewer before install (Step 307 rule) [R31].
5. Install with `L/tools/install_staged.sh STEP`:
   ```sh
   zsh /Volumes/memit/corpus-consolidation-toolkit/workspace/runs/20261013-overnight/G-build/LEAN/tools/install_staged.sh 326
   ```
   Type it in exactly this absolute form: the allow rule (settings.json:40) matches that literal command, and the file is mode 644, so it runs only through `zsh`. For each `L/w1opt/staged/<STEP>/*.new` with a live twin `L/tools/<b>`, it backs up to `L/tools/<b>.bak-<DAY>-<STEP>`, copies to `L/tools/.<b>.install-<pid>` with the live mode, moves it atomically, and compares. It refuses while `L/tools/land.lock` is held or a ship, train or land runs, because a ship starting mid-install could read half a pair; its pgrep (:15) also matches a running test_ship.sh or test_train.sh, so let a suite finish first. Install ship.sh and test_ship.sh as a pair [R30]. Edit and Write on install_staged.sh and reclaim.py are denied (settings.json:46-49).
   - A `skip <b>.new: no live ...` line means that file was NOT installed: its twin is not in L/tools (install_staged.sh:18-21). Step 326's `SKILL.md.new` and `prober.md.new` print it. Install those by 5b.
   - Its other refusals exit 2 with nothing changed: a STEP name outside `[0-9a-z-]+` (:11), no staged folder (:13), no `.new` with a live twin (:22), and an existing `L/tools/<b>.bak-<DAY>-<STEP>` (:23). So a second install of a revised step on the same day refuses: rename the earlier backup (for example to `.bak-<DAY>-<STEP>a`) after checking it holds the pre-step file, then install again.
   - The per-file loop (:24-30) is not transactional: if the second file fails, the first is already live. Restore the pair together from their backups (`mv` each `.bak-<DAY>-<STEP>` back over its live file), never one alone.

5b. Files install_staged.sh does not cover: `L/land.sh` (it lives in L, not L/tools), the skill's files in S, and any new file (a `.new` with no live twin, such as `S/references/prober.md` that staged ship.sh.new:18 points at). Do by hand what the script does: `cp -p` the live file to `<file>.bak-<DAY>-<STEP>`, copy the `.new` to a temp name in the same folder, `chmod` it to the live mode, `mv` it over the live file, `cmp` against the `.new`. Step 326 left `S/SKILL.md.bak-20261017-326` (the pre-326 SKILL.md) and the new `S/references/prober.md`. A new file has no backup; `mv` it into place only after checking nothing by that name exists. S is editable by the Edit tool under settings.json:38 (`Edit(//Users/robertrhu/.claude/skills/atomic-ticketizer/**)`); if a shell `mv` there prompts, hand the operator the `!` allow-rule command. Install a new reference before the script that names it, so no ship reads a missing file. trace.py counts every file in S, backups included (it skips `*.bak-*` only under L/tools), so a new file or backup in S fails `trace.py --doc` until this file names it: that failure is the close-out rule doing its job.

You will have the `.new` ready, the suite green, and think *"`cp` it over, it's one file."* `cp` writes into the live file's inode, and zsh reads a script as it runs, so a ship already running continues from its old offset into the new bytes; a ship starting mid-copy reads half a script; and there is no backup to diff against when something breaks at land. An atomic `mv` leaves running ships on the old inode. install_staged.sh is the station; use it.

6. Log an `install` row in the plan's TD/ledger.tsv (the step number in the ticket column), with the suite numbers, the positive control and the doc status, then close it under § Close-out rule.

Backups are the only history [G1]. Restoring one alone can break the flow, because several pairs changed together [G13]: restore a ship.sh backup with its test_ship.sh backup.

## Environment overrides

Defaults are the live values; set one only for a test or a deliberate one-off, and say so in the ledger row.

| script | variable | default |
|---|---|---|
| ship.sh | TRAIN | 1 (ready marker); 0 lands alone; any other value exits 2 (:33, :36) |
| ship.sh | TICKETS, ASTRA, PREREVIEW, LAND | `python3 -B $S/scripts/tickets.py`, `$L/tools/astra.sh`, `$L/tools/prereview.sh`, `$L/land.sh` (:13-15, :24) |
| ship.sh | SAMPLER, COMPUTE_LAST | `M/.venv/bin/python -B M/code/agents/compute_sample.py`, `$L/tools/compute.last` (:22-23) |
| ship.sh | GH, GIT, HYGIENE, GUARD | gh, git, `M/.venv/bin/python -B` git_hygiene.py, the same for guard_mutants.py (:25-28) |
| ship.sh | TESTRUN, LANES | the built-in testrun, `/Volumes/memit/llmdb-lanes` (:31-32) |
| ship.sh | ASTRA_MAX, ASTRA_LOAD_MAX, ADMIT_SLEEP | 6, 10, 15 s (:150, :129, :159) |
| ship.sh | LOCK_SLEEP, TRANSIENT_SLEEP | 10 s, 20 s (:446, :70) |
| ship.sh | PROBE | record; `gate` stops on the prober's verdict; any other value stops 2 (:20, :238) |
| ship.sh | PROBER | `env REVIEW_OUT=probe REVIEW_MODEL=$PROBE_MODEL REVIEW_EFFORT=$PROBE_EFFORT REVIEW_PROMPT=S/references/prober.md $ASTRA`; set but empty runs no prober (:19) |
| ship.sh | PROBE_MODEL, PROBE_EFFORT | gpt-6.1-sol, medium (:19) |
| train.sh | TRAIN_M, GATE (also GH, GIT, HYGIENE, LANES, LOCK_SLEEP, TRANSIENT_SLEEP) | M, `M/.venv/bin/python -B M/code/ops/git/git_merge_gate.py` (:24-29) |
| astra.sh | REVIEW_MODEL, REVIEW_EFFORT, REVIEW_OUT, TD | gpt-6-astra, high, verdict, `L/recut` (:9, :12) |
| astra.sh | REVIEW_PROMPT | unset (the packet); a file whose text replaces the packet (:5, :9) |
| test_ship.sh, test_train.sh | SHIP_SRC, TRAIN_SRC | the sibling script, or its `.new` when the suite is the staged copy (test_ship.sh:10, test_train.sh:9-11) |

## Ledger and metrics

`TD/ledger.tsv` (columns `utc ticket event rc detail`, UTC; speak MDT = UTC-6) is the trace of every ticket. Events: `dispatch` (mklane.sh); `build`, `blocked`, `verified`, `ruling`, `install` (MAESTRO by hand); `start`, `mutants`, `tests`, `close`, `wait`, `admit`, `probe`, `prereview`, `astra`, `ready`, `stop` (ship.sh); `land`, `merged`, `lane`, `branch`, `hygiene`, `done`, `wait`, `stop` (train.sh, or ship.sh with TRAIN=0). Write the hand rows too: a decision missing from the ledger is missing from every report built on it.

Two rc values mislead a reader who counts failures by rc. A fix-round close row carries the close's non-zero rc although the round succeeded, for example `close 2 fix round: open PR #95, head ... pushed` (ship.sh:382): count it as a close. A `stop` called with rc 0 is written as 1 (ship.sh:48), so every `stop` row is non-zero.

`TD/METRICS.md` (operator, 2026-10-16: "Proceed with the current workflow tracking all metrics for observability."): one row per ticket with dispatch, builder done, each fix round, gate (mutants killed/total, seconds), close, pre-review (minutes, verdict, BLOCKING), Astra (minutes, verdict, BLOCKING), ready, train minutes, merged, dispatch-to-merged minutes against 15, and the cause of each overrun. Derive the times from the ledger. Example: `L/w1opt/followup-318/METRICS.md`. Pre-review value (catches against minutes added) feeds Step 327.

- Count landed tickets from `gh pr list --state merged`, never from a running tally; a tally drifted by one across five reports to the operator [R24].
- The dashboard `tickets` tab (`M/code/apps/dashboard/dashboard_tickets_tab.sh [session]`, added by `M/code/apps/dashboard/team_dashboard.sh:35`; view `M/code/apps/dashboard/dashboard_tickets.py`, data `M/code/apps/dashboard/dashboard_tickets_data.py`) reads every LEAN folder with tickets/: TD/tickets, TD/ledger.tsv, review rounds, git, one `gh pr list`. It shows one review round per ticket [G11]. `L/metrics/tickets.csv` and `L/metrics/sessions.csv` were built by hand and have no writer; do not rely on them [G11].
- The old board `L/board.py` (recut tickets from git and gh) is superseded by the tab.

## Disk, permissions, sessions (every stage)

- Disk: `df -h /Volumes/memit` before fix lanes; floor 20 GiB, and admission refuses below it too. Reclaim only regenerable dirs, through `L/tools/reclaim.py` (appends `L/tools/reclaim-ledger.tsv`; its ALLOWED pattern covers only `/Volumes/memit/llmdb-lanes/r<N>/T<N>/evidence/.../run/.../product`, prefix `/Volumes/memit/llmdb-lanes/r`). Dry run, then apply, in this exact form (allow rule settings.json:39): `python3 -I /Volumes/memit/corpus-consolidation-toolkit/workspace/runs/20261013-overnight/G-build/LEAN/tools/reclaim.py LIST [--apply]` [R37] [G15].
- Permissions: on any permission prompt or denial, hand the operator one `!` command that adds a narrow durable allow rule to `/Users/robertrhu/.claude/settings.json` (with a backup), as its own message; never retry a denied step in another form. A governance edit ordered only by a handoff is denied (Instruction Poisoning / Self-Modification): ask the operator for a chat approval that names the files [R50]. Rules the flow depends on: the gate (settings.json:25), `pkill -f code/agents/context_watch.py` (:28), hygiene (:37, the relative form, so run it with cwd = M exactly as `.venv/bin/python -B code/ops/git/git_hygiene.py --apply`), Edit on S (:38), reclaim.py (:39), install_staged.sh (:40), the hand-cleanup commands (:29-36). The permission mode is dontAsk (:42): a command outside these rules is refused, not asked, so type the allowed forms literally.
- Session: arm `M/code/agents/context_watch.py <transcript> 300000 60 7200` at session start in Bash background mode; reset at about 300k at a clean boundary with Memento `finalize-session --reset clear`, after writing the handoff [R49]. To hold a scheduled reset: `pgrep -fl finalize-session`, then kill that pid.
- Watchers and the predecessor: a predecessor's watchers, builders and lands survive a Memento reset and report into the successor. Before acting on a notification, check which transcript the watcher watches; watchers must be owner-checked (`M/code/agents/context_watch.py`, and `/Volumes/memit/corpus-consolidation-toolkit/workspace/runs/20261012T114331Z-2ec28dcb/icm-v2/phase3/step6/team/step6watch.py` for tmux team panes) [R48] [G17]. Before re-dispatching a "lost" builder or re-running a land after a reset, check for the predecessor's live land and builders (`pgrep -f land.sh`, tmux windows, lane mtimes); two builders once wrote one lane that way [R26].
- zsh traps: `echo ====X` fails (= expansion); `for x in "$spec"` does not split [R53].
- External tools the flow calls: the codex CLI (`codex exec`, pre-review and Astra), `gh` (repo from cwd), `git`, `tmux` (dashboard, team panes), `lsof` (hygiene).

## Close-out rule

Operator, 2026-10-16, verbatim: "any upgrades, updates, feature adds to code are closed with these context updates where they are relevant in all related/relevant documents."

A change to any workflow tool or to the skill (a MAESTRO step, a ticket that changes a gate, a new allow rule, a new ledger event) is not closed until all four are current:
1. this file, `_system/governance/TICKETS.md`, and every other governance file that describes the changed part;
2. the CLAUDE.md routing row that reaches this file (then regenerate the twins AGENTS.md and routing.md);
3. the skill (S/SKILL.md, S/references/worker.md, S/references/reviewer.md) where it describes the changed part;
4. the related memory files in MEM (listed in § Pointers), updated in place, then targeted hygiene on the files the work touched.

Record the doc updates in the step's ledger row (the Step 325 install row says "docs pending: TICKETS.md (exit 5, tests row, test-edit-allow.json)"; that row stays open until they are written).

The tool works, the suite is green, and you will think *"docs after the next step; the code is the source of truth."* The code is the truth for the code. For the next session, the truth is what routing reaches: a feature that lives only in a script comment or a handoff is invisible to a successor that reads CLAUDE.md first, and it re-learns the trap at full price. "Ship small, document later" is right for a feature behind a flag; it is wrong here, because this workflow is run by agents who know only what the docs tell them. The memory drift in [G12] is what "later" looks like.

## Pointers (rules that live elsewhere)

- Merging, the gate, and the cooperative rule: `_system/governance/MERGING.md`.
- Context management for MAESTRO and every team session: `_system/governance/OPERATING-MODEL.md` § Context management.
- Bulk writes, downloads, deletions: `_system/governance/STORAGE.md`.
- Halt discipline and correctness gates: `_system/governance/DISCIPLINE.md`.
- Codex builders and tools: `_system/governance/CODEX.md`.
- Memory that holds this workflow's lessons (update in place, never append a duplicate): MEM/lean-ticket-lane-traps.md, MEM/lean-tools-ship-and-cut-base.md, MEM/atomic-units-parallel-worktree-lanes.md, MEM/workflow-change-closes-with-doc-updates.md, MEM/icm21-part2-and-workflow-approvals.md, MEM/check-gpu-counts-team-pythons.md, MEM/fix-lane-evidence-fills-memit.md, MEM/merge-gate-first-use-learnings.md, MEM/build-gate-allow-rules.md, MEM/atomic-unit-builder-lifecycle.md, MEM/rerun-builder-tests-host-tmpdir.md, MEM/review-substitution-is-exception.md, MEM/one-shot-run-needs-real-scale-dry-run.md.
- Handoffs: HO/HANDOFF-STEP65.md is the latest (it supersedes HO/HANDOFF-STEP64.md; STEP50-63 before them). A handoff carries a session's state; a rule found in one belongs in this file or in memory, where the next session will look.
- Wave-1 filesystem rulings: `L/part2/extra-fd-binding.md` and `L/part2/reviews/<T>/RULING.md` (for example `L/part2/reviews/T201/RULING.md`).

## Known gaps (all open on 2026-10-17)

Evidence is from the sweep unless marked "since".

- [G1] open. Nothing in L or S is version-controlled (ship.sh, train.sh, land.sh, astra.sh, prereview.sh, mklane.sh, install_staged.sh, the suites, tickets.py, SKILL.md, worker.md, reviewer.md). The only history is `*.bak-*` copies. Evidence: corpus-consolidation-toolkit `.gitignore:4` (`workspace/runs/*`); `~/.claude/.gitignore:1` (`*`). The operator accepts this (§ Roots); it is listed so nobody "fixes" it by moving tools.
- [G2] open. Leaked Astra slot `L/tools/astra.slot.1` (empty, mtime 2026-10-16 11:47) with no ship or codex process; capacity 5 of 6; nothing reaps a slot left by a SIGKILL. Evidence: `ls -la L/tools`; ship.sh:207-219 (release only in the EXIT trap). Since: T318's ship took astra.slot.2 (TD ledger 2026-10-17T00:25:55Z). On 2026-10-17 ~06:40Z no `L/tools/astra.slot.*` dir exists (`ls`); the cause of the leak is still unknown.
- [G3] open, half closed. Gate 1a and check 1b had never run on a real ship. Since: 1a ran on T318 (8/8 killed, 5.2 s, ledger row 2026-10-17T00:25:46Z); 1b has written no row yet (T318's test file is new since its base). Evidence: `grep $'\tmutants\t'` over L/*/ledger.tsv.
- [G4] open. CI runs none of the workflow's own tests: `test_guard_mutants*.py`, `test_compute_sample*.py`, `test_c10w_p2_gate_sampler.py`, `test_fault_kit.py`, `test_fdsafe.py`, `test_dashboard_tickets_*.py`, `test_context_watch.py`; the stub suites and S/tests/test_cut.py (fixture S/tests/sample_plan.md) cannot run in CI. Evidence: M/.github/workflows/ci.yml:43-60.
- [G5] open. Scripts with no test: land.sh, astra.sh, prereview.sh, mklane.sh, install_staged.sh, reclaim.py, mkfixbriefs.py, mkbrief.py, board.py, step6watch.py, dashboard_tickets_tab.sh (test_ship.sh only stubs astra.sh and land.sh). Evidence: sweep of L/tools and M test files.
- [G6] open. train.sh:21 says "Run it from anywhere"; its gh calls (train.sh:163, :243, :279) need cwd = M. Evidence: train.sh:21; MEM/lean-tools-ship-and-cut-base.md:22.
- [G7] open. astra.sh's exit status is `head`'s (astra.sh:51-52), not codex's. A codex failure that leaves no verdict file still fails `head`, but one that leaves an older verdict file passes. Since Step 326, ship.sh moves an earlier verdict aside before each review (aside(), ship.sh:81-94), so inside a ship the failure stops the ship; astra.sh run by hand still passes on an older file. astra.sh also hardcodes L (astra.sh:11) and the lane, ignoring LANES (astra.sh:12). Evidence: astra.sh:11-12, :51-52.
- [G8] open. Brief templates are split and stale: `L/tools/template-brief-builder.md` (T020, no guard step); the live `L/w1opt/brief-template.md` hardcodes W paths; mkbrief.py accepts only T301-T305; `L/tools/template-brief-fix.md` is T020-specific; mkfixbriefs.py hardcodes Part 2. Evidence: template-brief-builder.md:36-37; mkbrief.py:6.
- [G9] open. A third copy of the skill in L/tools/ticketizer (`L/tools/ticketizer/SKILL.md`, `L/tools/ticketizer/scripts/tickets.py`, `L/tools/ticketizer/references/reviewer.md`, `L/tools/ticketizer/agents/openai.yaml`, `L/tools/ticketizer/tests/test_cut.py`, `L/tools/ticketizer/tests/sample_plan.md`) with a stale `L/tools/ticketizer/references/worker.md` (identical to `S/references/worker.md.bak-20261016-310`, no guard rule). Nothing calls it; read S, never the copy. SKILL.md:100 says keep one copy. Evidence: `cmp` results.
- [G10] open. S/SKILL.md does not describe the live flow: dispatch by plain `git worktree add` (SKILL.md:64), "merge each PR ... as CLAUDE.md routes merges" (SKILL.md:81), and no mklane.sh, ship.sh, train.sh, guard_mutants, test-edit check, pre-review or admission. This file now names them; the skill still does not. Evidence: S/SKILL.md:59-82.
- [G11] open. Dashboard review contract mismatch: dashboard_tickets_data.py:326-331 reads rounds from `reviews/<T>/r<N>/verdict.md`, but astra.sh overwrites `reviews/<T>/verdict.md` each round and older rounds are renamed by hand; prereview.md is not read; the tab shows one round. `L/metrics/tickets.csv` has no writer. Evidence: dashboard_tickets_data.py:273-276, :326-331; astra.sh:51.
- [G12] open. Memory drift: MEM/lean-tools-ship-and-cut-base.md:8 says ship.sh lands, and :18 says 3 Astra slots; live ship.sh stops at a ready marker by default (TRAIN=1, ship.sh:33) and uses ASTRA_MAX 6 (ship.sh:150). Since: install_staged.sh is now named in HO/HANDOFF-STEP59.md:27 and MEM/workflow-change-closes-with-doc-updates.md:12, but in no ship/lane memory. Evidence: MEM/lean-tools-ship-and-cut-base.md:8, :18.
- [G13] open. Backups that break the flow if restored alone: L/land.sh.bak-20261016 lacks the "PR must include the current origin/master" match (land.sh:30-31); astra.sh.bak-20261016e writes head.sha, not verdict.sha (breaks ship.sh:390 reuse); ship.sh.bak-20261016-310 has no guard gate; ship.sh.bak-20261016-325 has no 1b check; ship.sh.bak-20261016 and b-f predate admission and ready markers; each ship.sh backup pairs with its test_ship.sh backup. Evidence: `diff` of each backup against live.
- [G14] open. land.sh's ci() hides gh errors (`2>/dev/null`, land.sh:14) and reports "none" after 20 minutes; only on the TRAIN=0 path. Evidence: land.sh:14.
- [G15] open. reclaim.py's ALLOWED covers only r<N>/T<N> evidence product dirs; failed `land-<id>` worktrees, stale tk-* lanes and `TD/reviews/<T>/work` mutant trees (L/w1opt/reviews/T303: verdict.log 894 KB, prereview.log 555 KB, work/) have no reclaim path. Evidence: reclaim.py:15.
- [G16] open. `S/scripts/__pycache__/tickets.cpython-314.pyc` was written into the skill by a Python 3.14 import without `-B` (test_cut.py imports tickets.py). Run the skill's tests with `python3 -B`. `S/.DS_Store` is Finder metadata, also not part of the workflow. Evidence: `ls -lT S/scripts/__pycache__`.
- [G17] open. step6watch.py lives in an older run folder (20261012T114331Z-2ec28dcb/.../step6/team/), unversioned, untested, named only in memory. Evidence: MEMORY.md index.
- [G18] open. The base checkout `/Volumes/memit/llmdb-lanes/base` is refreshed by hand only; a stale base gives cut verdicts against an old master. Evidence: MEM/lean-tools-ship-and-cut-base.md:14.
- [G19] corrected, minor. The sweep said admission waits until swap falls back. Live: ship.sh:126-127 overwrites `L/tools/compute.last` with every sample, refused ones included, and :131 compares each sample against the previous one, from any ship. A swap refusal clears after one 15 s interval in which swap stays flat; it does not have to fall. The open point is only that "previous" may be another ship's sample. Evidence: ship.sh:126-131.
- [G20] open. Memory marks item 3 of the 2026-10-16 approvals (the review-round rule) "unverified"; the rule is present in SKILL.md:88-95 and reviewer.md:12-18, so the memory is stale on that point. Evidence: MEM/icm21-part2-and-workflow-approvals.md:24.
- Since the sweep: M93 (a kill must fail for the right reason) is a known gap of the guard_mutants gate (HO/HANDOFF-STEP59.md:49).
- [G21] open. The INT-after-mkdir stub case in test_ship.sh is timing-flaky: 1 of 3 live runs, 1 of 3 staged runs in 326 round 2, 4 of 30 mutant runs under load.
- [G22] open. guard_mutants' O_RDONLY drop mutant is always equivalent (`os.O_RDONLY == 0`): it needs an allow entry each time; consider skipping zero-valued flags.
- [G23] open. A ticket that repairs a syntax error cannot pass gate 1a: the revert-file mutant refuses to parse the base file. MAESTRO handles such a ticket by hand.
- [G24] open. The train's gate refuses on lsof while a review or mutant run holds a temp lane; the retry cap is 6 tries.
- [G25] open. The OpenAI content filter stops Astra on signal-stress reviews of ship.sh cleanup (326 r3) and stopped the Codex pre-review before (T303 r3, T318 r2). A dead codex leaves its stub suites running as orphans: check `ps` and kill them before hygiene.
- [G26] open. ship.sh survivors ignore_pid, no_term_pid_fallback and no_kill_pid_fallback are race-only (the fork-to-setpgid window); no stub case can reach them (326 ruling 14).
- [G27] open. Two signals back to back: the second signal's exit code can win in sig(); release runs once and cleanup is correct.
- [G28] open. A background subagent that resumes after its own background job, after a MAESTRO /clear, runs on the parent's model (326 r3 went from claude-fable-5-1 to claude-opus-5-5). A brief for a model-specific reviewer says "foreground only".
- Inherited coverage gaps from the T319 reviews: M17 and M19 (round 1); M03, M35, M36 (pre-review round 2); M34-M36 (Astra round 1). T319 sweep N3 at :334 is equivalent on APFS only.

## Path index (for trace.py)

`L/w1opt/staged/tickets-doc/trace.py --doc` checks that every workflow file and every path the scripts name appears in this file. These are the strings that are not workflow stations, listed so the check can pass; what each one is, is in INVENTORY.md §2:
- Roots as the scripts name them: `L`, `M`, `L/tools`, `L/tools/ready`, `L/tools/ready/`, `L/tools/ready/claimed`, `L/tools/ready/claimed/`, `TD/reviews/<T>/`, `L/w1opt/staged/<STEP>/*.new`.
- Script-internal forms: `/Volumes/memit/llmdb-lanes/tk-<mk>` (train.sh:97), `/Volumes/memit/llmdb-lanes/tk-<T>/<f>` (ship.sh 1b existence check), `L/tools/ship.sh<SUF>`, `L/tools/train.sh<SUF>`, `/<v>` (the `${P//"{{$k}}"/$v}` substitution at astra.sh:25, read as a path).
- System paths: `/bin/sh`, `/bin/zsh`, `/usr/bin/env`, `/dev/null`, `/bin/mkdir`, `/bin/rmdir`, `/bin/mv`, `/var`, `/private/var`.
- Stub-suite fixture strings (not paths on disk): `/d`, `/gone`, `/l/tk-T900`, `/pull/41`, `/tmp/elsewhere`, `/x`, `/astra.slot.1`, `/bin/sleep`, `/stub.pids`, `/stub.ready` (the last four in test_ship.sh since Step 326).

## Recap

- The goal: every ticket dispatch to merged in 15 minutes; all ready PRs land in one train, never serially.
- The belt: plan → `tickets.py cut --base` → `mklane.sh` → brief from `L/w1opt/brief-template.md` → builder (worker.md, revert check) → MAESTRO verifies → `ship.sh` (1a guard mutants, 1b test-file edits, close, pre-review, Astra under admission, ready marker) → `train.sh` from cwd M (batch gate, cleanup, hygiene) → ledger and METRICS.md.
- Hand work drops the ticket off the belt: no hand commit (re-ship), no hand merge (the gate), no `cp` over a tool (install_staged.sh), no edit to a pinned review file (a new note).
- Allow files and rulings are MAESTRO's alone, each with its reason.
- A tool change closes only when this file, the routing row, the skill and the memory say what is now true.
