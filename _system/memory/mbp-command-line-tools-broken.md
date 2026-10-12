---
name: mbp-command-line-tools-broken
description: "HISTORICAL (fixed 2026-10-07): broken Xcode CLT on the M3 Pro; CLT 27.0 now installed. Lesson: hand admin-only fixes to the operator at once"
metadata:
  type: project
---

**FIXED 2026-10-07.** The operator ran `sudo softwareupdate --install "Command Line Tools for Xcode 27.0-27.0"`; pkg `com.apple.pkg.CLTools_Executables` = 27.0.0.0.1788430756, `xcrun --show-sdk-path` = `.../SDKs/MacOSX.sdk`, and a hello-world compiles and runs with no `SDKROOT` override. Native C/C++/Rust builds (llama.cpp with Metal, llama-cpp-python, LARQL) are no longer blocked by the toolchain.

**History:** found 2026-10-04 — CLT 26.6 plus a 27.0 beta SDK installed the same day (2026-09-14); the 26.6 `ld` could not read `MacOSX27.0.sdk/.../libSystem.tbd` ("unknown architecture"). Workaround then was `SDKROOT=/Library/Developer/CommandLineTools/SDKs/MacOSX26.sdk` or prebuilt binaries. The `metal` CLI was also absent (needs full Xcode; still true unless verified).

**Lesson (operator, 2026-10-07: "why would you leave them that way. Fix it."):** I recorded the admin-only fix in memory for three days without putting it in front of the operator. When a fix needs the operator's password, check `softwareupdate --list` for the official update and hand them the one command right away, in plain words. Related: [[operator-decision-scope]].
