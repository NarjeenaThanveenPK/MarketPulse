"""
MarketPulse — Synthetic Data Generation
=========================================

Generates two tables that do NOT exist in the real Olist dataset, and are
required for this project's funnel analysis and A/B testing modules:

1. sessions.csv
   - One "converting" session per real order (guarantees every purchase in
     the real data has a matching session with a full funnel: view -> cart
     -> checkout -> purchase).
   - Additional "non-converting" sessions (browsed but didn't buy), so the
     conversion funnel has realistic drop-off at each stage.

2. experiments.csv
   - Simulated A/B test: customers are randomly assigned to control/treatment
     for a "new checkout experience" experiment.
   - Treatment group is given a deliberate, modest conversion uplift so the
     A/B testing notebook has a real, detectable effect to find.

IMPORTANT: Both tables are entirely synthetic / generated for this project.
They are NOT real user behavior or real company data. This is documented
here and in the project README.

Run this script once after downloading and placing the real Olist CSVs in
data/raw/. Output is written back into data/raw/ so all raw inputs live in
one place for the ETL step.
"""

import numpy as np
import pandas as pd

# Reproducibility — same output every run
np.random.seed(42)

RAW_DIR = "../data/raw"

# ---------------------------------------------------------------------------
# 1. Load the real tables we need to reference
# ---------------------------------------------------------------------------
orders = pd.read_csv(f"{RAW_DIR}/olist_orders_dataset.csv")
customers = pd.read_csv(f"{RAW_DIR}/olist_customers_dataset.csv")

orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"]
)

# ---------------------------------------------------------------------------
# 2. Generate SESSIONS table
# ---------------------------------------------------------------------------

# --- 2a. One converting session per real order ---
converting_sessions = pd.DataFrame({
    "session_id": ["sess_conv_" + str(i) for i in range(len(orders))],
    "customer_id": orders["customer_id"],
    "order_id": orders["order_id"],
    "session_date": orders["order_purchase_timestamp"],
    "pages_viewed": np.random.randint(4, 25, size=len(orders)),
    "time_on_site": np.random.randint(120, 1800, size=len(orders)),  # seconds
    "added_to_cart": True,
    "checkout_started": True,
    "purchase": True,
})

# --- 2b. Non-converting sessions (browsed but didn't buy) ---
# Generate extra sessions equal to ~60% of order volume, from random existing
# customers, with realistic funnel drop-off at each stage.
N_NON_CONVERTING = int(len(orders) * 0.6)

random_customers = customers.sample(
    n=N_NON_CONVERTING, replace=True
)["customer_id"].values

# Random session dates spread across the same date range as real orders
date_min = orders["order_purchase_timestamp"].min()
date_max = orders["order_purchase_timestamp"].max()
random_days = np.random.randint(
    0, (date_max - date_min).days, size=N_NON_CONVERTING
)
random_dates = date_min + pd.to_timedelta(random_days, unit="D")

# Funnel drop-off: everyone views pages, ~45% add to cart, ~60% of those
# start checkout, and NONE of these sessions purchase (that's what makes
# them "non-converting" by definition).
added_to_cart = np.random.rand(N_NON_CONVERTING) < 0.45
checkout_started = added_to_cart & (np.random.rand(N_NON_CONVERTING) < 0.60)

non_converting_sessions = pd.DataFrame({
    "session_id": ["sess_nonconv_" + str(i) for i in range(N_NON_CONVERTING)],
    "customer_id": random_customers,
    "order_id": None,
    "session_date": random_dates,
    "pages_viewed": np.random.randint(1, 15, size=N_NON_CONVERTING),
    "time_on_site": np.random.randint(20, 900, size=N_NON_CONVERTING),
    "added_to_cart": added_to_cart,
    "checkout_started": checkout_started,
    "purchase": False,
})

sessions = pd.concat(
    [converting_sessions, non_converting_sessions], ignore_index=True
)
sessions = sessions.sample(frac=1, random_state=42).reset_index(drop=True)

sessions.to_csv(f"{RAW_DIR}/sessions.csv", index=False)
print(f"sessions.csv written — shape: {sessions.shape}")

# ---------------------------------------------------------------------------
# 3. Generate EXPERIMENTS table
# ---------------------------------------------------------------------------
# Simulated experiment: "New checkout experience" test.
# A subset of customers are randomly assigned to control or treatment.
# Treatment gets a deliberate, modest conversion uplift (10% -> 13%) so the
# A/B testing notebook has a genuine, detectable effect to find and report.

N_EXPERIMENT_CUSTOMERS = 20000

experiment_customers = customers.sample(
    n=N_EXPERIMENT_CUSTOMERS, random_state=42
)["customer_id"].values

variant = np.random.choice(
    ["control", "treatment"], size=N_EXPERIMENT_CUSTOMERS, p=[0.5, 0.5]
)

# Base conversion rate for control, deliberate uplift for treatment
base_conversion_rate = 0.10
treatment_uplift = 0.03

conversion_prob = np.where(
    variant == "treatment",
    base_conversion_rate + treatment_uplift,
    base_conversion_rate,
)
conversion = np.random.rand(N_EXPERIMENT_CUSTOMERS) < conversion_prob

# Revenue only for converted customers, with some random spread.
# Treatment converters spend a similar amount to control (uplift is in
# conversion rate, not average order value — a realistic, defensible setup).
revenue = np.where(
    conversion,
    np.round(np.random.gamma(shape=2.0, scale=60.0, size=N_EXPERIMENT_CUSTOMERS), 2),
    0.0,
)

exposure_dates = date_min + pd.to_timedelta(
    np.random.randint(0, (date_max - date_min).days, size=N_EXPERIMENT_CUSTOMERS),
    unit="D",
)

experiments = pd.DataFrame({
    "customer_id": experiment_customers,
    "experiment_id": "checkout_redesign_v1",
    "variant": variant,
    "exposure_date": exposure_dates,
    "conversion": conversion,
    "revenue": revenue,
})

experiments.to_csv(f"{RAW_DIR}/experiments.csv", index=False)
print(f"experiments.csv written — shape: {experiments.shape}")

# ---------------------------------------------------------------------------
# 4. Quick sanity check printout
# ---------------------------------------------------------------------------
print("\n--- Sanity check ---")
print("Sessions funnel counts:")
print(sessions[["added_to_cart", "checkout_started", "purchase"]].sum())

print("\nExperiment conversion rate by variant:")
print(experiments.groupby("variant")["conversion"].mean())
