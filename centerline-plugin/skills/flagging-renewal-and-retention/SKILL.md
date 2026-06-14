---
name: flagging-renewal-and-retention
description: Use to prep an RM for a healthy, valuable borrower — or to answer "who am I about to lose?" Surfaces the maturity clock, the health/trend, a competing offer, and relationship value, and flags that the RM should engage proactively. The inverse of the early-warning watchlist (which is blind to healthy clients). Facts only; never recommends a rate or price.
---

# Flagging renewal & retention

Early-warning watches the *sick* credits. But the borrower you actually **lose** is the **healthy** one a
competitor is courting while the renewal drifts — and distress monitoring is structurally blind to it
(0 signals → bottom of the watchlist). This skill is that missing lens. Everything it surfaces is a
**fact (§4.2)**; it flags *that* the RM should engage — it **never** recommends a rate or price (the
pricing committee owns that), and it never characterizes creditworthiness.

## Steps

1. **Run the radar.** Call the `centerline` MCP tool **`flag_renewal_and_retention(borrower)`** (deterministic,
   server-side). It returns: `retention_attention` (fires or not) + `reasons`; the **maturity clock**
   (`days_to_maturity`); the **health** (compliant + deterioration-signal count + DSCR trend — it reuses
   `check_covenant_compliance` / `detect_deterioration_signals`); the **relationship** (tier, facility
   size, relationship-since, primary contact); the **competitive signal** + **attrition** flags; and the
   dated **renewal_signals** it found in the record.

2. **For a meeting prep, add context.** Compose with `building-client-360` (the dossier) and, if useful,
   `get_relationship_timeline` (to show how the renewal actually unfolded). Cite every fact
   (`grounding-claims-to-source`).

3. **Frame it as engage-not-price.** State the facts and the recommendation to **engage / prioritize the
   renewal** — e.g. *"Growth-tier relationship, pristine and improving, matures 2026-08-31; a competing
   term sheet has been on record since February and the renewal is stalling; attrition risk is noted. →
   Prioritize closing the renewal this week."* Do **not** propose a rate, a match, or an approval — surface
   that a pricing decision is owed and route it to the RM / pricing committee.

4. **Screen + render.** Route the readout through **`screen_and_finalize`** (pass anything stale/unresolved
   as `low_confidence_inputs`), then `render_pdf` for a fileable copy; keep the markdown inline. Tag for RM
   review (§4.3). Automated alerting on this signal needs **CCO approval (§4.1)** before it runs unattended.

## The honest point (say it)
This is the **"flag ≠ action"** lesson made concrete: Tom's own weekly summary flagged the Crestwood gap
and he *still* nearly lost it (vague reply → missed call → slow proposal → pricing in limbo). The radar
surfaces it **earlier** and makes the next step obvious — but the value only lands if the RM acts, so the
deployment must make engaging frictionless and avoid alert fatigue.
