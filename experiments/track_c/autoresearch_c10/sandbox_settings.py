#!/usr/bin/env python3
"""Print the Claude Code settings that fence the autoresearch agent into its sandbox.

Usage: sandbox_settings.py <program_checkout> <program_repo_root> <sandbox_dir>

Two layers, because docs/AUTORESEARCH.md's context-isolation ruling is a binding condition and a rule in words is
not enforcement: (1) the Bash filesystem sandbox, which covers every process a shell command starts, so a Python
one-liner cannot read the program's files either; (2) permission deny rules for the file-reading tools (a `//`
prefix means an absolute path in these rules; Read rules cover every file-reading tool). Reads are allowed only
where a run needs them: the environment and its base interpreter, the engine, the model cache, the covariance
caches, the hyperparameter files, the harness, the fingerprint tool and the reference run. Everything else in the
program checkout, and the research collections beside it, is denied. Which layers hold under
--dangerously-skip-permissions was settled by probe sessions before the relaunch; see docs/AUTORESEARCH.md
"Context isolation and permissions".
"""
import json
import os
import sys

program, repo, sandbox = sys.argv[1:4]
home = os.path.expanduser("~")
venv = os.path.realpath(f"{program}/.venv")                            # the worktree's .venv links to the main checkout's
base_python = os.path.realpath(f"{venv}/bin/python")                    # which links to uv's interpreter
base_prefix = os.path.dirname(os.path.dirname(base_python))
hf_home = os.path.realpath(f"{program}/hf_cache")                       # a link to the shared model cache
runtime_reads = [
    f"{program}/.venv",
    venv,
    base_prefix,
    f"{home}/.local/share/uv",
    f"{home}/.cache",
    hf_home,
    f"{program}/hf_cache",
    f"{repo}/hf_cache",
    f"{program}/memit_dry_run",
    f"{program}/configs",                                                # hparams + the stimulus screens the harness loads at import
    f"{program}/docs/C10_BANDKNOB_PREREG.md",                            # named by the harness's manifest fields
    f"{program}/experiments/track_c/c10e_bandknob.py",
    f"{program}/experiments/track_c/__pycache__",
    f"{program}/tools/engine_fingerprint.py",
    f"{program}/results/c10l_covgeom/run1_armB_identity.json",
    f"{repo}/covariance_caches",
]
denied_roots = [
    program,
    repo,
    "/Volumes/memit/llm-database-poc-mirror/connected-papers-knowledge-graphs",
    "/Volumes/memit/llm-database-project-artifacts",
    f"{home}/Backups/memit",
]
write_dirs = [sandbox, "/tmp", "/private/tmp", "/private/var/folders", hf_home, f"{home}/.cache",
              f"{program}/experiments/track_c/__pycache__"]

if len(sys.argv) > 4 and sys.argv[4] == "--seatbelt":
    # The macOS Seatbelt profile for the model runs. Claude Code's own Bash sandbox denies every sysctl read, which
    # makes PyTorch believe the OS predates macOS 13 and drop to the CPU (probes 6-8, 2026-10-06), so `run.sh` and
    # `setup.sh` are excluded from that sandbox and run under this profile instead: default allow (sysctl, Metal, the
    # network), the same read denials, re-opened only for the runtime set, and writes only where a run writes.
    # In a Seatbelt profile the last matching rule wins, so the allows come after the denies.
    def q(p):
        return '"' + p.replace('"', '\\"') + '"'
    lines = ["(version 1)", "(allow default)"]
    lines += [f"(deny file-read* (subpath {q(r)}))" for r in denied_roots]
    lines += [f"(deny file-write* (subpath {q(r)}))" for r in [program, repo]]
    lines += [f"(allow file-read* (subpath {q(p)}))" if os.path.isdir(p) else f"(allow file-read* (literal {q(p)}))"
              for p in runtime_reads + [sandbox]]
    lines += [f"(allow file-write* (subpath {q(p)}))" for p in write_dirs]
    print("\n".join(lines))
    sys.exit(0)

settings = {
    "sandbox": {
        "enabled": True,
        "allowUnsandboxedCommands": False,   # strict mode: the agent's dangerouslyDisableSandbox retry is ignored
        # the two model-run wrappers run outside Claude Code's sandbox, inside the Seatbelt profile above
        "excludedCommands": ["./run.sh", "./run.sh *", "./setup.sh", "./setup.sh *", "./kill_run.sh", "./kill_run.sh *",
                             "bash run.sh", "bash setup.sh", "bash kill_run.sh"],
        "filesystem": {
            "denyRead": denied_roots,
            "allowRead": runtime_reads + [sandbox],
            "allowWrite": write_dirs,
            "denyWrite": [program, repo],
        },
    },
    "permissions": {
        "deny": [f"Read(/{root}/**)" for root in denied_roots] + ["Agent", "Task"],
        "allow": [f"Read(/{p}/**)" for p in runtime_reads] + [f"Read(/{sandbox}/**)"],
    },
}
print(json.dumps(settings, indent=1))
