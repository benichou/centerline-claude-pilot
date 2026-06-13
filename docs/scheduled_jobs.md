# Scheduled jobs — turning the skills into recurring "prep" (adoption / deployment beat)

This is a **narrated adoption beat**, not a repo build. Claude Cowork ships a native **Scheduled** feature
("Schedule a recurring task — great for reminders, reports, regular check-ins"). It runs a prompt/skill on a
cadence in Cowork. We use it to turn the skills we built into a teammate that's **already done the morning prep**.

## Why it's *narrated*, not built (the build-vs-config line)
The **schedule definition** (cadence · folder · model · trigger) lives in the **Cowork account config** — it is
**not a git artifact**, so we don't (and can't) version it in this repo. What *is* versioned is the **skill /
prompt the schedule runs** — and we already have those. So scheduling is a **deploy-time configuration step**
we narrate; the repo supplies the skills it invokes.

## The compliance frame (this is the real value, not the feature)
A scheduled job here is deliberately **boring on purpose**:
- **Prepare-only — never auto-act (§4.3):** it *assembles* a digest / watchlist / draft into the RM's folder.
  It never sends to a client, writes the credit file, or escalates. A human reviews and acts.
- **§4.1 — CCO approval gate:** any *automated monitoring/alerting* needs CCO sign-off → we present it as
  "**designed, pending CCO approval**," with the CCO as the approver.
- **§2.3 — residency:** prefer **local** scheduled tasks (data stays on the bank's machine) over cloud
  Routines (which run in Anthropic's cloud). A rollout recommendation, not a blocker.

## Three concrete fits — one per persona

### Tom — schedule his wf5 (closes the shadow-workflow loop) ★
Tom's flagged shadow workflow wf5 was *itself* a recurring task — *"Every Monday morning I do this… ~15 min"* —
pasted into personal ChatGPT. The natural end state: **schedule the compliant rebuild** (Deliverable A's
deterministic watchlist) so his Monday summary is **pre-computed for him**, compliantly, with no manual paste.
The arc — **shadow recurring task → compliant rebuild → scheduled compliant pre-compute** — is the whole
adoption story in one line. Prepare-only; Tom reviews.

### Sarah — Sunday-night Monday-prep pre-compute
Sarah's own KPI is *"my Monday setup in 10 minutes instead of 45."* A **Sunday-night / early-Monday** scheduled
task runs `assemble_watchlist` + `measuring-engagement-coverage` + open-items and writes a **ready Monday
digest** to her folder. She opens Cowork Monday and the prep is done. → hits her stated success metric directly.

### CCO (Rachel) — weekly portfolio early-warning sweep
Her §7 priority is early-warning (contact-gap + deterioration). A **weekly scheduled sweep** writes a watchlist
report for her review. This is the **§4.1 governance example**: automated monitoring needs CCO approval, so it's
*"designed, pending her sign-off,"* and she's the approver — prepare-only, no auto-alert/act.

## The symmetry worth saying out loud
Just as **we** schedule the **eval-improve loop** (CI) to keep the *skill library* healthy, **the bank**
schedules a **CRM-hygiene / early-warning pre-compute** to keep the *RM's morning and the CCO's oversight*
current — the same "run on a cadence, prepare for a human, never auto-act" pattern at two levels.

## Honest caveat for a *live* demo
A scheduled Cowork task that calls our **bridged `centerline` MCP** inherits the surface caveats we documented
(the desktop bridge may not be present in a headless/cloud scheduled run; the production answer is a
hosted/remote connector). So **narrate scheduling as the deployment pattern**; for a live flourish, schedule a
**folder-only digest** (no dependency on the bridged MCP) so it reliably runs.

## One-line framing for the panel
> *"The workflows don't wait to be opened — a scheduled job has Sarah's Monday list and Tom's portfolio summary
> ready before they sit down, and a weekly early-warning sweep waiting for the CCO's review. Every scheduled
> run only **prepares**; the human still decides and acts (§4.3), and the monitoring piece goes live only on
> CCO approval (§4.1)."*
