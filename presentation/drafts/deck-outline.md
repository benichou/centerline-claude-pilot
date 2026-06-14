# Centerline Bank — Claude Pilot · Panel Deck OUTLINE (draft v1)

> **Status:** brainstorm/outline for refinement (Task #12). Format decided: **Marp**, **presenter-spine** (sparse, visual slides talked over live) + **rich speaker notes** (`speaker-notes.md`) — narration & Q&A are graded, so the notes are the main writing effort.
> **Cover line (required):** *Claude Pilot — technical-challenge presentation · **Senior Forward Deployed Engineer (candidate)** · **Caylent**.*
> **Two dates, kept distinct:** the **cover/presentation date is June 2026** (when this is delivered to the Caylent panel). The **engagement scenario is set at the end of May 2025, as-of 2025-05-31** — the last row of loan-performance data (emails end Apr–May 2025; policy v1.2 eff. Feb 2025). Pinning the as-of to 2025-05-31 keeps every computed figure exact and verifiable: A3's 78-day contact gap and B1's 457-day maturity clock (2025-05-31 → 2026-08-31 = 457 days) are both measured from that date. In-scenario "this week" = the week of the 2025-05-31 data close, and the 90-day engagement starts then. *Only the cover carries June 2026; all narration inside the scenario is as-of end-May 2025.*

## The three through-lines — HELD, not chosen (the braid)
We do not pick one spine. Each owns a movement; all three are present throughout.
- **A — "shadow IT → compliant library"** = the **opening hook** (Part I). An RM already proved AI helps — by breaking policy. Keep the instinct, fix the violations, generalize it.
- **B — "the signal's already there, but the record can't be trusted → AI organizes the facts, the RM judges"** = the **spine through both demos** (Parts II–IV). Where §4.2 becomes a feature, not a constraint.
- **C — "adoption is the real risk → a portfolio, each tool earning a specific RM"** = the **close/landing** (Part V).

## Design rules (apply to EVERY demo + eval/adoption slide)
Each such slide's notes must answer, in this order:
1. **Why it matters / business impact** (in $/risk/time terms, grounded in the data).
2. **Which existing RM workflow it fits + what gap it fills** (so it's an upgrade to how they already work, not a new burden).
3. **The live orchestration exposed** — *skill selected → MCP tools fired → deterministic compute/guard → `screen_and_finalize` → `render_pdf`*. We literally show Claude picking a skill and the skill calling tools.
4. **Compliance line** (the §4.2 / §2.1 / §4.1 point made out loud).
5. **Honest caveat** (the hard-20% for this element).
6. **Segue** to the next beat.

The **"Architecture in one picture"** slide (S8) is the recurring lens — we point back to it on every demo.

---

## PART I — CONTEXT *(front-loaded; through-line A enters)*
1. **Cover** — Centerline Bank · Claude Pilot. Role/firm line. Presenter: Franck Benichou · **June 2026** (presentation date).
2. **Who I am / my mandate** — Senior FDE embedded for a 90-day engagement (**starting end-May 2025, as-of 2025-05-31**) to help **Rachel Torres (CCO)** complete the Claude pilot adoption across Commercial Banking. How I work: pair from minute one, narrate decisions, show what good looks like.
3. **The situation** — 3 RMs, **$350M**, **30–40%** of their time on docs/covenant-tracking/call-prep. Licenses procured, **nothing deployed**. The CCO's stated priority: early-warning (contact-gap + financial deterioration).
4. **The catalyst (A)** — Tom DeLuca's shadow ChatGPT workflows, surfaced by the IT audit; the **two compliance violations**. "Right instinct, wrong tools — our starting point, not our blueprint."
5. **The compliance reality** — §4 is trickier than it looks: **§4.2** (no creditworthiness language; disclaimers don't count) · **§2.1** (credit grade/watchlist as AI inputs) · **§5** (Special Assets/litigation) · **§4.1** (monitoring → CCO approval) · **§4.3** (human review). *This constraint shapes every design choice that follows.*
6. **The data & what it revealed (B enters)** — 8 files; signal scattered across structured + unstructured; **the record can't be trusted** (mis-dated logs, decisions only in email, status-label lags the trend). Three finds: Meridian *plan-not-executed* · Crestwood *attrition-while-healthy* · *engagement diverges from distress*.

## PART II — APPROACH *(the bridge)*
7. **How we built it** — composable **skill library** (not one mega-prompt) · **MCP tool-use** over copy-paste · **guardrails server-side** (designed-in, not tacked-on) · **Code build → Cowork = the RM's no-terminal surface**. The brief's "is single-prompt right?" answered: *the RM still types one prompt, but it now fires a multi-tool pipeline; only the memo (§4.2) and monitoring (§4.1) need a genuine extra human/governance step.*
8. **Architecture in one picture** — the diagram + the recurring lens: *Claude selects a skill (by its description) → the skill orchestrates deterministic MCP tools → math/guards run in code → output routed through `screen_and_finalize` → PDF → human review.* "The model orchestrates and narrates; the tools do the math and enforce compliance."
9. **Requirements scorecard** *(flip-to / Q&A safety net)* — brief-ask → what we delivered (2 solutions · exact prompts · real outputs · honest eval · multi-step · MCP · compliance-designed-in · creative non-obvious pick).

## PART III — TRACK A = Deliverable A *(A pays off; B runs through)*
10. **Track A intro** — fix Tom's **wf5** (weekly portfolio summary): what it was → what changed → architecture verdict. **Why:** the CCO's #1 priority, and the workflow IT flagged. **Fits:** replaces the Monday multi-system scramble.
11. **A1 — "who needs attention this week?"** — watchlist ranked by **risk × neglect**; ranks, doesn't judge (§4.2); every line cited. *Orchestration: `assembling-watchlist-triage` → `assemble_watchlist` (composes covenant + deterioration + engagement) → screen → PDF.*
12. **A2 — "is Meridian compliant — cushion *and* trend?"** — deterministic covenant math (DSCR 1.03 vs 1.20, etc.); status-label lagged the slide. *`checking-covenant-compliance` → `check_covenant_compliance` + `detect_deterioration_signals` → screen → PDF + trend chart.*
13. **A3 ★ — "who have I gone quiet on?"** — engagement coverage; Meridian **78 days** substantive silence (as of 2025-05-31; naive log undercounts by 45); a risk **no field flags**; answers Sarah's fear (RM-private, dismissible). → **close on "flag ≠ action"** (Tom flagged Crestwood and still lost it) → bridge to B.

## PART IV — TRACK B = Deliverable B *(our non-obvious find; B is the spine)*
14. **Track B intro** — the **creative claim** = close-the-loop + cross-source reconciliation + retention (a risk Tom didn't see, combining sources no one reconciles). The memo / doc-intake / email = the **compliant cleanup of Tom's other workflows**, explicitly *not* the creative claim. (Says out loud we read the brief's "avoid" list.)
15. **B1 — "prep me for Crestwood" (retention)** — the inversion: the one you lose by being *slow*, not by credit risk; healthy + maturity clock + competitor 4.90%. Facts + "engage," **never a rate**. *`flagging-renewal-and-retention` + `building-client-360` + `get_relationship_timeline`.*
16. **B2 — "what's in Meridian's package?" (doc-intel — the trust centerpiece)** — §2.1 guarantor refusal on intake · ACORD → `other`, skipped · certified 1.23/3.76 vs **recomputed 1.03/4.50** vs the bank's own figures · the **$2.0M add-back bridge** · **provenance footer** (`[tool · source]`) reads **Partial** honestly. *`reviewing-covenant-package`: list → classify → §2.1 prescreen → extract → cross_validate → review_package → ground → screen → PDF.* + missing-docs email (wf3).
17. **B3 — "reconcile Arcadia emails vs the CRM log" (scribe-not-author — THE §4.2 moment)** — mis-dated Apr-9 row poisons recency math; Chen's "don't waive 75%" ruling lives only in email, surfaced **verbatim + attributed**; propose-only CRM entry. *`detecting-cross-source-discrepancies` + `verifying-commitment-fulfillment` + `get_relationship_timeline`.* + draw-response letter (wf1).
18. **B4 — "build my Summit annual memo" (wins the skeptic)** — assembles + cites every factual section, then **STOPS and hands the RM the pen** for the credit assessment (attributed, verbatim). Removes ~71-memos/yr for Marcus without changing how he thinks. *`drafting-relationship-review-memos`: assemble → ⏸ elicit (assessment/outlook/next-steps/attribution) → draft around verbatim → screen → PDF.*

## PART V — TRUST · EVAL · ADOPTION *(B resolves on trust; C lands)*
19. **How we keep it trustworthy** — the eval system *is* the governance: **Layer-1** deterministic golden (95/95, both tracks) · **Layer-3** live agent-behavior eval (Sonnet headless, scans the model's own narration for §4.2) · **Layer-4** improvement loop (advisory) · **CI prod-gate**. Exposed as a workflow; **reported to the CCO across BOTH tracks.**
20. **Governance loop** — AI proposes skill edits (no write access to guards/core), a human in Compliance disposes (§4.3); audit trail = committed timestamped reports. The loop *independently caught* the A1/A3 §4.2 footer issue and we left it unapplied as a live artifact.
21. **Honest eval — the 80/20** — works: grounded/cited/compliant/reusable. Hard 20%: flag≠action · value gated by logging discipline (Marcus) · Track A blind to healthy/construction · doc-intel runs on **synthetic** (labeled) docs. *On-slide, owned.*
22. **Adoption per RM** — Sarah (trust scar → grounding + RM-private = the answer to her fear) · Tom (co-build; shadow→sanctioned) · Marcus (the memo is the wedge). **No single tool wins all three — a portfolio does.**
23. **Production & rollout** — Cowork = the RM surface (no UI to build) · §4.1 CCO fast-track for monitoring · §2.3 residency (local > cloud) · the scheduled-jobs beat (Sarah's "10-minute Monday"). What the next 90 days delivers.
24. **Close / the ask** — recap the braid: *the instinct was right (A) → we made it trustworthy (B) → and built it to be adopted, per RM (C).* → Q&A.

*(~24 slides; demos run live in Cowork between the intro/beat slides. Appendix candidates: full architecture diagram, the §2.1/§4.2 line-by-line, the data-findings detail, the reuse matrix.)*
