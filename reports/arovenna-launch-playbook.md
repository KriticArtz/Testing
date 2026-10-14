# Arovenna — Launch Playbook (Oct 2026 → Q1 2027)

> **How to read this.** The plan is opinionated guidance. All numbers marked *[model]* come from the hypothetical retention model in `reports/sim/retention_model.py` (raw output: `reports/sim/retention_results.json`) and inherit its assumptions — they are not forecasts. Targets are starting points to replace with your own pilot data.

**Goal:** launch in the New Year window (target **Mon Jan 4, 2027**) with a product people keep using, a waitlist that converts, and unit economics that hold up.

**The strategy in one line:** one audience (people who struggle with follow-through), one loop (commit → check-in → follow-up → weekly review), proven retention before growth, cheap to run per user.

---

## Part 1 — Why retention comes first *[model]*

24-month scenarios, same organic sign-up assumptions (~50K sign-ups over 24 months, January launch spike), $9.99/mo or $79.99/yr:

| Scenario | What changes | Payers @ M12 | Payers @ M24 | 24-mo revenue | 24-mo gross profit | Gross margin | LTV (monthly payer) | Max CAC* |
|---|---|---|---|---|---|---|---|---|
| 1. Baseline | Launch as-is | 746 | 1,043 | $166K | $75K | 45% | $57 | $13.69 |
| 2. Retention fixes | Activation 35→50%, churn 10→6.5%/mo, more annual, better renewals | 1,595 | 2,514 | $361K | $193K | 54% | $88 | $16.25 |
| 3. + Virality | Buddy invites + shareable scorecards | 1,683 | 2,784 | $389K | $209K | 54% | $95 | $16.67 |
| 4. Full playbook | + cheap-model routing, push-default/capped SMS, web billing | 1,683 | 2,784 | $389K | **$272K** | **70%** | **$123** | **$21.49** |

\*Max CAC = one-third of a monthly payer's first-year contribution — a conservative ceiling for paid acquisition.

**What the model says:**
- **Retention fixes more than double the business** (2.4× subscribers at month 24, 2.2× revenue) with *zero* extra sign-ups. This is the highest-leverage work you can do.
- **Cost work turns the same revenue into ~30% more profit** (gross margin 54% → 70%) and raises what you can afford to pay per customer by ~30%.
- **Virality helps modestly** in this model (+11% subscribers). Its real value is free acquisition — treat it as a bonus, not the plan.
- **Paid ads are tight at any scenario:** you can afford roughly $14–21 per *paying* customer. With ~7% of sign-ups paying, that's ~$1–1.50 per sign-up — hard to hit with ads. **Organic and creator channels have to carry the launch.**

---

## Part 2 — Week-by-week plan

### Phase 0 — Focus (Oct 19 – Nov 1)

| Week | Do | Done when |
|---|---|---|
| Oct 19 | Lock scope: commitment follow-up, check-ins, weekly review, read-only calendar. Write down what's **cut** (finance, fitness, auto-scheduling, bank linking). | One-page scope doc |
| Oct 19 | Rewrite the website hero: *"The AI that checks in on you — so you actually do what you said you'd do."* Add waitlist + "founding member" interest. | Live waitlist |
| Oct 26 | Recruit 30–50 pilot users from the target audience (friends-of-friends, ADHD/productivity communities — follow each community's self-promotion rules). | 40 sign-ups for pilot |
| Oct 26 | Set up SMS properly: provider account, US A2P 10DLC brand/campaign registration, explicit opt-in wording, STOP/HELP handling. Registration can take weeks — start now. | Registration submitted |

### Phase 1 — Concierge pilot (Nov 2 – Nov 29)

Run the loop by text with an LLM drafting messages and **you reviewing** them. No app yet — a spreadsheet and an SMS tool are enough.

| Week | Focus | Measure |
|---|---|---|
| Nov 2 | Onboarding by text: name 1–3 commitments, pick check-in times and tone. First check-in within 5 minutes. | % who reply to 3 check-ins in week 1 (**activation**) |
| Nov 9 | Tune timing and tone; add quiet hours; back off when ignored. | Reply rate per message; opt-outs |
| Nov 16 | First weekly reviews (Sunday). Test the "fresh start" message on anyone who went quiet. | % re-engaged after a miss |
| Nov 23 | Week-4 check: ask every user to pay (founding price) to continue. Interview 10 users, including the quiet ones. | **Week-4 engagement** and **% who pay** |

**Go / no-go gate (end of November):**
- ✅ Go: ≥40% still engaging in week 4 **and** ≥20% of those pay when asked.
- ⚠️ Iterate: 25–40% engaged — run a second 4-week cohort with fixes before building.
- ❌ Rethink: <25% engaged even after tuning timing and tone.

Also record: AI cost per user, SMS messages per user, which messages get replies. These replace the model's guesses.

### Phase 2 — Build + pre-sell (Nov 30 – Dec 27)

| Week | Build | Market |
|---|---|---|
| Nov 30 | Text-first sign-up (text a number to start), check-in engine with adaptive timing, commitment ledger | Start posting real (anonymized, permissioned) check-in screenshots and pilot stories on TikTok / Instagram / YouTube Shorts |
| Dec 7 | Weekly review, fresh-start flow, tone settings, quiet hours, calendar read access | Open **founding member** pre-sale: $59/yr, price locked for life, limited count |
| Dec 14 | Billing (web checkout first), pause/downgrade instead of cancel, push notifications | Line up 5–10 creators in productivity/ADHD/self-improvement on revenue-share affiliate deals |
| Dec 21 | Model routing (cheap model for routine check-ins, stronger model for weekly reviews), per-user usage caps, cost dashboard | Pre-launch email/text to waitlist: "Your New Year check-in starts Jan 4" |

### Phase 3 — Launch (Dec 28 – Jan 10)

- **Dec 28 – Jan 3:** "Make this the year you actually follow through" campaign; creators post; waitlist gets early access.
- **Mon Jan 4, 2027: public launch.** Push everyone to send their first commitment by text on day one.
- **First week:** watch activation daily; fix onboarding drop-offs the same day; personally reply to feedback.

### Phase 4 — First 90 days (Jan – Mar 2027)

| When | Focus |
|---|---|
| Weeks 2–4 | Activation and the first weekly review. Anyone who misses 3 days gets the fresh-start flow. |
| Weeks 3–6 | Offer annual ($79.99) to users after their 2nd–3rd weekly review — not at sign-up. |
| Weeks 4–8 | Ship **accountability buddy** invites and a shareable weekly scorecard. |
| February | "Quitter's day" save campaign: mid-Feb is when New Year goals collapse — run a re-commit challenge. |
| Monthly | Call 5–10 churned users. Fix the top reason before adding features. |
| Month 3 | Only now test small paid campaigns, with a hard CAC cap (see Part 1). Decide whether to test a Coach+ tier ($17.99–19.99) with buddy/stakes features. |

---

## Part 3 — The playbook by goal

### Get people in
1. **Text-first onboarding** — no download needed to start; first check-in within 5 minutes.
2. **Content that shows the product** — real check-in exchanges are inherently shareable.
3. **Creator partnerships** with revenue share in productivity/ADHD/self-improvement niches.
4. **Built-in invites** — accountability buddy makes the product better with a friend.
5. **Campus ambassadors** for the $4.99 student plan (push-only to protect margin).
6. **Seasonal timing** — New Year and back-to-school are the high-intent windows.
7. **Founding-member annual pre-sale** — cash upfront, committed users, social proof at launch.

### Keep them
1. **Activation = 3 replies in week 1.** Everything in week 1 serves this.
2. **Adaptive check-ins** — user-chosen times, quiet hours, tone settings, back off when ignored, hard daily cap.
3. **Fresh start, never guilt** after a missed stretch.
4. **Sunday weekly review** as the ritual — visible progress over time.
5. **Memory** — reference past wins and patterns; value builds the longer someone stays.
6. **"What's next?"** when a goal is completed, so success doesn't cause churn.
7. **Annual offered after proof** (2nd–3rd review).
8. **Pause / downgrade to free** before cancel; win-back text 30 days later.
9. **Talk to churned users** every month.

### Keep margins healthy
1. **Model routing** — cheap model for routine check-ins, strong model only for reviews/planning; cache prompts; per-user caps.
2. **Push by default, SMS as a capped paid feature** (~50 messages/month in the full-playbook scenario vs ~90).
3. **Web billing** where store rules allow (~3–6% vs 15% fees) — verify current iOS external-payment rules in your markets.
4. **Cheap free tier** — push only, one goal, cheapest model.
5. **Don't discount below $9.99/mo or ~$79.99/yr**; use the founding-member price only once.
6. **Weekly cost dashboard** — AI + SMS cost per active user, margin per plan.

*[model]* Full-playbook unit cost ≈ **$1.70/payer/month** (vs $3.04 baseline) → contribution ≈ **$7.38** per $9.99 monthly payer (vs $5.72).

---

## Part 4 — Metrics dashboard (check weekly)

| Metric | Definition | Starting target |
|---|---|---|
| Activation | % of sign-ups replying to ≥3 check-ins in first 7 days | ≥50% |
| Week-4 engagement | % of a cohort still replying in week 4 | ≥40% |
| Trial → paid | % of activated users who pay | ≥15% |
| Monthly churn | % of monthly payers cancelling per month | <7% |
| Annual mix | % of new payers choosing annual | ≥40% |
| Annual renewal | % of annual payers renewing | ≥65% |
| Opt-out rate | % texting STOP per month | <3% |
| Unit cost | AI + SMS + infra per paying user per month | ≤$2 |
| Gross margin | (revenue − payment fees − variable cost) / revenue | ≥65% |
| CAC (paid) | Spend ÷ new paying customers | ≤ max CAC from model (~$14–21) |
| Referral rate | Invites accepted per paying user per month | ≥0.1 |

---

## Part 5 — Don'ts

- Don't build finance, fitness or auto-scheduling before the core loop retains.
- Don't ask for bank logins.
- Don't make medical claims about ADHD — say "built for people who struggle with follow-through."
- Don't text anyone without explicit opt-in and completed carrier registration.
- Don't run paid ads before week-4 retention is known.
- Don't add features to fix a retention problem — fix the loop.
- Don't offer the annual plan before people have seen value.

---

## Part 6 — What could change this plan

| If the pilot shows… | Then… |
|---|---|
| Week-4 engagement < 25% | Rethink the concept before building — likely timing/tone or the core premise |
| People love it but won't pay | Test a lower-cost push-only plan; look at a B2B angle (coaches, schools, employers) |
| SMS dramatically outperforms push | Keep SMS central; raise price toward $12.99 or add an SMS-heavy tier |
| AI cost per user > $3 | Tighten routing and caps before launch, or raise price |
| One segment retains far better | Narrow messaging to that segment entirely |
