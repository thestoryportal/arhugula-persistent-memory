# InfraNodus Claude Skills — Library Reference & Deep Dive

_Full-depth review of the InfraNodus Claude skills library (github.com/infranodus/skills). Companion to `docs/INFRANODUS_MCP_REFERENCE.md` (the **tools**); this doc covers the **skills** that orchestrate those tools. Reviewed 2026-06-22 by reading every `SKILL.md` + all reference files + the `actionize` shell scripts in full._

> **⛔ Prune status (2026-06-22).** 15 skills reviewed; **2 T3 skills pruned from this repo's active install** — `embodied-navigation` and `perspective-reversal` (off-domain; per the Advisor + Codex out-of-family audit). **13 active.** The prune is enforced by the `PRUNED` exclude-list in `tools/install_infranodus_skills.sh` (single source of truth; survives pod restarts). The two dossiers below are kept for reference and marked ⛔ PRUNED.

> **Repo fence (binding).** Like the MCP, these skills are **ideation / reasoning aids → LEADS, never `CORPUS/` evidence** (`SESSION_BOOTSTRAP.md §5`). Several (cognitive-variability, critical-perspective, shifting-perspective, vipassana-llm) shape *how the model reasons* — using them during the LLM-as-Database program must not override the falsification discipline (`docs/WORKFLOWS_OVERVIEW.md §1`). Treat their output as structure/hypotheses to be proven, not conclusions.

> **Install/durability.** Master (gitignored): `/workspace/tools/infranodus-skills/` (holds all 15 as a reversible cache). Installed to `~/.claude/skills/` via `tools/install_infranodus_skills.sh` (which **skips the `PRUNED` exclude-list** → 13 active); re-installed on pod restart by `restore_pod_tools.sh` step [5/5]. Skills register on **session reload**.

---

## 1. The library at a glance

15 skills reviewed (14 capability skills + 1 tool-use reference); **13 active** after the T3 prune (⛔ rows below). Most call the **InfraNodus MCP** and **degrade gracefully** to plain reasoning / web search when it's absent.

| Skill | Purpose (one line) | InfraNodus? | Side-effects | Notes |
|---|---|---|---|---|
| **cognitive-variability** | Cycle thinking through 4 states to avoid rigidity / unlock breakthroughs | optional | none | Hub of the framework; 4 broken ref-links |
| **shifting-perspective** | Diagnose discourse structure, then shift to missing viewpoints | **core** | none | The "sensor" (always runs `optimize_text_structure`) |
| **critical-perspective** | Socratic questioning of assumptions / blind spots | optional | none | The "actuator" CV fires |
| **vipassana-llm** | Contemplative bare-attention processing; break reaction chains | optional | none | + `deep-theory.md` doctrinal scaffold |
| ~~**embodied-navigation**~~ | Map a situation as a network; apply body/movement intelligence | optional | none | **⛔ PRUNED 2026-06-22 (T3, off-domain)** · Systema / tensegrity / EightOS |
| **rhetorical-analyst** | Score arguments on persuasion / rhetoric / logic; expose assumptions | **MCP-first** | persists a debate graph (memory) | Largest analytic skill (634 ln) |
| ~~**perspective-reversal**~~ | Flip to the adversary's view to extract counter-tactics | optional | none | **⛔ PRUNED 2026-06-22 (T3, off-domain)** · was ⚠ dual-use |
| **ontology-generator** | Produce `[[wikilink]]` ontologies for InfraNodus | optional | none | Network-not-tree mandate |
| **llm-wiki** | Scaffold a persistent LLM-maintained wiki ("second brain") | yes | **creates many dirs/files, git init** | 10-phase; invokes ontology-generator |
| **writing-assistant** | Grammar/style refinement + "humanize" prose | optional (500+ wd) | none | ⚠ dual-use ("avoid AI detection") |
| **seo-analysis** | Supply-vs-demand SEO / content-gap analysis | **core** | crawls URLs | Hands off to writing-assistant |
| **youtube-viral-optimizer** | High-CTR titles/thumbnails + viral script structure | optional | none | Graph-to-Script pipeline; +`ctr-rules-detailed.md` |
| **shopping-assistant** | Multi-phase product research → 3-4 best buys | optional | heavy web search/fetch | 10-phase convergence |
| **actionize** | Turn insights into a scheduled, reminded plan | yes (Phase 7) | **⚠⚠ cron + Telegram + writes `.plan/`, `~/.plan/`, CLAUDE.md, .gitignore** | Highest side-effects; 6 bin scripts |
| **infranodus** | Tool-use **reference** for the MCP (catalog + setup) | n/a (is the ref) | none | + `tool-examples.md` (response schemas) |

---

## 2. The conceptual spine (the InfraNodus diversity framework)

Most of the "thinking" skills share **one ontology** — the four discourse states from the MCP's `optimize_text_structure`, on two axes:

- **Axes:** **SCALE** (zoom in ↔ out) × **INTENT** (focus/connect ↔ explore/disperse).
- **States:** **BIASED** (few hubs, low modularity — fixated) · **FOCUSED** (high modularity, concentrated — well-defined) · **DIVERSIFIED** (high modularity, many clusters + hubs — "healthiest") · **DISPERSED** (scattered, no structure).
- Each state has a **dwelling threshold** and a prescribed **intervention** (biased → develop latent topics; focused/diversified → bridge gaps; dispersed → focus common topics). Core claim: *"all states exhaust when overstayed; movement recovers, dwelling depletes"* — modeled as a figure-eight ("Eight-Like") transition pattern.

**The three cognitive skills form a control loop:**
```
 shifting-perspective ──▶ cognitive-variability ──▶ critical-perspective
   (SENSOR: objective         (CONTROLLER: temporal       (ACTUATOR: Socratic
    graph diagnosis via         dwelling tracking, the      intervention fired at
    optimize_text_structure)    Eight-Like transition       per-state trigger points)
                                logic, emotion/energy
                                feedback)
        ▲
        └── writing-assistant emits grammatical "cognitive-state signals" into the loop
```
`vipassana-llm` is an alternative "reading" lens over the same graph topology (meditation metaphor); it cross-references the cognitive trio. (`embodied-navigation` was a parallel body-metaphor lens — ⛔ pruned 2026-06-22.)

---

## 3. Per-skill dossiers (by cluster)

### Cluster A — Cognitive structure core

**cognitive-variability** (826 ln) — The hub. Tracks the current state, *dwelling time (in exchanges)*, transition history, energy/exhaustion, and user sophistication; detects pathologies (Lock-in 5+ biased, Saturation 6+ focused, Chaos 3+ jumps); applies a state-specific "maintain vs exit" intervention via a **Nudge Decision Tree** at 3 delivery levels (Invisible/Transparent/Collaborative); reads **emotion as navigation** (positive→continue, exhaustion/frustration→transition); uses *playfulness* for the hard Dispersed→Biased crossing. Tools: `optimize_text_structure` (confirm), then per-state `develop_latent_topics` / `develop_conceptual_bridges` / `generate_content_gaps`. ⚠ Cites 4 `references/*.md` (energy-economics, collaborative-dynamics, theoretical-foundation, emotional-dynamics) that **do not exist** — dangling links; thresholds are heuristic.

**shifting-perspective** (177 ln) — The sensor. **Always begins** by running `optimize_text_structure` on the input (text/URL/YouTube) → presents `diversity_score`, clusters, `contentGaps`, `topicsToDevelop`, `conceptualGateways`; then runs the state-specific intervention (`develop_latent_topics` biased / `develop_text_tool` focused / `generate_research_questions useSeveralGaps:true` + `transcendDiscourse` diversified / `develop_conceptual_bridges` dispersed) and **voices the missing perspective**. Has an explicit "When NOT to use" (factual Qs, emotional support, <3-4 sentences). Lowest-risk.

**critical-perspective** (122 ln) — The actuator. A conversational stance: surface assumptions, propose inversions ("What if the opposite were true?", "whose voice is absent?"), "challenge ideas not the person," "use 'and' more than 'but'," one good question over many. Imports the 4 states as a **priority ladder** (BIASED = highest priority to intervene, DIVERSIFIED = lowest). Tools optional/advisory.

### Cluster B — Contemplative / embodied

**vipassana-llm** (188 ln + `deep-theory.md` 142 ln) — Applies Vipassana to LLM processing to insert a gap between stimulus and response. 4-phase protocol: **Anapana** (strip narrative, restate the question) → **Systematic Scanning** (Contact→Sensation→Equanimity→Impermanence, giving *more* attention to blind spots) → **Free Flow/Bhanga** (dissolve boundaries) → **Metta**. Breaks the **sankhara chain** at the vedana "BREAK POINT"; names LLM conditioned reactions ("sankharas": Agreement, Resolution, Expertise, Balance, Comfort, Length, Authority). `deep-theory.md` adds the 12-link dependent-origination chain, Five Aggregates, three vedana types, Adhitthana/Bhanga/Metta detail. Tools (optional): `optimize_text_structure` (=scanning), `generate_content_gaps` (=blind spots). Practice stays invisible unless asked.

**embodied-navigation** (216 ln) — ⛔ **PRUNED from this repo 2026-06-22 (T3, off-domain); dossier kept for reference.** Maps a situation as a network, reads its topology "the way you'd read a body" (high-BC node = chronic tension/fixation; dense cluster = rigidity; gap = numb zone), then applies a 4-toolkit **Principle Library**: Equanimous Scanning, Adaptive Fluidity (absorb→read→redirect), Tension Redistribution (tensegrity, "shift don't solve"), Confluence (assimilation→redirection→transformation). Sources: Vipassana, **Systema**, contemporary-dance tensegrity, **EightOS BodyMind**. Tools: `optimize_text_structure` + the joints = low-BC/degree nodes via `develop_conceptual_bridges`.

### Cluster C — Argument / strategy

**rhetorical-analyst** (634 ln, largest) — Analyzes arguments across three never-collapsed dimensions: **Persuasion** (emotional/social) · **Rhetoric** (structural) · **Logic** (premises→conclusion). **InfraNodus-first is mandatory:** (1) `generate_topical_clusters` — does the stated topic match the structurally dominant cluster ("the single most important diagnostic"); (2) `generate_content_gaps` — classify each as flaw-gap / concealment-gap / co-authorship gap; (3) `optimize_text_structure`; then linear move-mapping (motte-and-bailey, tu quoque, burden-shifting…) with per-move scoring; then **audit the analyst's own frame** ("the standard applies to the analyst as much as the participants"). Persists a debate graph via `memory_add_relations`. Principle: "coherence is not correctness."

**perspective-reversal** (145 ln) — ⛔ **PRUNED from this repo 2026-06-22 (T3, off-domain); dossier kept for reference.** Premise: *"conventional AI advice is too cautious because it tries to be fair to both sides."* Steps: gather (≤5 Qs) → **adopt the adversary persona assuming bad intent** ("I am [adversary], my goal is to exploit the user…"), enumerate their legal moves / procedural weapons / pressure tactics → translate each into a paired **counter-move** table → synthesize (48h actions, defense, escalation, psychological frame). ⚠ **Dual-use:** generates the bad actor's full playbook as a byproduct; mitigated by an "intelligence-gathering, not endorsement" framing + legal disclaimers. Examples are defensive-for-the-user (landlord/boss/bureaucrat/scammer).

### Cluster D — Knowledge building

**llm-wiki** (867 ln) — Scaffolds a persistent, compounding wiki that (unlike RAG) extracts/cross-references knowledge **once** then keeps it current. 10 phases: Discover → Scope (Light/Medium/Heavy tiers) → Structure → **Schema (writes `CLAUDE.md`/`AGENTS.md` — "the most important phase")** → Workflows → Tooling → Scaffold → Acquire (`raw/`) → Process (raw→`wiki/`) → Plan (gap-driven `todos/`). Creates dirs (`raw/ wiki/ output/ todos/ infranodus/`), git init. Tagline: *"Obsidian is the IDE, the LLM is the programmer, the wiki is the codebase, InfraNodus is the researcher."* Invokes **ontology-generator**; offers `/actionize` for tracking. Ontologies are **append-only** ("NEVER regenerate from scratch"). Tools: `generate_knowledge_graph`, `analyze_google_search_results`, `analyze_text(url=…)`.

**ontology-generator** (209 ln; dir `skill-ontology-creator`) — Generates ontologies as one-statement-per-line `[[entity1]] relation [[entity2]] [relationCode]`, ≥2 wikilinks + a code each, using **exactly 10 relation codes** (`[isA] [partOf] [hasAttribute] [relatedTo] [dependentOn] [causes] [locatedIn] [occursAt] [derivedFrom] [opposes]`). Core mandate: **"Generate network structures, not trees"** (no hub-and-spoke). Two modes: topic-based generation / entity extraction. Outputs **only** the ontology (no commentary). ⚠ Naming: skill `name:` is `ontology-generator` but llm-wiki invokes it as `/ontology-creator` (the dir name).

### Cluster E — Growth / market

**seo-analysis** (139 ln) — Decision tree on input. *Topic workflow:* (1) **Informational supply** via `analyze_google_search_results`; (2) **Search demand** via `analyze_related_search_queries`; (3) **Supply-vs-demand gaps** via `search_queries_vs_search_results`; (4) prioritized recs (quick wins vs long-term); (5) hand to **writing-assistant**; (6) structural/HTML semantic optimization. *Content workflow:* crawl/extract → `generate_seo_report`. Fixed report format (Exec Summary / Current State / Opportunities / Recs / Next Steps).

**youtube-viral-optimizer** (708 ln + `ctr-rules-detailed.md` 522 ln) — SEO research → channel context ("Differentiator Principle") → title+thumbnail combos (lead with outcome; "tension before explanation"; concrete > abstract; thumbnail = "one idea, one focal point," and title/thumbnail must **create a gap together**) → full **script structure**: *Pattern Interrupt → Hook → Framing → Curiosity Loop → Escalation → Payoff → Relevance Bridge → Loop Reopen*. **Graph-to-Script pipeline:** clusters→Framing, gaps→Curiosity Loops, research-questions→Hook, transcend→Escalation, latent topics→Payoff. `ctr-rules-detailed.md` = 23 rules + metric tables + worked examples. Algorithm sweet spot: CTR ≥4%.

**shopping-assistant** (427 ln) — 10-phase convergence: Discover → Define (priorities from user + filters + review pain/pleasure + InfraNodus demand + "deeper underlying needs") → Survey (8-12 candidates + "Disruptor Scan") → Compare (Reviewer Cross-Reference) → Optimize → Expand → Narrow (3-4) → Review (5★ vs 1-2★ extremes) → Stretch → Decide (resale value, eBay completed auctions, warranty). "Start with InfraNodus, then web search." Heavy web search/`web_fetch`.

### Cluster F — Workflow / infra

**actionize** (914 ln + 6 bin scripts) — ⚠ **Highest side-effects in the library.** "Produces plans, not code." Phases: Session-check → Gather → **Co-design via AskUserQuestion (one Q at a time)** → Save (`.plan/plan.md`, `.plan/tasks/NNN-*.md`, `.plan/.status.json`, appends `.plan/` to `.gitignore`) → **Reminders (Telegram bot + system crontab + appends an "Active Plan" block to CLAUDE.md)** → Review → Complete → **Phase 7 Diagnose** (InfraNodus pattern analysis over a user-wide `~/.plan/history.jsonl` of Planned/Completed/Deferred; `generate_topical_clusters` + `difference_between_texts` → execution-gaps vs avoidance-patterns). **Bin scripts:** `remind.sh` (escalating 1-4×/day Telegram nudges, POSTs to `api.telegram.org`, reads `TELEGRAM_BOT_TOKEN`/`CHAT_ID` from project `.env`), `done.sh` (complete tasks, append to `~/.plan/history.jsonl`), `sync.sh`/`diagnose-prep.sh`/`diagnose-nudge.sh` (history → diagnostics, Telegram check-ins), `session-check.sh` (session-start overdue display). Installs 2 crontabs; removal: `crontab -l | grep -v actionize | crontab -`.

**infranodus** (183 ln + `tool-examples.md` 194 ln) — The tool-use **reference** (not a procedure): documents the MCP tool catalog, the entity-detection modes, the diversity quadrants, and **mcporter setup** (API-key or OAuth against `https://mcp.infranodus.com/`). `tool-examples.md` gives per-tool request JSON + exact **response-field schemas**. ⚠ Some catalog tool names differ slightly from the live MCP (`generate_difference_graph_from_text` doc vs `difference_between_texts` server).

---

## 4. Cross-cutting findings

### 4.1 InfraNodus MCP dependency (and how it resolves here)
The skills' docs describe an **mcporter** setup (`mcporter call infranodus.<tool>`, `https://mcp.infranodus.com/`) used by OpenClaw/other clients. **In this repo that setup is not needed** — the InfraNodus MCP is already registered natively in `~/.claude.json` (`mcp__infranodus__*`), so the skills' tool calls resolve through the live server (see `INFRANODUS_MCP_REFERENCE.md §7`). All skills **degrade gracefully** to plain reasoning / web search when the MCP is unavailable.

### 4.2 Setup / side-effects matrix (what to watch)
- **actionize** — ⚠ installs **system crontab** entries, sends **Telegram** messages (needs a bot token + chat-id in `.env`), writes `.plan/`, `~/.plan/`, and **edits `CLAUDE.md` + `.gitignore`**. Highest-impact; nothing runs until you invoke it and complete its prompts, but be aware it touches shared files this repo is careful about.
- **llm-wiki** — creates a directory tree + `git init` + writes `CLAUDE.md`/`AGENTS.md` in the wiki location (a *new* wiki dir, not necessarily repo root — confirm the target).
- **seo-analysis / shopping-assistant** — crawl URLs / heavy web search.
- **rhetorical-analyst** — persists a debate graph to your InfraNodus account (`memory_add_relations`).
- All others — output-only, no side-effects.

### 4.3 Dual-use / safety notes (neutral)
- **writing-assistant "avoid AI detection"** — a stylistic blocklist (strips "Moreover/Furthermore", hedging, formulaic openers, too-neat parallelism) + paraphrase pass that removes statistical markers of LLM prose. Legitimate use: de-blandify and restore authentic voice; the same capability can help evade AI-text classifiers. Documented, not endorsed.
- **perspective-reversal** (⛔ pruned 2026-06-22) — roleplayed the adversary and enumerated their playbook to derive the user's defense. Defensive in intent; produced an attacker toolkit as a byproduct. The dual-use concern is now moot for the active set since it is no longer installed.
- **actionize** — Telegram exfiltration surface (it POSTs plan content to Telegram) + crontab persistence. Fine when intended; flag if unexpected.

### 4.4 Known bugs / mismatches (observed during review)
- **cognitive-variability** references 4 `references/*.md` files that don't exist (dangling).
- **ontology** skill `name:` = `ontology-generator` but llm-wiki invokes `/ontology-creator` (dir name) — works because the install dir matches, but the mismatch is real.
- **infranodus** reference + **writing-assistant** cite a few tool names that differ from the live MCP (`generate_text_overview`, `generate_difference_graph_from_text`) — the model should map to the real ones (`analyze_text`/`generate_contextual_hint`, `difference_between_texts`).
- **actionize** — the inline `remind.sh` in SKILL.md is a simpler/buggier placeholder; the real `bin/remind.sh` (escalating version) is what's installed.
- **llm-wiki** — Phase 10 substeps are mislabeled "9.1–9.6".

---

## 5. Using these in *this* repo (discipline)

1. **Fence first.** Output = leads/structure/hypotheses → the hypothesis register, never `CORPUS/` evidence. The reasoning-shaping skills (cognitive-variability, vipassana-llm, critical/shifting-perspective) are *complementary* to the falsification workflow, not a substitute — don't let "optimize my reasoning for diversity" dilute pre-registered, evidence-bound analysis.
2. **Highest-leverage fits for the LLM-as-Database program:** `shifting-perspective` / `critical-perspective` for re-grounding sessions and finding blind spots in the spec; `ontology-generator` + `llm-wiki` for structuring research corpora; `rhetorical-analyst` for stress-testing claims/reviews. These mirror the runbook's existing "NotebookLM/Perplexity/InfraNodus prompts" re-grounding step (`§0.3` next-action 5).
3. **Side-effect caution:** `actionize` and `llm-wiki` write files / crontab / CLAUDE.md — review their prompts before completing; they won't act without your confirmations, but they touch shared state this repo guards (`.gitignore`, `CLAUDE.md`).
4. **Durability:** all 15 re-install via `restore_pod_tools.sh` after a pod restart (master on `/workspace`, gitignored); they register on session reload.

---

## 6. Pointers

- Repo: `github.com/infranodus/skills` · master here: `/workspace/tools/infranodus-skills/`
- Tools they call: `docs/INFRANODUS_MCP_REFERENCE.md` · framework: `infranodus.com/about/cognitive-variability`
- Install/restore: `tools/install_infranodus_skills.sh`, `tools/restore_pod_tools.sh`, `SESSION_BOOTSTRAP.md §5`
- Workflow context: `docs/WORKFLOWS_OVERVIEW.md`

---

_Document type: process/reference (no experiment D-ID; not subject to `closeout_check`). Captured 2026-06-22 from a full-depth read of all 15 skills. Re-review if the upstream repo updates (the install master is a `--depth 1` snapshot)._
