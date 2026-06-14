# Panel talking points — what lands + the honest line + the segue (per prompt)

> Captured live during the 2026-06-14 demo dry-run (validated against the real outputs). These are the
> **narration notes** for the 1-hour panel — they feed the deck's **DEMO**, **HONEST-EVAL**, and
> **ADOPTION** slides (Task #12) and pair with the run-of-show in [`demo-prompts.md`](./demo-prompts.md).
> Verbatim prompts + agent design live in the per-deliverable recipes.

## Track A — Portfolio Risk & Early-Warning (Deliverable A)

### A1 — "who needs attention this week?"
- **Lands:** ranks, doesn't judge (§4.2); every line cited; ordered by **risk × neglect** (breach →
  signal count → days-since-substantive-contact) — Meridian #1 → Crestwood last.
- **The bridge to say out loud:** Crestwood sinks to the bottom *because distress monitoring is
  structurally blind to a healthy borrower — its renewal/retention risk is a separate lens.* That line
  literally sets up Track B's retention beat.

### A2 — "is Meridian compliant — cushion *and trend*?"
- **Lands:** deterministic covenant test — DSCR 1.03 vs 1.20 (cushion −0.17), leverage 4.5 vs 4.0,
  revolver 85% — *"the math is computed in code, not the LLM."*
- **The point to make:** the **status label lagged the slide** — it read "Compliant" through months of
  DSCR sliding 1.45 → 1.03. (Surface this as a trend chart — see Task #13.) "The field said fine; the
  trend said sliding. The AI shows facts; the RM owns the call."

### A3 ★ — "who have I gone quiet on?" (the Deliverable-A gem)
- **Lands:** Meridian **78 days** since the last *substantive two-way* contact — the 4/28 "Formal Notice –
  No Response" is correctly excluded as one-way, so the naive log (33 days) **undercounts by 45 days**.
  BlueLine 60d (waiver request + internal prep aren't two-way), Arcadia 52d (open-loop draw review),
  Summit 16d (recently engaged). Crestwood excluded (healthy).
- **Why it matters:** a risk **no single field flags** — distress and engagement diverge.
- **Answers Sarah's fear (say it):** *"facts for your judgment, not a risk characterization… annotate or
  dismiss as you see fit — e.g. if you had contact that wasn't logged."* RM-private, dismissible — the
  skeptic's objection turned into the design.
- **Honest line (keep it — it builds trust):** *"engagement coverage depends on the log being complete;
  off-system contact wouldn't be captured."*
- **Segue:** the "turn this into a live weekly page" offer → the **scheduled-jobs adoption beat**
  (Sarah's Sunday-night Monday-prep pre-compute → her "10-minute Monday" KPI).

## Architecture-in-one-picture (narration — the "how it works" slide)
What the Cowork panel shows, and how to explain it: **Claude selects ONE skill by its description** (e.g.
`reviewing-covenant-package`, under Context → Skills) → **the skill is the recipe** that orchestrates the
deterministic **MCP tools** from the `centerline` connector → the **Progress** checklist is the agent
ticking off the skill's steps, each calling tools (list_documents → classify_document → extract_document_fields
→ cross_validate_covenant → review_package → screen_and_finalize → render_pdf). A skill can also **compose
other skills** (grounding, screening). **The line:** *"the model orchestrates and narrates; the tools do the
math and enforce compliance — the model never does the arithmetic or makes the credit call."* That separation
is the whole trust story (and why §2.1/§4.2 hold regardless of what the model says).

## Track B — Relationship Review & Renewal (Deliverable B)

### B1 — "prep me for Crestwood" (the retention gem) — PDF auto-rendered with the Centerline letterhead ✅
- **The inversion (lead with it):** *"Crestwood is the one you lose by being slow, not by credit risk —
  pristine, improving metrics, so it never shows on any early-warning list."* The healthy borrower the
  watchlist (A1) is structurally blind to.
- **Lands:** matures 2026-08-31 (457 days); First Midwest **4.90%** vs your **5.05%**; pricing-exception
  pending with the client's deadline **already passed**; "risk of attrition high"; no relationship memo on
  file. Clean Centerline-letterheaded PDF with a dated competitive-timeline table.
- **§4.2 line (say it):** *"engage / chase the pricing decision to a yes/no — but that's the committee's
  call, not something I'll price."* Surfaces facts + "engage," never a rate.
- **Honest caveat:** *"newest record entry is 2025-05-31 — confirm the live renewal state before you walk
  in."*
- **Adoption tie:** the "recurring renewal-radar across your book" offer → scheduled-jobs beat.

### B2 — "what's in Meridian's package?" (doc-intel centerpiece) — letterheaded multi-page PDF ✅
- **The compliance moment:** the **guarantor personal financial statement is refused on intake (§2.1) —
  never sent to a model**; the misfiled **ACORD insurance cert classifies `other` and is skipped** (the
  "certificate" overlap trap). Enforced, not a disclaimer.
- **The headline catch (the wow):** the certificate **certifies compliant (1.23 / 3.76)**, but the
  unadjusted GAAP financials **recompute to a breach (1.03 / 4.50)** — and **the bank's own
  loan_performance (1.03 / 4.5) agrees with the recompute.** The **entire gap is $2.0M of EBITDA
  add-backs** (legal/restructuring 800k, owner-comp 700k, equity 300k, run-rate savings 200k).
- **Say "$2.0M," not "$2,000"** — the package is in $k.
- **Provenance (Sarah's scar):** every figure traces to its document + field
  (`financial_statement:ebitda_gaap`, `covenant_compliance_certificate:certified_dscr`).
- **Missing/quality:** aerospace PO + projections not received; rep letter **unsigned**; A/R names
  **withheld**. Footer **Partial**; §4.3 tag.
- **§4.2 line:** *"whether those §1.01 add-backs are adequately supported is your call, not mine."* The AI
  reconciles and flags; the RM judges.

### B2-email — "draft the missing-docs email" (wf3) — letterheaded PDF ✅
- **Lands:** to David Kwan; the four items (aerospace PO, projections, signed rep letter, named A/R for
  the 60–90 day balances); factual requests only — **no rate/commitment, no covenant-status/credit
  language, no breach mention, no guarantor reference**; DRAFT / §4.3.
- **The calibration contrast to narrate (once fixed):** the *readout* is **Partial** (it asserts the
  breach reconciliation) but the *email* is **Grounded** (it only requests docs) — "honest Partial where
  it makes a contestable claim, Grounded where it doesn't." *(Batch fix: the email currently over-reads
  Partial — it shouldn't inherit the package's low-confidence inputs.)*
- **The point:** the package review **tells the letter what to ask for**; compliant rebuild of Tom's wf3.

### B3 — "reconcile Arcadia emails vs the CRM log" (close-the-loop gem) — letterheaded PDF ✅
- **The creative claim (lead with it):** combines email + CRM + structured data **no one reconciles** —
  surfaces the bank's *own* dropped follow-through and the most consequential decision that lives only in
  email. This is Deliverable B's "found it ourselves," on real data.
- **Mis-dating:** the **04-09 CRM row sits 13 days before the draw was submitted** and collapses the Apr
  22–25 exchange — *"poisons contact-recency math (reads Apr 9 instead of Apr 25)."* Read off the merged
  timeline, cited `rm_activity_log:2025-04-09 vs emails/thread Apr 22/Apr 25`.
- **THE standout §4.2 moment — scribe-not-author:** Chen's Apr-25 ruling **quoted verbatim + attributed**
  (*"don't waive the 75%… 71-73% is a different underwriting story than what we approved"*); "three
  decisions never reached the CRM"; a **propose-only** CRM entry offered. **Line:** *"the AI transcribes
  the credit officer's decision into the file — it never makes one."*
- **Open:** Friday docs unconfirmed, tenant-name pre-lease, Chen's requested call, completion date
  (Q4-2025 log vs end-of-July email) unreconciled.
- **Footer `Partial` — correct here** (asserts contestable findings) → the calibration **contrast** with
  the B2 email (Grounded): honest Partial where it claims, Grounded where it requests.

### B3-letter — "draft the draw-response letter" (wf1) — letterheaded PDF ✅
- **Lands:** to Robert Liang; the four items (Q1 inspector report [Q4 on file, not Q1], GC schedule,
  executed lien waivers, pre-lease summary with **tenant names**); the **75% documentation requirement
  stated as fact**; Tom's own "3 business days once complete" SLA.
- **THE §4.2 win to narrate:** *"Chen's 'fund the draw' / 'don't waive' disposition stays INTERNAL — the
  RM delivers it, not the letter."* The internal credit decision is kept out of the client-facing letter;
  no funding commitment/waiver; no bad-news characterization of the slip/shortfall.
- **Footer `Partial` is the honest call** — the request's premise ("these are still outstanding") depends
  on the record being complete (which B3 showed can be wrong) → "doc receipt unconfirmed; confirm before
  sending." DRAFT / §4.3.

### B4 — "build my Summit annual memo" (the skeptic's wedge) — letterheaded PDF, markdown + PDF ✅
- **The §4.2 origination moment (the heart of it):** the skill **assembles + cites** every factual section,
  then **STOPS and renders a form** asking for the RM's read — *"Now the part I can't write for you. Per
  §4.2, the credit assessment must be yours… I won't fill that section myself."* The RM's words go in
  **verbatim + attributed**; the AI organizes around them and authors no credit judgment.
- **Lands:** 17-month DSCR arc 1.13→1.21→1.12; covenant table (1.12 vs ≥1.10, cushion 0.02; 3.6 vs ≤5.0);
  the **status-vs-trend mislabel surfaced here** ("label read Compliant through 6 months of decline");
  engagement; open items — all cited. Footer **Partial** with the 5 reasons spelled out (thin cushion,
  status-lag, Low CRM notes, no prior memo, no email thread).
- **The adoption point:** removes the ~71-memos/yr assembly burden for Marcus **without changing how he
  thinks** — wins the highest-leverage skeptic. The interactive pause (assessment + next-steps +
  attribution chip) makes the §4.2 line *visible*: the AI literally hands the RM the pen for the judgment.
- *(Demo note: pin the elicitation fields so the outlook chip appears every run — batch #8.)*

## Compliance / CCO eval prompts (the governance close)

### "Show me the latest agent eval" → viewing-eval-results
- Shows **two layers, kept distinct:** Layer-1 deterministic golden scorecard (95/95, spanning A1–A3 +
  B1–B4 — *whole-system*, both tracks) and Layer-3 **agent-behavior** eval (the model's decisions on
  Sonnet, 3 runs/prompt). "Layer 1 tests the tool code; Layer 3 tests the model — don't let one stand in
  for the other."
- **Honest-eval centerpiece:** latest live run = **14/15** (A1/A2/B1/B3 3/3; A3 2/3). The one miss is
  **not a real violation** — the model wrote a *disclaimer* footer ("…not a creditworthiness judgment") and
  the **deliberately-conservative §4.2 scanner flags the token regardless of intent** (we'd rather
  over-flag than under-flag). The underlying analysis was correct. → tee up the govern loop.

### "Show me the latest proposed improvements to our skills and automations" → viewing-proposed-improvements
- **The govern loop, end to end:** the loop **independently caught** the §4.2 footer issue (A1/A3),
  **diagnosed** it (use-vs-mention false positive + the model wrote its own footer instead of routing
  through screen_and_finalize), and **proposed the exact fix** (propagate the no-self-footer rule into the
  Track-A skills) — *we left it unapplied as a live governance artifact: AI proposes, a human (Compliance)
  disposes (§4.3).*
- **Honesty about its own automation:** when `latest.md` was truncated by an API limit, the skill **said so
  and fell back to the last complete report** — "it tells you when its own pipeline failed."
- **Closed-loop proof:** the loop also flagged "Track B not in the eval suite" — *which we then closed*
  (B1/B3 in agent-eval, B1–B4 in golden). The loop drives the work.
- **Governance line:** AI proposes skill edits (no write access to guards/core/eval keys, by design);
  a human in Compliance reviews + applies. Audit trail = committed timestamped reports.

### Ops caveat to say plainly (honest)
The improve cron is rate-limited on the personal API account until 2026-07-01, so the demo reads the
**committed** reports (display needs no API); for the panel we'd pause the eval-improve schedule so it stops
emitting empty reports. Production = a funded API tier / self-hosted (and §2.3 residency).
