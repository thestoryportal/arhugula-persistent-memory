# First gated merge — step 4: GitHub-side inventory, reservation, drain (MAESTRO9, 2026-10-10)

Candidate: PR #21, head bac4fbe0ee18ecfb6f18ca3707185f23cac58f94 (= b19e437 + merge of origin/master f6c1f421; no tree change), base f6c1f421af6f183f8545739280852b245f05964a.

GitHub-side writer inventory (gh api, ~10:55Z):
- Workflows: one, `CI` (.github/workflows/ci.yml, active). Triggers: push to master; pull_request to master with default types (opened/synchronize/reopened — ready_for_review is NOT a trigger, so the gate's draft→ready transition starts no candidate run). No schedule, no workflow_dispatch.
- Dependabot/Renovate: no config (.github has only workflows/).
- Auto-merge: repo allow_auto_merge=false; PR autoMergeRequest=null. Merge queue / branch protection: protection API 403 (private repo on free plan — feature unavailable); rulesets: {"message":"Upgrade to GitHub Pro or make this repository public to enable this feature.","documentation_url":"https://d.
- External CI / App publishers: commit statuses on candidate head = 0; check runs = only `cpu` (github-actions).
- Local writers: see step1 (none for this repo besides MAESTRO).

Reservation: MAESTRO9 holds the window from candidate push (~10:52Z) until the gate returns. During it: no commits/pushes by MAESTRO (receipts are committed after the merge), Codex builders codexmb14/codexmb15 run under briefs forbidding commit/push/merge, no CI reruns requested. Merge-generated master-push CI stays enabled (ci.yml push trigger untouched).
Drain: the only candidate-head run is 38043913838 (pull_request, bac4fbe); the gate is invoked only after it completes successfully.
