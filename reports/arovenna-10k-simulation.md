# Arovenna — 10,000-Customer Simulation: Features, Price & Margins

> **Hypothetical.** This is a Monte Carlo simulation of 10,000 *synthetic* prospects generated from assumed segment sizes, willingness-to-pay (WTP) curves, feature preferences, churn and costs. It is not survey data. Every number below inherits those assumptions — see `reports/sim/arovenna_sim.py` (all inputs at the top of the file) and the raw output in `reports/sim/results.json`. Re-run it with real pilot data to get real answers.
>
> **Website:** arovenna.com could not be reviewed — the session's network policy blocked it — so this simulation is based on the concept description only.

## How the simulation works

1. **10,000 prospects** drawn from 8 segments (assumed mix): procrastinating young professionals 22%, college students 20%, ADHD/executive-function 12%, optimized power users 12%, busy parents/shift workers 10%, "I'll just use ChatGPT" skeptics 10%, coaching seekers 7%, fitness/finance specialists 7%.
2. Each prospect gets a personal **WTP** (lognormal around their segment's median), **feature importance weights** (segment weight + individual noise), a **monthly churn** rate, and a monthly vs. annual preference. 55% refuse to link financial accounts.
3. For each price/bundle, a prospect converts only if the bundle's value to them ≥ the price, then only ~12% of those actually convert (funnel leakage). Payers churn monthly; churn is lower when value far exceeds price.
4. Year-1 revenue, payment fees (50% app store at 15%, 50% web at 2.9% + $0.30) and variable costs (AI, SMS, infra, support) are tallied.

## Result 1 — What to focus on

Feature ranking across 10,000 prospects, weighted by willingness to pay (the people who'd actually pay):

| Rank | Feature | WTP-weighted importance | % ranking it top-3 | Verdict |
|---|---|---|---|---|
| 1 | **Commitment follow-up** ("you said X by Y — done?") | 0.77 | 66% | **Build first — the core** |
| 2 | **Proactive SMS/push check-ins** | 0.74 | 63% | **Build first — the differentiator** |
| 3 | **Weekly review / scorecard** | 0.67 | 39% | **Build first — drives retention** |
| 4 | **Calendar context (read-only)** | 0.65 | 48% | **Build first — smart timing, quiet hours** |
| 5 | Goal → weekly steps breakdown | 0.60 | 25% | v1, lightweight |
| 6 | Accountability buddy / stakes | 0.52 | 17% | v1.5 — premium tier candidate |
| 7 | Auto-scheduling (writes to calendar) | 0.46 | 23% | Defer — only power users care |
| 8 | General AI chat assistant | 0.35 | 9% | Don't lead with it — ChatGPT does this |
| 9 | Fitness planning | 0.26 | 6% | Cut from launch (keep as a goal type) |
| 10 | Finance tracking (bank-linked) | 0.16 | 3% | Cut from launch (keep as a manual goal type) |

**Takeaway [hypothetical]:** The four features at the top form a single loop — *commit → get checked on → follow up → review the week*. Finance and fitness, which the current Pro tier is built on, came last, largely because of privacy refusals and better specialist apps.

## Result 2 — Who will pay

| Segment | Share | Median monthly WTP |
|---|---|---|
| Coaching seekers | 7% | **$18.50** |
| ADHD / executive function | 12% | **$9.82** |
| Procrastinating young professionals | 22% | **$8.90** |
| Optimized power users | 12% | $8.21 |
| Busy parents / shift workers | 10% | $6.22 |
| College students | 20% | $3.59 |
| Fitness/finance specialists | 7% | $3.00 |
| ChatGPT skeptics | 10% | $1.96 |

Overall WTP: median **$6.30**, 25th pct $3.40, 75th pct $10.90, 90th pct $17.50.
Distribution: <$5: 40% · $5–10: 32% · $10–20: 21% · $20+: 7.5%.

**Launch audience:** ADHD/executive-function + procrastinating young professionals (34% of prospects, ~$9–10 median WTP), with coaching seekers as the premium upsell.

## Result 3 — Price point

Price sweep for the focused core bundle (annual set at ~7× monthly):

| Monthly | Conversion | Paying customers | Year-1 revenue | Year-1 gross profit | Gross margin | Revenue per prospect |
|---|---|---|---|---|---|---|
| $4.99 | 8.2% | 816 | $33.5K | $7.8K | 23% | $3.35 |
| $6.99 | 6.7% | 671 | $37.9K | $16.1K | 43% | $3.79 |
| $7.99 | 6.2% | 616 | $40.1K | $19.4K | 48% | $4.01 |
| $8.99 | 5.7% | 568 | $41.2K | $21.7K | 53% | $4.12 |
| **$9.99** | **5.3%** | **527** | **$42.6K** | **$24.1K** | **57%** | **$4.26 (peak)** |
| $11.99 | 4.3% | 430 | $40.7K | $25.1K | 62% | $4.07 |
| $12.99 | 3.9% | 389 | $40.6K | $26.1K | 64% | $4.06 |
| $14.99 | 3.4% | 337 | $40.5K | $27.4K | 68% | $4.05 |
| $17.99 | 2.6% | 260 | $37.3K | $26.7K | 72% | $3.73 |
| $19.99 | 2.2% | 215 | $33.3K | $24.3K | 73% | $3.33 |

What this says (under these assumptions):
- **$9.99/month maximizes revenue.** Gross profit keeps edging up to ~$14.99 because fewer customers means lower SMS/AI costs, but you lose ~36% of your paying base for ~14% more profit. Early on, more customers is worth more (learning, word of mouth, a bigger base to upsell).
- **Revenue is nearly flat from $7.99 to $14.99** ($4.01–$4.26 per prospect). Price is *not* the main lever; **conversion and retention are**.
- **Below $7, margins collapse** — SMS and AI costs eat the price. A $4.99 plan only works without SMS.
- **Retention is the real problem:** of ~300 monthly payers at $9.99, only ~155 are still paying at month 12.

### Tier comparison (same 10,000 prospects)

| Option | Conversion | Payers | Year-1 revenue | Gross margin |
|---|---|---|---|---|
| Proposed Plus — $9.99 / $99.99 | 5.2% | 521 | $47.9K | 61% |
| Proposed Pro — $19.99 / $199.99 (everything) | 2.7% | 272 | $50.2K | 76% |
| **Recommended — $9.99 / $69.99 (focused loop)** | **5.8%** | **579** | $46.4K | 57% |
| Push-only — $7.99 / $55.99 (no SMS) | 6.1% | 609 | $39.0K | 61% |

**Read these honestly:**
- The $19.99 "everything" tier looks best on paper **only because the model assumes finance, fitness and auto-scheduling are already built and work well.** It doesn't count the engineering cost, compliance work or delayed launch those modules require, and it assumes adding features never makes the product feel more complex. Treat it as an upper bound, not a recommendation.
- $99.99/yr earns slightly more year-1 revenue than $69.99/yr, but converts fewer annual subscribers. And at $69.99/yr the per-user margin is thin (see below). **A middle option — $79.99/yr — is the better test.**

## Result 4 — Margins

Per paying user per month (base case: $1.50 AI cost + ~90 SMS at ~$0.011 + $0.55 infra/support = **$3.04**):

| Plan | Effective price/mo | Payment fees | Variable cost | **Contribution** | **Gross margin** |
|---|---|---|---|---|---|
| $7.99/mo | $7.99 | $0.87 | $3.04 | $4.08 | 51% |
| **$9.99/mo** | $9.99 | $1.04 | $3.04 | **$5.91** | **59%** |
| $12.99/mo | $12.99 | $1.31 | $3.04 | $8.64 | 67% |
| $69.99/yr | $5.83 | $0.53 | $2.43 | $2.87 | 49% |
| $79.99/yr *(computed the same way)* | $6.67 | $0.61 | $2.43 | $3.62 | 54% |

**Margin sensitivity at $9.99 / $69.99** (blended year-1 gross margin):

| AI cost / user / mo | With SMS | Push only |
|---|---|---|
| Low ($0.50) | 68% | 78% |
| **Base ($1.50)** | **57%** | **67%** |
| High ($4.00) | 29% | 40% |

**Key margin levers:**
1. **AI cost is the biggest swing factor.** Use a small, cheap model for routine check-ins and save the expensive model for weekly reviews and planning. Cap AI usage per user.
2. **SMS costs about $1/user/month.** Make push the default and SMS a paid feature with a cap (e.g. ~2 outbound/day).
3. **Web billing beats app-store billing** (~3–6% vs 15%). Push web checkout where store rules allow.
4. **Target 65–75% gross margin**, typical for healthy consumer subscription software *[assumption — benchmark it]*. At base costs you reach that only with cheap-model routing or a price ≥ ~$12.

These are gross margins — before marketing (likely the largest cost), salaries, and the cost of serving free users.

## Recommendation

| Tier | Price | What's in it |
|---|---|---|
| **Free** | $0 | 1 active goal, push check-ins only, basic weekly summary |
| **Arovenna** | **$9.99/mo or $79.99/yr**, 7-day trial | Unlimited goals, SMS + push check-ins (capped), commitment follow-up, calendar-aware timing, full weekly review, tone settings |
| **Student** | $4.99/mo or $39.99/yr | Same as Arovenna, **push-only** to protect margin |
| **Coach+** *(later)* | Test $17.99–19.99/mo | Accountability buddy/stakes, higher SMS caps, deeper reviews — for coaching seekers |

**Focus:** commitment follow-up + proactive check-ins + weekly review + calendar context. Ship those four well before anything else.

**Hypothetical economics at the recommended price** (blended ~$8.50/mo revenue per payer, ~$5/mo contribution):
- 1,000 payers ≈ $102K/yr revenue, ≈ $60K/yr gross profit
- 10,000 payers ≈ $1.0M/yr revenue, ≈ $600K/yr gross profit

## What to validate (the model is only as good as these inputs)

| Assumption | Why it matters | How to measure |
|---|---|---|
| Segment mix and WTP medians | Drives everything | Van Westendorp / Gabor-Granger survey with 200+ real target users |
| 12% funnel conversion factor | Converts "would pay" into "did pay" | Landing-page pre-orders, trial-to-paid in the pilot |
| Monthly churn 7–16% | Month-12 retention | 4–8 week concierge pilot, week-4 reply rates |
| $1.50 AI cost / user / month | Swings margin from 29% to 68% | Instrument the pilot; test cheap-model routing |
| ~90 SMS / user / month at ~$0.011 | ~$1/user/month | Provider quote incl. carrier fees + 10DLC registration |
| Finance/fitness low value | Justifies cutting them | "Fake door" buttons in the beta |
