# Stage 4 — Briefs
Part of the tickets guide. Router: `_system/governance/TICKETS.md`. Roots (L, M, S, W, TD, MEM, HO): `00-roots-and-roles.md`.

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

