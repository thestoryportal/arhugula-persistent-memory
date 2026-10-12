FIX-FIRST

Reviewer: GPT-6-Astra (high)  
Requested reviewer label; actual backend/effort UNVERIFIABLE.

**BLOCKING**

- **M4 is not fully report-only.** [inertness.py:133](experiments/track_c/c10x_enginepath_inertness.py:133) records an unguarded fp32 norm; [read.py:231](experiments/track_c/c10x_enginepath_read.py:231), `:602` and `:628` reject nonfinite fp32 diagnostics. Serialization also rejects them. Thus fp32 diagnostics can cause HALT/INVALID, contrary to [prereg:583](docs/C10X_ENGINEPATH_PREREG.md:583). **Fix:** encode nonfinite fp32 diagnostics explicitly, admit that representation without affecting scientific acceptance, and add an overflow regression. Preserve strict float64 gate checks. This is a static contract defect, not an observed GPU failure.

**ADVISORY**

- [telemetry_check.py:293](experiments/track_c/c10x_enginepath_telemetry_check.py:293), `:422`: any disable marker excuses **all** missing answers, including earlier gaps. T11 permits that exception only after disable. Track the cutoff and reject earlier omissions; add that negative test before telemetry-on use.
- First-attempt launch commands are correctly telemetry-unset and watchdog-mediated. Skip the separately authorized T8 command. No direct shell launchers require mode changes.

**Verified:** 63 CPU tests passed in 16.063s; no live-tree changes; forbidden imports absent. All 194 reported source/protected-file hashes match. Saved assertion-level RED and 18 mutation logs support the report. No additional discrepancy found in recipes, thresholds, attributed pre-cast capture, template pinning, process combination, or launch gates. Live GPU gates remain UNVERIFIED.

🌱 graft reported ~260,116 tokens saved (~$0.14), 1 successful call.

