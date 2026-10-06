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
settings = {
    "sandbox": {
        "enabled": True,
        "allowUnsandboxedCommands": False,   # strict mode: the agent's dangerouslyDisableSandbox retry is ignored
        "excludedCommands": [],
        "filesystem": {
            "denyRead": denied_roots,
            "allowRead": runtime_reads + [sandbox],
            "allowWrite": [sandbox, "/tmp", "/private/tmp", hf_home, f"{home}/.cache", f"{program}/experiments/track_c/__pycache__"],
            "denyWrite": [program, repo],
        },
    },
    "permissions": {
        "deny": [f"Read(/{root}/**)" for root in denied_roots] + ["Agent", "Task"],
        "allow": [f"Read(/{p}/**)" for p in runtime_reads] + [f"Read(/{sandbox}/**)"],
    },
}
print(json.dumps(settings, indent=1))
