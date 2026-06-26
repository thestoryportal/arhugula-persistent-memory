---
title: AnyEdit token alignment gate prevents false rescue
date: 2026-06-26
decision: D-C10h-anyedit-viability
---
Advisor-review returned FIX-FIRST on the C10 AnyEdit viability audit: upstream AnyEdit tokenizes `answer` standalone but computes keys over `question + answer`, so Qwen continuation tokenization mismatch could create a false rescue or false failure. A no-GPU gate on current A7 passes 24/24 suffix alignment with leading-space answers. The prereg/harness must emit answer IDs, continuation suffix IDs, decoded text, window boundaries, and lookup indices for every request, and abort on mismatch or malformed decoded text.
