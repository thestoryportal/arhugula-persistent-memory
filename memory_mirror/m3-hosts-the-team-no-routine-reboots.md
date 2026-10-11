---
name: m3-hosts-the-team-no-routine-reboots
description: Any design step that reboots/logs out the M3 kills MAESTRO, every Codex builder and the operator's phone/Termius link (all in tmux there); reject it as a routine mechanism
metadata:
  type: project
---
MAESTRO, all Codex builders and the operator's remote access (Claude remote control + Termius into tmux) run on the M3 under the operator account. The R2 redesign draft (codexr2d, 2026-10-11) proposed a full M3 reboot as the routine switch between science and Drive backup; MAESTRO61 caught it before Astra and replaced it with dedicated macOS activity accounts (science UID / backup UID; "no process of the opposing UID" is a complete, list-free exclusion), reboot recovery-only (`results/compute_storage_brainstorm_20261011T054507Z/r2_git_drive_redesign_v1.md` R2).

**Why:** builders optimise for provable safety and don't know the team's host topology unless told; a reboot looks "conservative" but ends every session.

**How to apply:** when reviewing any host-level design (backup, admission, sandbox, storage), ask "what else runs on this machine, and does this step end it?" Put the M3-hosts-the-team fact in briefs for host-level designs. Related: [[remove-shared-resource-before-policing-it]].
