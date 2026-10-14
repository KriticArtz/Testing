"""
Arovenna — hypothetical 10,000-customer Monte Carlo simulation.

EVERYTHING HERE IS AN ASSUMPTION. Segment shares, willingness-to-pay (WTP)
distributions, feature valuations, churn and cost inputs are reasoned
guesses, not market data. The point is to make the assumptions explicit
and show how price/feature choices behave under them — then replace the
inputs with real pilot/survey data.

Run:  python3 arovenna_sim.py            (writes results.json next to it)
"""
import json
import math
import os
import random

SEED = 42
N = 10_000
random.seed(SEED)

# ---------------------------------------------------------------- segments
# share: fraction of the 10,000 prospects who reach the landing page/app
# wtp_median / wtp_sigma: lognormal monthly WTP for the *core* product ($)
# churn: baseline monthly churn for payers, before feature effects
# feat: how much each feature matters to this segment (0..1 weight)
FEATURES = [
    "sms_checkins",        # proactive SMS/push check-ins you can reply to
    "commitment_followup", # "you said X by Y — done?" loop
    "weekly_review",       # scorecard of commitments vs outcomes
    "calendar_context",    # read-only calendar for timing + planning
    "goal_breakdown",      # AI turns goals into weekly steps
    "accountability_buddy",# partner / stakes / shared streaks
    "auto_scheduling",     # AI writes to your calendar
    "finance_tracking",    # budgets, debt payoff (bank-linked)
    "fitness_planning",    # workout programming
    "ai_chat_assistant",   # general-purpose assistant chat
]

SEGMENTS = {
    "procrastinator_young_pro": dict(share=0.22, wtp_median=9.0, wtp_sigma=0.55, churn=0.08,
        feat=dict(sms_checkins=.95, commitment_followup=.95, weekly_review=.8, calendar_context=.6,
                  goal_breakdown=.6, accountability_buddy=.55, auto_scheduling=.35, finance_tracking=.25,
                  fitness_planning=.25, ai_chat_assistant=.3)),
    "adhd_exec_function": dict(share=0.12, wtp_median=10.0, wtp_sigma=0.6, churn=0.09,
        feat=dict(sms_checkins=1.0, commitment_followup=.95, weekly_review=.65, calendar_context=.75,
                  goal_breakdown=.7, accountability_buddy=.6, auto_scheduling=.5, finance_tracking=.2,
                  fitness_planning=.15, ai_chat_assistant=.3)),
    "college_student": dict(share=0.20, wtp_median=3.5, wtp_sigma=0.6, churn=0.14,
        feat=dict(sms_checkins=.7, commitment_followup=.7, weekly_review=.5, calendar_context=.7,
                  goal_breakdown=.65, accountability_buddy=.6, auto_scheduling=.4, finance_tracking=.35,
                  fitness_planning=.35, ai_chat_assistant=.55)),
    "coaching_seeker": dict(share=0.07, wtp_median=18.0, wtp_sigma=0.6, churn=0.07,
        feat=dict(sms_checkins=.85, commitment_followup=.95, weekly_review=.9, calendar_context=.5,
                  goal_breakdown=.85, accountability_buddy=.8, auto_scheduling=.3, finance_tracking=.3,
                  fitness_planning=.3, ai_chat_assistant=.35)),
    "optimized_power_user": dict(share=0.12, wtp_median=8.0, wtp_sigma=0.7, churn=0.10,
        feat=dict(sms_checkins=.35, commitment_followup=.45, weekly_review=.55, calendar_context=.8,
                  goal_breakdown=.4, accountability_buddy=.2, auto_scheduling=.85, finance_tracking=.3,
                  fitness_planning=.2, ai_chat_assistant=.5)),
    "busy_parent_shift_worker": dict(share=0.10, wtp_median=6.0, wtp_sigma=0.55, churn=0.10,
        feat=dict(sms_checkins=.6, commitment_followup=.6, weekly_review=.45, calendar_context=.85,
                  goal_breakdown=.4, accountability_buddy=.3, auto_scheduling=.55, finance_tracking=.4,
                  fitness_planning=.25, ai_chat_assistant=.3)),
    "chatgpt_skeptic": dict(share=0.10, wtp_median=2.0, wtp_sigma=0.8, churn=0.16,
        feat=dict(sms_checkins=.45, commitment_followup=.45, weekly_review=.35, calendar_context=.4,
                  goal_breakdown=.2, accountability_buddy=.25, auto_scheduling=.45, finance_tracking=.2,
                  fitness_planning=.15, ai_chat_assistant=.1)),
    "specialist_fitness_or_finance": dict(share=0.07, wtp_median=3.0, wtp_sigma=0.7, churn=0.15,
        feat=dict(sms_checkins=.35, commitment_followup=.35, weekly_review=.35, calendar_context=.3,
                  goal_breakdown=.3, accountability_buddy=.35, auto_scheduling=.2, finance_tracking=.55,
                  fitness_planning=.55, ai_chat_assistant=.2)),
}

# Trust penalty: share of each segment that refuses bank linking / sensitive data
PRIVACY_REFUSERS = 0.55  # applied to finance_tracking value

# ---------------------------------------------------------------- costs
# Per *paying* active user per month. All are placeholders to replace with
# measured numbers from a pilot. SMS price is a rough US A2P per-message
# figure including carrier pass-through fees — verify with your provider.
COST = dict(
    llm_low=0.50, llm_base=1.50, llm_high=4.00,  # $/user/mo, depends on model + volume
    sms_per_msg=0.011, sms_msgs_per_month=90,       # ~2 outbound/day + replies
    infra=0.30,                                     # hosting, db, monitoring, email
    support=0.25,                                   # support tooling/time, amortized
)
# Payments: share billed via app stores (15% small-biz rate, verify) vs web (Stripe-like 2.9% + $0.30)
APP_STORE_SHARE = 0.5
APP_STORE_FEE = 0.15
WEB_PCT, WEB_FIXED = 0.029, 0.30


def lognormal(median, sigma):
    return median * math.exp(random.gauss(0, sigma))


def build_population():
    names = list(SEGMENTS)
    weights = [SEGMENTS[n]["share"] for n in names]
    people = []
    for i in range(N):
        seg = random.choices(names, weights)[0]
        s = SEGMENTS[seg]
        # individual feature weights: segment weight +/- noise, clamped
        feat = {f: min(1.0, max(0.0, s["feat"][f] + random.gauss(0, 0.15))) for f in FEATURES}
        if random.random() < PRIVACY_REFUSERS:
            feat["finance_tracking"] *= 0.15
        people.append(dict(
            id=i, segment=seg,
            wtp_core=lognormal(s["wtp_median"], s["wtp_sigma"]),
            churn=min(0.35, max(0.02, s["churn"] + random.gauss(0, 0.02))),
            feat=feat,
            prefers_annual=random.random() < (0.35 if seg != "college_student" else 0.2),
        ))
    return people


def wtp_for_bundle(p, bundle):
    """WTP scales with how much of what this person values is in the bundle."""
    total = sum(p["feat"].values())
    covered = sum(p["feat"][f] for f in bundle)
    # Core WTP is anchored to the *must-have* loop; extra features add with
    # diminishing returns. A bundle missing the person's top features loses value.
    return p["wtp_core"] * (covered / total) ** 0.8 * 1.6


def feature_analysis(people):
    """Per-feature: avg importance, share ranking it top-3, and drivers of WTP."""
    out = {}
    for f in FEATURES:
        vals = [p["feat"][f] for p in people]
        top3 = sum(1 for p in people if f in sorted(p["feat"], key=p["feat"].get, reverse=True)[:3])
        # paying-intent weighted importance: importance * wtp
        pw = sum(p["feat"][f] * p["wtp_core"] for p in people) / sum(p["wtp_core"] for p in people)
        out[f] = dict(avg_importance=round(sum(vals) / N, 3),
                      pct_top3=round(top3 / N * 100, 1),
                      wtp_weighted_importance=round(pw, 3))
    return dict(sorted(out.items(), key=lambda kv: -kv[1]["wtp_weighted_importance"]))


def unit_cost(llm_key="llm_base", sms=True):
    c = COST[llm_key] + COST["infra"] + COST["support"]
    if sms:
        c += COST["sms_per_msg"] * COST["sms_msgs_per_month"]
    return c


def payment_fee(price):
    return APP_STORE_SHARE * price * APP_STORE_FEE + (1 - APP_STORE_SHARE) * (price * WEB_PCT + WEB_FIXED)


def simulate_price(people, bundle, monthly, annual, trial_conv_factor=0.12, sms=True, llm_key="llm_base",
                   months=12):
    """
    trial_conv_factor: of people whose WTP >= price, what fraction actually
    convert (inertia, never-activated, forgot). Real funnels leak heavily.
    """
    annual_eff = annual / 12
    payers_m, payers_a = [], []
    for p in people:
        w = wtp_for_bundle(p, bundle)
        if p["prefers_annual"] and w >= annual_eff:
            # stronger value perception needed to commit upfront
            if random.random() < trial_conv_factor * 0.9:
                payers_a.append(p)
        elif w >= monthly:
            if random.random() < trial_conv_factor:
                payers_m.append(p)
    # Monthly cohort decays; surplus (WTP well above price) lowers churn
    rev = cost = fees = 0.0
    active_m = []
    for p in payers_m:
        surplus = wtp_for_bundle(p, bundle) / monthly
        churn = p["churn"] / min(2.0, max(0.7, surplus))
        alive = 1.0
        for _ in range(months):
            rev += alive * monthly
            fees += alive * payment_fee(monthly)
            cost += alive * unit_cost(llm_key, sms)
            alive *= (1 - churn)
        active_m.append(alive)
    # Annual: paid upfront, ~active usage decays but cost only while engaged
    for p in payers_a:
        rev += annual
        fees += payment_fee(annual)
        engaged = 1.0
        for _ in range(months):
            cost += engaged * unit_cost(llm_key, sms)
            engaged *= (1 - p["churn"] * 0.6)
    payers = len(payers_m) + len(payers_a)
    gross_margin = (rev - fees - cost) / rev if rev else 0
    return dict(
        monthly=monthly, annual=annual,
        paying_customers=payers,
        conversion_pct=round(payers / N * 100, 2),
        annual_share_pct=round(len(payers_a) / payers * 100, 1) if payers else 0,
        month12_active_monthly_payers=round(sum(active_m)),
        year1_revenue=round(rev),
        year1_payment_fees=round(fees),
        year1_variable_cost=round(cost),
        year1_gross_profit=round(rev - fees - cost),
        gross_margin_pct=round(gross_margin * 100, 1),
        revenue_per_prospect=round(rev / N, 2),
    )


def main():
    people = build_population()
    seg_counts = {s: sum(1 for p in people if p["segment"] == s) for s in SEGMENTS}
    wtps = sorted(p["wtp_core"] for p in people)
    pct = lambda q: round(wtps[int(q * (N - 1))], 2)
    bands = [(0, 2), (2, 5), (5, 8), (8, 10), (10, 15), (15, 20), (20, 30), (30, 1e9)]
    wtp_dist = {f"${lo:g}-{'' if hi > 1e8 else f'${hi:g}'}".rstrip("-") + ("+" if hi > 1e8 else ""):
                round(sum(1 for w in wtps if lo <= w < hi) / N * 100, 1) for lo, hi in bands}
    seg_wtp = {s: round(sorted(p["wtp_core"] for p in people if p["segment"] == s)[seg_counts[s] // 2], 2)
               for s in SEGMENTS}

    features = feature_analysis(people)

    CORE = ["sms_checkins", "commitment_followup", "weekly_review", "calendar_context", "goal_breakdown"]
    CORE_PLUS_BUDDY = CORE + ["accountability_buddy"]
    EVERYTHING = FEATURES

    # Price sweep on the focused core bundle (annual ~ 7x monthly ≈ 42% off)
    sweep = []
    for m in [4.99, 6.99, 7.99, 8.99, 9.99, 11.99, 12.99, 14.99, 17.99, 19.99]:
        random.seed(SEED + 1)
        sweep.append(simulate_price(people, CORE_PLUS_BUDDY, m, round(m * 7, 2)))

    # Compare proposed pricing on the broad bundle vs focused bundle
    random.seed(SEED + 2)
    proposed_plus = simulate_price(people, CORE + ["ai_chat_assistant"], 9.99, 99.99)
    random.seed(SEED + 2)
    proposed_pro = simulate_price(people, EVERYTHING, 19.99, 199.99)
    random.seed(SEED + 2)
    recommended = simulate_price(people, CORE_PLUS_BUDDY, 9.99, 69.99)
    random.seed(SEED + 2)
    rec_push_only = simulate_price(people, [f for f in CORE_PLUS_BUDDY if f != "sms_checkins"], 7.99, 55.99,
                                   sms=False)

    # Margin sensitivity for recommended price
    margins = {}
    for llm in ["llm_low", "llm_base", "llm_high"]:
        for sms in [True, False]:
            random.seed(SEED + 2)
            r = simulate_price(people, CORE_PLUS_BUDDY, 9.99, 69.99, sms=sms, llm_key=llm)
            margins[f"{llm}|{'sms' if sms else 'push_only'}"] = dict(
                unit_cost_per_user_month=round(unit_cost(llm, sms), 2),
                gross_margin_pct=r["gross_margin_pct"])

    per_user = {}
    for price in [7.99, 9.99, 12.99]:
        uc = unit_cost("llm_base", True)
        fee = payment_fee(price)
        per_user[f"${price}"] = dict(price=price, payment_fee=round(fee, 2), variable_cost=round(uc, 2),
                                     contribution=round(price - fee - uc, 2),
                                     margin_pct=round((price - fee - uc) / price * 100, 1))
    for annual in [69.99]:
        m = annual / 12
        uc = unit_cost("llm_base", True) * 0.8  # annual users engage a bit less on average
        fee = payment_fee(annual) / 12
        per_user[f"${annual}/yr"] = dict(price_per_month=round(m, 2), payment_fee=round(fee, 2),
                                         variable_cost=round(uc, 2), contribution=round(m - fee - uc, 2),
                                         margin_pct=round((m - fee - uc) / m * 100, 1))

    results = dict(
        disclaimer="All outputs are hypothetical, generated from assumed inputs; not market data.",
        n=N, seed=SEED,
        segment_counts=seg_counts,
        wtp_core_percentiles=dict(p10=pct(.1), p25=pct(.25), median=pct(.5), p75=pct(.75), p90=pct(.9)),
        wtp_core_distribution_pct=wtp_dist,
        segment_median_wtp=seg_wtp,
        feature_ranking=features,
        price_sweep_core_bundle=sweep,
        comparison=dict(proposed_plus_9_99=proposed_plus, proposed_pro_19_99_everything=proposed_pro,
                        recommended_9_99_69_99=recommended, push_only_7_99_55_99=rec_push_only),
        margin_sensitivity=margins,
        per_user_unit_economics=per_user,
        cost_assumptions=COST,
    )
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results.json")
    with open(path, "w") as fh:
        json.dump(results, fh, indent=2)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
