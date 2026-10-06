**FIX-FIRST**

**Next: pause candidate iteration and remove the history-bearing runtime exceptions.** I demonstrated two readable history routes under the deployed v4 profile; no enumeration race was needed.

1. **The allowlist itself exposes prior ideas.** Successful reads returned:
   - `docs/C10_BANDKNOB_PREREG.md`: **5,071 bytes**, including prior **19.4% / 37.5%** results and the recommendation to try wider/later bands before AnyEdit.
   - `experiments/track_c/__pycache__/c10q_stacked_arms.cpython-311.pyc`: **12,179 bytes**; decoding its constants recovered the stacked second-edit method and `z_post` versus `z_pre` control.

   In the same probe, README access failed and sandbox `program.md` succeeded; **exit 0**. These are demonstrated context leaks. Deny shared experiment bytecode and remove unnecessary preregistration access. [Exact probe evidence](/Users/robertrhu/.gstack/projects/thestoryportal-arhugula-persistent-memory/checkpoints/20261006-113006-autoresearch-fence-v4-review.md).

2. **PID ownership remains unchecked.** Line **19** accepts any command containing `sandbox-exec -f`, or an unrelated `.venv/bin/python edit.py`. A signal-free predicate test accepted **both** foreign examples. Require verified run identity before signalling; the present OR-pattern does not establish it. [kill_run.sh](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/autoresearch_c10/kill_run.sh:19).

3. **The accepted temporary-directory gap affects shell/profile isolation too.** Lines **89–99** reopen the shared temp root and enumerate existing children. A later child lacks those denials in both layers; this is not exclusively a file-tool limitation. [Generator](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/autoresearch_c10/sandbox_settings.py:89).

**Metadata question:** more than existence is exposed—my probe returned mode, ownership, size and modification time. Directory listing was blocked. I found no content leak through that literal metadata permission. [Probe evidence](/Users/robertrhu/.gstack/projects/thestoryportal-arhugula-persistent-memory/checkpoints/20261006-113006-autoresearch-fence-v4-review.md).

**Cheapest closure test:** repeat the two demonstrated reads and require denial, while retaining successful sandbox reads, shell capture and GPU execution. Actual baseline comparison remains **UNVERIFIABLE** from this review.

**Drift:** this supports F1 indirectly through C10 candidate generation. Candidate-only output does not satisfy the separate no-history/no-seeded-ideas criterion. I did not stop or modify the loop.

