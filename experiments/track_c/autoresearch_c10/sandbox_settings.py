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

# v11: the reviewer kept finding history in places no list named (an archive copy in the home folder, the GitHub CLI
# cache, a sweep-trials folder at the root of the external drive). So the home folder, every drive and the per-user temp
# area are now denied by default: every child is listed as denied unless it is one of the few a run needs. Children,
# not the parents, so the file-tool rules (where a deny always wins) never cover a runtime path.
import subprocess


def children(root, keep):
    return [f"{root}/{n}" for n in sorted(os.listdir(root)) if n not in keep] if os.path.isdir(root) else []


shell_init = (".zshenv", ".zshrc", ".zprofile", ".zlogin", ".zlogout", ".zcomp")   # .zsh_history / .zsh_sessions are not
home_keep = {".cache", ".local", "Library"} | {n for n in os.listdir(home) if n.startswith(shell_init)}
library_caches = f"{home}/Library/Caches"
# v12: the v11 review read a Chrome cache object (a saved web page with old results) under ~/Library/Caches/Google, so that
# folder is deny-by-default too: only the caches the model runs use stay open
# (com.apple.python is the system python's bytecode cache, a file-system mirror holding decodable copies of scripts; not runtime)
caches_runtime = {"com.apple.metal", "com.apple.metalfe", "torch", "huggingface", "pip", "uv"}
history_enum = (
    children("/Volumes", {"memit", "Macintosh HD"})                       # the other drives
    + children(mirror.rsplit("/", 1)[0], {mirror.rsplit("/", 1)[1]})       # the external drive outside the mirror
    + children(home, home_keep)                                            # the home folder
    + children(f"{home}/.local", {"share"})                                # ~/.local: only share/uv is runtime
    + children(f"{home}/.local/share", {"uv"})
    + children(f"{home}/Library", {"Caches"})                              # ~/Library: only the caches folder, and only part of it
)
# the denied caches sit inside the allowed ~/Library/Caches, so they go after the allows (last matching rule wins in the profile)
denied_inside_allowed += children(library_caches, caches_runtime)
# the per-user temp folder (getconf DARWIN_USER_TEMP_DIR): other processes' temp files; the agent's TMPDIR is /tmp/claude-501
user_tmp = subprocess.run(["getconf", "DARWIN_USER_TEMP_DIR"], capture_output=True, text=True, check=True).stdout.strip()
history_enum.append(os.path.realpath(user_tmp).rstrip("/"))
seen = set(denied_roots)
denied_roots += [r for r in history_enum if not (r in seen or seen.add(r))]
# the roots themselves, for the two shell layers only (narrower allows re-open the runtime pieces; a listing of the root
# would otherwise still show the names). Not for the file tools, where a deny on a root would cover the runtime children.
shell_only_denied = ["/Volumes", mirror.rsplit("/", 1)[0], home, f"{home}/.local", f"{home}/.local/share", f"{home}/Library"]
# the home-folder pieces a run reads, now named because the home root is denied in the shell layers
runtime_reads += [f"{home}/.cache/huggingface", f"{home}/.cache/uv", f"{home}/Library/Caches"]
runtime_reads += [f"{home}/{n}" for n in sorted(os.listdir(home)) if n.startswith(shell_init)]

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
    lines += [f"(deny file-read* (subpath {q(r)}))" for r in denied_roots + shell_only_denied]
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
            "denyRead": denied_roots + shell_only_denied + denied_inside_allowed,
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
