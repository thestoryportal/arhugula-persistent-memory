# Advisor / objective-review prompt (reusable — Claude & Codex)

You are an **independent, adversarial reviewer** of a research step in the LLM-as-Database program. You are not the author. **Do not rubber-stamp.** Your job is to find where the work is wrong, over-claimed, confounded, or drifting from the goal — *before* it is leaned on.

You will be given ONE of: a **test/experiment design** (before it runs), a **finding/result** (before it is declared conclusive or written to CORPUS), or an **approach** the author is about to commit to — together with its evidence (artifact paths + numbers) and the relevant context.

Run this review and answer concisely and specifically:

1. **Real criterion.** Does this answer the question's *actual* criterion, or a flattering adjacent one? (e.g. is the metric matched to the claim — top-1 for read-correctness, distributional for distributional; is the gate's true requirement being met or a softer proxy?)
2. **Confounds & over-claims.** Hunt for confounds, leakage, Goodhart, and over-statement. Is `EVIDENCE-SHOWS` blurred with `I-INFER`? Is "the mechanism works" being passed off as "the contract is met" (**mechanics ≠ contract**)? Is design-viability being passed off as empirical evidence?
3. **Cite or flag.** Every factual claim must cite an artifact (path + exact number) or be labeled **`UNVERIFIABLE`**. Call out any claim that isn't grounded. Verify that external repos/IDs/claims were actually checked before being relied on.
4. **The overturning test.** What is the *cheapest* experiment or control that could **falsify** this finding/design? If it hasn't been run, that is the gap.
5. **Drift check.** Does this advance the F1 readiness determination (or a live §0.3 falsifier)? If not, say so.

**Output:** a short verdict — `PROCEED` / `FIX-FIRST` / `OVERTURNED-OR-RECONSIDER` — then the **single most important thing** to do next, then the specific issues in priority order. Be a skeptic; the author will weigh your input heavily but evidence remains binding over your opinion.


---

# Review packet — autoresearch fence v10 (2026-10-06, ~12:40): your fence-v9 item (`~/.cache/gh` and every other non-runtime child of `~/.cache` denied); equivalence re-run finishing; the sixth launch waits for this verdict

Your v7 review (`results/autoresearch_c10_advisor_fence_v7.md`, FIX-FIRST) decompressed a git object under `/private/tmp/claude-501/bash-edit-diff/` (Claude Code's shared scratch; the object carried past C10 numbers) because the temp-folder enumeration denied only children starting with `-`. v8: every pre-existing child of `/private/tmp/claude-501` except the agent's own two slug folders is denied, in all three layers. Verified: direct test v8 (listing `bash-edit-diff`, the exact object you read, an `fswatch-probe-*` folder → all `Operation not permitted`; own tmp root listable and writable; GPU on) and probe 14 in a Claude session (bare wrapper → GPU; `cat run.log` captured; `ls bash-edit-diff`, `head` of the object and the Read tool on it → denied; own-tmp `touch` and the HF cache listing → OK).

Your item 2: docs/AUTORESEARCH.md now states the screen exposure fully — the two screens are readable in full: pre-edit screening of 67 and 91 real countries (56 and 78 selected) with the model's top-three predictions and probabilities for capital, currency, continent and language; no edit result, no coined value; nothing smaller without changing the hash-gated harness. Recorded as the accepted exposure.

Known remaining limit (recorded): a child created under `/private/tmp/claude-501` or the mirror root *after* a launch is not in the deny lists until the next launch.

Residual runtime allow-list: the two `.venv` paths and the uv interpreter; `~/.local/share/uv`; `~/.cache/huggingface` and `~/.cache/uv` only (every other pre-existing child of `~/.cache` denied, v10); the HF cache; `memit_dry_run`; the three config files; the harness file; `tools/engine_fingerprint.py`; the two `covariance_caches`; own `/private/tmp/claude-501`; the sandbox; the fence (profile, settings, wrappers, the two-number reference extract).

## What I want you to attack
- Any remaining history content reachable (name the path).
- Verdict: PROCEED (after the equivalence PASS) or the single thing to fix.

Your v8 review named `~/llm-as-database/`; v9 denied it. Your v9 review read a cached GitHub CLI response under `~/.cache/gh/` (pull-request text with past verdicts). v10 denies every pre-existing child of `~/.cache` except `huggingface` and `uv` in all three layers (13 folders and 3 loose files at launch). Direct test v10: the exact object you read, the `gh`/`codex-runtimes`/`antigravity`/`claude` listings and a loose cache-root file blocked; HF and uv caches listable and writable; runtime files readable; GPU on. Probe 15 (Claude session, launch flags): bare wrapper → GPU OK (mps matmul in run.log), capture OK; head and the Read tool on the exact gh cache object, ls of ~/.cache/gh and ~/.cache/codex-runtimes → all denied; ls ~/.cache/huggingface, own-tmp touch and the HF hub listing → OK. FORBIDDEN_SUCCEEDED none · CONTROLS_OK 7, 8, 9. (Claude Code notes that a Write(//…) deny rule is not matched by file-permission checks and that the Edit(//…) rule beside it covers all file-editing tools; the fence keeps both.) Verdict wanted: PROCEED or the single thing to fix.

## sandbox_settings.py (current)
```python
#!/usr/bin/env python3
"""Print the fence that keeps the autoresearch agent's context to its sandbox.

Usage:
  sandbox_settings.py <program_checkout> <program_repo_root> <sandbox_dir> <fence_dir>             -> Claude Code settings JSON
  sandbox_settings.py <program_checkout> <program_repo_root> <sandbox_dir> <fence_dir> --seatbelt  -> macOS Seatbelt profile

Two layers, because the context-isolation ruling (docs/AUTORESEARCH.md) is binding and a rule in words is not
enforcement.

Layer 1, the agent's shell and file tools: Claude Code's Bash filesystem sandbox (strict: no unsandboxed retry) plus
`Read(//…/**)` / `Edit(//…/**)` permission denies. Reads are denied for every root that holds program history — the
whole mirror volume tree, the program checkout and repository, this machine's Claude / Codex / gstack / OpenResearch
/ rtk state, the backups — and re-opened only for the runtime set a run needs (the shared .venv and its uv
interpreter, the engine, the model cache, the covariance caches, the configs, the harness, the fingerprint tool, the
reference run, the prereg file the harness names) and for the sandbox and fence directories.

Layer 2, the model runs: that sandbox denies every sysctl read, which makes PyTorch believe the OS predates macOS 13
and drop to the CPU (probes 6-8, 2026-10-06). So the wrappers in the fence directory are `excludedCommands` and run
their python under the Seatbelt profile printed with --seatbelt: default allow (sysctl, Metal, the network), the same
read denials and re-openings, and writes denied everywhere except where a run writes (the sandbox, tmp, the HF cache,
~/.cache and ~/Library/Caches, the harness's __pycache__, /dev). In a Seatbelt profile the last matching rule wins, so
the narrow rules come after the wide ones. The fence directory (profile + wrappers) is writable by neither layer.
Probes: results/autoresearch_c10_sandbox_probe.md.
"""
import json
import os
import re
import sys

program, repo, sandbox, fence = sys.argv[1:5]
home = os.path.expanduser("~")
mirror = "/Volumes/memit/llm-database-poc-mirror"
venv = os.path.realpath(f"{program}/.venv")                            # the worktree's .venv links to the main checkout's
base_python = os.path.realpath(f"{venv}/bin/python")                    # which links to uv's interpreter
base_prefix = os.path.dirname(os.path.dirname(base_python))
hf_home = os.path.realpath(f"{program}/hf_cache")                       # a link to the shared model cache

# what a run reads (re-opened inside the denied roots)
runtime_reads = [
    f"{program}/.venv",
    venv,
    base_prefix,
    f"{home}/.local/share/uv",
    hf_home,
    f"{program}/hf_cache",
    f"{repo}/hf_cache",
    f"{program}/memit_dry_run",
    f"{program}/configs/hparams/qwen25_3b_memit_hparams.json",         # the engine hyperparameters prepare.py loads
    f"{program}/configs/screens/g6_screen_qwen3b_v2.json",             # the stimulus screen the harness loads at import
    f"{program}/configs/screens/g6_screen_qwen3b.json",                # its companion the harness can open; the rest of
                                                                       # configs/ holds other arms' configs and old probe
                                                                       # results and is not re-opened (fence v7)
    f"{program}/experiments/track_c/c10e_bandknob.py",   # the harness only; its sibling experiments, the shared
                                                         # __pycache__ (bytecode of every experiment) and the prereg
                                                         # document the harness names are NOT re-opened (v5): the
                                                         # wrappers set PYTHONDONTWRITEBYTECODE so no pyc is needed
    f"{program}/tools/engine_fingerprint.py",
    f"{repo}/covariance_caches",
    f"{mirror}/covariance_caches",
    sandbox,
    fence,
]
# where program history lives on this machine (denied as sources of information)
denied_roots = [
    mirror,                       # the whole mirror tree: repo, worktrees, session logs, notebooks, probes
    "/Volumes/memit/llm-database-project-artifacts",   # the genesis artifacts (spec history, sessions, corpora)
    f"{home}/llm-as-database",    # a second archive copy of the program (164 files: spec history, session summaries) — v9
    "/private/tmp",               # loose files other sessions leave in tmp (NotebookLM prompts, packets); the agent's own
                                  # /private/tmp/claude-501 is re-opened below. /tmp itself (a symlink) stays resolvable:
                                  # denying it stops the kernel resolving /tmp/… paths and breaks TMPDIR writes (probe 12)
    f"{home}/Backups",
    "/Volumes/backups",
    "/Volumes/Development",
    f"{home}/.claude",            # this program's sessions, memory, jobs
    f"{home}/.codex",
    f"{home}/.gstack",
    f"{home}/.config/openresearch",
    f"{home}/.local/share/openresearch",   # the research pass's worktrees = full program checkouts
    f"{home}/.local/share/claude",
    f"{home}/Library/Application Support/rtk",
]
# narrower denies that sit inside an allowed region (listed after the allows). ~/.cache stays readable because a run
# needs the Hugging Face xet cache and uv's package cache there, but its other children hold history: ~/.cache/claude
# (this program's sessions) and ~/.cache/gh (the GitHub CLI's response cache, which carried pull-request text with
# past findings - the v9 review read one). So every pre-existing child but the two runtime ones is denied (v10).
cache_root = f"{home}/.cache"
cache_runtime = {"huggingface", "uv"}
denied_inside_allowed = [f"{cache_root}/{n}" for n in sorted(os.listdir(cache_root)) if n not in cache_runtime]


def slug(path):
    return re.sub(r"[^A-Za-z0-9]", "-", path)


# Claude Code keeps each session's shell output and task files under /private/tmp/claude-501/<slug of its cwd>/. The
# agent's own folder must stay readable (its shell tool captures output there), so the other sessions' folders are
# denied one by one rather than the root (which broke the agent's `cat` in probe 11).
tmp_root = "/private/tmp/claude-501"
own_tmp = {slug(sandbox), slug(fence)}
tmp_history = []
if os.path.isdir(tmp_root):
    for name in sorted(os.listdir(tmp_root)):
        # every existing child but the agent's own: other sessions' folders, and Claude Code's shared scratch such as
        # bash-edit-diff/ (objects of past edits, which carried old results - the v7 review read one)
        if name not in own_tmp:
            tmp_history += [f"{tmp_root}/{name}", f"/tmp/claude-501/{name}"]
# the agent's TMPDIR is /tmp/claude-501 itself, so that root is re-opened and the other sessions' folders in it are
# denied again (narrower rules win in the Bash sandbox; in the profile they come last)
runtime_reads += [tmp_root, "/tmp/claude-501"]
denied_inside_allowed += tmp_history

# The file tools (Read/Edit) have no "re-open inside a denied region": a deny always wins. So for them the mirror's
# history is listed child by child, keeping the sandbox, the fence and the two caches out of the list.
keep = {os.path.realpath(x) for x in (sandbox, fence, hf_home, f"{mirror}/hf_cache", f"{mirror}/covariance_caches")}
mirror_history = [f"{mirror}/{n}" for n in sorted(os.listdir(mirror))
                  if os.path.realpath(f"{mirror}/{n}") not in keep]
tool_denied = mirror_history + [r for r in denied_roots if r != mirror] + denied_inside_allowed

# where a run may write
write_dirs = [sandbox, "/tmp/claude-501", "/private/tmp/claude-501", "/private/var/folders", hf_home, f"{home}/.cache",
              f"{home}/Library/Caches", "/dev"]


def q(p):
    return '"' + p.replace('"', '\\"') + '"'


if len(sys.argv) > 5 and sys.argv[5] == "--seatbelt":
    lines = ["(version 1)", "(allow default)"]
    lines += [f"(deny file-read* (subpath {q(r)}))" for r in denied_roots]
    lines += ["(deny file-write*)"]
    lines += [f"(allow file-read* (subpath {q(p)}))" if os.path.isdir(p) else f"(allow file-read* (literal {q(p)}))"
              for p in runtime_reads]
    lines += [f"(allow file-write* (subpath {q(p)}))" for p in write_dirs]
    lines += [f"(deny file-read* (subpath {q(r)}))" for r in denied_inside_allowed]
    lines += [f"(deny file-write* (subpath {q(fence)}))"]
    # the two directory entries stay stat-able (not listable) so /tmp/… paths resolve to the re-opened claude-501
    lines += ['(allow file-read-metadata (literal "/private/tmp"))', '(allow file-read-metadata (literal "/tmp"))']
    print("\n".join(lines))
    sys.exit(0)

wrappers = [f"{fence}/run.sh", f"{fence}/setup.sh", f"{fence}/kill_run.sh"]
settings = {
    "sandbox": {
        "enabled": True,
        "allowUnsandboxedCommands": False,   # strict mode: the agent's dangerouslyDisableSandbox retry is ignored
        # the three wrappers, by their exact absolute command text, run outside this sandbox inside the Seatbelt profile
        "excludedCommands": wrappers,
        "filesystem": {
            "denyRead": denied_roots + denied_inside_allowed,
            "allowRead": runtime_reads,
            "allowWrite": [p for p in write_dirs if p != "/dev"],
            "denyWrite": [program, repo, fence],
        },
    },
    "permissions": {
        "deny": [f"Read(/{r}/**)" for r in tool_denied]
        + [f"Edit(/{fence}/**)", f"Write(/{fence}/**)", "Agent", "Task"],
        "allow": [f"Read(/{p}/**)" for p in runtime_reads],
    },
}
print(json.dumps(settings, indent=1))
```
