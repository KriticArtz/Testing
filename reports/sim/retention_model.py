"""
Arovenna — 24-month retention & margin scenario model.

HYPOTHETICAL. Shows how improving activation, churn, annual mix, referrals
and unit costs changes subscribers, revenue and margin. Every input is an
assumption; replace with pilot data. Prices: $9.99/mo, $79.99/yr.

Run:  python3 retention_model.py   (writes retention_results.json)
"""
import json
import os

MONTHS = 24
PRICE_M, PRICE_A = 9.99, 79.99

# Organic sign-ups per month (before referrals). Launch spike in January
# (month 1), a smaller back-to-school bump in September (month 9).
BASE_SIGNUPS = [5000, 2500, 2000, 1800, 1600, 1500, 1500, 1600, 2500, 2000, 1800, 1700,
                4000, 2200, 1900, 1800, 1700, 1600, 1600, 1700, 2600, 2100, 1900, 1800]

SCENARIOS = {
    "1_baseline": dict(
        desc="Launch as-is: generic onboarding, fixed-schedule nudges, annual offered at sign-up",
        activation=0.35, trial_to_paid=0.12, monthly_churn=0.10, annual_share=0.30,
        annual_renewal=0.55, referral_per_payer=0.03,
        llm=1.50, sms_msgs=90, app_store_share=0.70),
    "2_retention_fixes": dict(
        desc="+ text-first onboarding, adaptive check-ins, fresh-start flow, weekly review, "
             "pause/downgrade, annual offered after 2nd review",
        activation=0.50, trial_to_paid=0.15, monthly_churn=0.065, annual_share=0.45,
        annual_renewal=0.68, referral_per_payer=0.03,
        llm=1.50, sms_msgs=90, app_store_share=0.70),
    "3_retention_plus_virality": dict(
        desc="+ accountability buddy invites and shareable weekly scorecard",
        activation=0.50, trial_to_paid=0.15, monthly_churn=0.06, annual_share=0.45,
        annual_renewal=0.70, referral_per_payer=0.12,
        llm=1.50, sms_msgs=90, app_store_share=0.70),
    "4_full_playbook": dict(
        desc="+ cheap-model routing, push-default with capped SMS, web billing",
        activation=0.50, trial_to_paid=0.15, monthly_churn=0.06, annual_share=0.45,
        annual_renewal=0.70, referral_per_payer=0.12,
        llm=0.60, sms_msgs=50, app_store_share=0.35),
}

SMS_PER_MSG = 0.011     # rough US A2P incl. carrier fees — verify with provider
INFRA_SUPPORT = 0.55    # $/payer/month
FREE_USER_COST = 0.15   # $/active free user/month (push only, cheapest model)
FREE_MONTHLY_DECAY = 0.30
ANNUAL_ENGAGEMENT = 0.8  # annual payers use the product a bit less on average
APP_STORE_FEE = 0.15
WEB_PCT, WEB_FIXED = 0.029, 0.30


def fee(price, store_share):
    return store_share * price * APP_STORE_FEE + (1 - store_share) * (price * WEB_PCT + WEB_FIXED)


def run(s):
    unit = s["llm"] + s["sms_msgs"] * SMS_PER_MSG + INFRA_SUPPORT
    monthly = 0.0
    annual_cohorts = []  # [start_month, count]
    free = 0.0
    totals = dict(revenue=0.0, fees=0.0, cost=0.0, signups=0.0)
    timeline = []
    for t in range(MONTHS):
        annual_active = sum(c for _, c in annual_cohorts)
        signups = BASE_SIGNUPS[t] + s["referral_per_payer"] * (monthly + annual_active)
        new_payers = signups * s["activation"] * s["trial_to_paid"]
        new_annual = new_payers * s["annual_share"]
        new_monthly = new_payers - new_annual

        revenue = fees = 0.0
        # renewals of annual cohorts hitting their anniversary
        renewed = 0.0
        for c in annual_cohorts:
            if t > c[0] and (t - c[0]) % 12 == 0:
                c[1] *= s["annual_renewal"]
                renewed += c[1]
        annual_cohorts.append([t, new_annual])
        annual_active = sum(c for _, c in annual_cohorts)

        monthly = monthly * (1 - s["monthly_churn"]) + new_monthly
        free = free * (1 - FREE_MONTHLY_DECAY) + (signups - new_payers)

        revenue += monthly * PRICE_M + (new_annual + renewed) * PRICE_A
        fees += monthly * fee(PRICE_M, s["app_store_share"]) + (new_annual + renewed) * fee(PRICE_A, s["app_store_share"])
        cost = (monthly + annual_active * ANNUAL_ENGAGEMENT) * unit + free * FREE_USER_COST

        totals["revenue"] += revenue
        totals["fees"] += fees
        totals["cost"] += cost
        totals["signups"] += signups
        timeline.append(dict(month=t + 1, signups=round(signups), paying=round(monthly + annual_active),
                             revenue=round(revenue), gross_profit=round(revenue - fees - cost)))

    contrib_m = PRICE_M - fee(PRICE_M, s["app_store_share"]) - unit
    ltv = contrib_m / s["monthly_churn"]
    gp = totals["revenue"] - totals["fees"] - totals["cost"]
    m12 = timeline[11]
    m24 = timeline[23]
    return dict(
        description=s["desc"],
        unit_cost_per_payer_month=round(unit, 2),
        contribution_per_monthly_payer=round(contrib_m, 2),
        avg_paid_lifetime_months=round(1 / s["monthly_churn"], 1),
        ltv_monthly_payer=round(ltv),
        max_cac_one_third_first_year=round(contrib_m * sum((1 - s["monthly_churn"]) ** i for i in range(12)) / 3, 2),
        paying_month_12=m12["paying"], paying_month_24=m24["paying"],
        run_rate_revenue_month_24_annualized=m24["revenue"] * 12,
        total_signups_24m=round(totals["signups"]),
        revenue_24m=round(totals["revenue"]),
        gross_profit_24m=round(gp),
        gross_margin_pct=round(gp / totals["revenue"] * 100, 1),
        timeline=timeline,
    )


def main():
    results = dict(disclaimer="Hypothetical scenario model; all inputs are assumptions.",
                   prices=dict(monthly=PRICE_M, annual=PRICE_A), base_signups=BASE_SIGNUPS,
                   scenarios={k: dict(inputs=v, **run(v)) for k, v in SCENARIOS.items()})
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "retention_results.json")
    with open(path, "w") as fh:
        json.dump(results, fh, indent=2)
    for k, r in results["scenarios"].items():
        print(f"{k:28s} m12={r['paying_month_12']:>6} m24={r['paying_month_24']:>6} "
              f"rev24={r['revenue_24m']:>9} gp24={r['gross_profit_24m']:>9} gm={r['gross_margin_pct']:>5}% "
              f"ltv={r['ltv_monthly_payer']:>4} maxCAC={r['max_cac_one_third_first_year']:>6} "
              f"unit={r['unit_cost_per_payer_month']} contrib={r['contribution_per_monthly_payer']} "
              f"signups={r['total_signups_24m']} m24rr={r['run_rate_revenue_month_24_annualized']}")


if __name__ == "__main__":
    main()
