**FIX-FIRST.**

**Next: make the context boundary enforceable and pass a no-GPU escape test before relaunching.** Copying the harness removes one invitation to explore; it does not satisfy the operator’s context restriction.

1. **The criterion is context isolation, independently of scoring correctness.** Runbook §5.2, `EXPERIMENT_RUNBOOK.md:320`, explicitly excludes research-corpus context. Consequently, `docs/AUTORESEARCH.md:43` calling scorer separation “the fence … that matters for the science” dismisses a binding experimental condition. A separate scorer also does not, by itself, protect writable scorer files.

2. **There is another concrete escape: shared Git history.** From the sandbox, I successfully ran:
   ```sh
   git show worktree-c10k-route-a:docs/AUTORESEARCH.md
   ```
   Exit **0**, **12,246 bytes**, expected document header. An orphan branch does not isolate the shared object database. Use a standalone sandbox repository without shared objects/alternates, alongside filesystem restrictions. This probe tested the existing filesystem layout, not a newly launched Claude session.

3. **Read/Glob/Grep denies alone are insufficient; ordinary hooks conflict with safe mode.** Arbitrary Python subprocesses bypass file-tool permission rules; ordinary customization hooks are disabled by `--safe-mode`. [Permission documentation](https://code.claude.com/docs/en/permissions), [CLI reference](https://code.claude.com/docs/en/cli-reference).  
   The cheapest plausible approach is strict Bash filesystem sandboxing **plus** file-tool restrictions, with no excluded commands or unsandboxed retries; alternatively, sandbox the entire Claude process while retaining permission bypass internally. [Sandbox documentation](https://code.claude.com/docs/en/sandboxing). **Compatibility with this installed CLI’s safe-mode combination is UNVERIFIABLE until exercised.** Runtime dependencies need narrowly scoped access: denying all of `PROGRAM_ROOT` breaks the imports and reference check (`prepare.py:29–33,85`). Broadly allowing it defeats isolation.

   **Acceptance test:** in a disposable session using the exact launch flags, try outside reads/listings through file tools, Bash/Python, symlinks, Git objects, and a helper. Require **zero successful forbidden accesses**, with an allowed-file positive control and successful setup. Discard that test session before starting research.

4. **Copy drift is real, but a fresh expensive equivalence run is unnecessary for this diff alone.** I verified **all three current source hashes** match the recorded **PASS** (`results/autoresearch_c10_equivalence.json:209–214`). `prepare.py:30,85` hashes/imports the program harness, so the sandbox copy is merely what the agent reads. Check its hash against the same manifest after copying and on every launch, including the resume branch that skips copying (`launch.sh:53–67`). Current sandbox inspection still found a symlink: deployment of the proposed copy remains unverified. Measurement-code changes would invalidate the existing gate.

5. **Stopping the contaminated session was correct; killing an unchanged baseline was optional.** Under the ruling, future ideas from that session cannot qualify. An untouched baseline could have finished as a quarantined instrument check; context exposure alone does not establish numerical corruption. The claimed helper shutdown timing and ≈117k-token exposure remain **UNVERIFIABLE from the inspected artifacts**. The sandbox TSV currently contains **one header, zero result rows**.

6. **The bullet constrains scope without seeding a method, but needs precision.** `program.md:36` should distinguish agent information access from trusted runtime dependency reads and explicitly retain the permitted cited-paper exception. Replace “worthless” with “invalid for this context-restricted run.” Separately, “Fable 5.5” → `claude-fable-5-1` is an interpretation, not the literal operator order; “only offered model” is **UNVERIFIABLE** here. Record the substitution accurately.

**Drift check:** this supports C10 candidate discovery, hence F1 indirectly. It supplies no new readiness evidence; the candidate-only boundary in `docs/AUTORESEARCH.md:62` must remain.