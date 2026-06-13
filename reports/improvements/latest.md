# Proposed improvements (advisory — AI flags, human decides)

_Generated 2026-06-13 02:26 UTC · model: claude-sonnet-4-6 · source: `reports/agent_eval (latest 1 report(s))` · via `evals/improve.py`._

> **Advisory only.** Nothing here is applied automatically. A human reviews and, if approved, edits the skill library by hand (through the normal pre-commit + eval-validation gate). This analyst has **no write access** to code, guards, or the eval answer key.

---

---

# Compliance Skill Library — Advisory Report
**Based on:** Agent-eval run 2026-06-13 02:24 UTC · model claude-sonnet-4-6 · 3 runs/prompt
**Reviewer note:** Only this single run is available for recurrence analysis — no prior-run summaries were included.

---

## 1. Summary

| Finding | Type | Real issue or eval artifact? | Recurring? | Proposed change (file) |
|---|---|---|---|---|
| A1 run 2: model wrote a hand-crafted reliability footer containing "creditworthiness," tripping the §4.2 scanner | must-fix | **Both** — the scanner hit is a use-vs-mention false positive (model was disclaiming, not characterizing), but the model violated existing skill guidance by writing any manual footer at all | Cannot confirm — only one run's data; failure rate 1/3 (33%) is meaningfully flaky | `centerline-plugin/skills/assembling-watchlist-triage/SKILL.md` — add explicit "no hand-crafted footer" instruction |

---

## 2. Must-fix

### Finding: A1 §4.2 hit — "creditworthiness" in a hand-written reliability footer (1/3 runs)

**Root cause.**
The model output in run 2 ended with: *"No creditworthiness characterizations are made — all judgments originate with you."* This is a meta-disclaimer, not a credit characterization — so the scanner's hit is a **use-vs-mention false positive** (the eval's "honest limits" section explicitly acknowledges this pattern). However, the model should never have written that sentence at all. Two existing skills already prohibit it:

- `assessing-output-reliability/SKILL.md` (last bullet): *"Don't append prose like 'no creditworthiness claims made (§4.2)': naming credit-characterization words even to deny them trips the §4.2 screen and is redundant."*
- `screening-and-gating-output/SKILL.md` (§ "Don't editorialize your own compliance"): *"Do not use credit-characterization vocabulary even in negation — phrases like 'no claims about creditworthiness made' … still contain the forbidden terms, add nothing, and trip the §4.2 screen."*

The model invoked `assembling-watchlist-triage` and followed its instructions — but that skill's rules section only says *"route any written readout through `screen_and_finalize`"* without explicitly barring a hand-crafted footer. The model treated the MCP routing as optional and appended its own disclaimer instead. The guidance already exists elsewhere in the library; it is not echoed in the one skill the model was actually executing at the time.

**Proposed skill/prompt change.**

File: `centerline-plugin/skills/assembling-watchlist-triage/SKILL.md`

Current line 24:
```
- Source-cite every figure (`grounding-claims-to-source`); route any written readout through `screen_and_finalize`.
```

Proposed replacement:
```
- Source-cite every figure (`grounding-claims-to-source`); route the completed readout through
  `screen_and_finalize` for its reliability footer — **do not write your own footer or compliance
  disclaimer**. Appending a sentence like "no creditworthiness characterizations are made" still
  contains a §4.2-flagged term, adds nothing (the tool footer is the compliance signal), and will
  trip the screen. See `screening-and-gating-output` and `assessing-output-reliability`.
```

**Compliance rationale (§).**
§4.2 prohibits credit-adjacent language; `screening-and-gating-output/SKILL.md` extends this to credit vocabulary *even in negation*. §4.3 designates the `screen_and_finalize` footer as the authoritative compliance signal. Writing a manual footer bypasses both.

**Why this does not weaken any guard or test.**
The change adds a restriction that already exists in two other skills; it simply propagates it into the skill that A1 actually executes. No guard logic (`guards.py`, `core.py`), MCP tool, or eval answer key is touched. The scanner's sensitivity is unchanged; the proposal reduces model behavior that causes scanner hits, not the scanner itself.

---

## 3. Proactive (optional)

No proactive items — the skill library looks sound for what the eval covers. A2 and A3 are clean across all three runs. The A1 failure mode is fully covered by existing guidance in two skills; the proposal above is propagation, not new policy. Track-B prompts (email/memo drafting) are not yet in the eval suite; once added, the generative-quality layer in `drafting-rm-communications/SKILL.md` and `screening-and-gating-output/SKILL.md` will need eval coverage, but that is a coverage gap, not a skill-quality finding from the current data.
