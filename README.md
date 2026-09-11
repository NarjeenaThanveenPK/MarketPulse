<<<<<<< HEAD
=======
<div align="center">

# MarketPulse
## E-commerce Product Analytics & Experimentation Platform

>>>>>>> b2d73e6782e2b4f0c31e1c5ede389dc2d2b1a5f1
![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![PySpark](https://img.shields.io/badge/PySpark-Databricks-orange?logo=apachespark&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-S3-orange?logo=amazonaws&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-Dashboards-yellow?logo=powerbi&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

<<<<<<< HEAD
# MarketPulse — E-commerce Product Analytics & Experimentation Platform
=======
</div>

---

>>>>>>> b2d73e6782e2b4f0c31e1c5ede389dc2d2b1a5f1

## Problem Statement

How can an e-commerce company use large-scale customer and transaction data to understand business performance, identify the factors affecting conversion and retention, and determine whether product changes actually improve customer outcomes?

This project builds an end-to-end analytics and experimentation platform that ingests raw transactional data, processes it at scale, analyzes customer behavior, runs a controlled experiment, predicts customer churn, and surfaces the results through business-facing dashboards.

---

## Business Questions

**Business Performance**
- How is revenue changing over time?
- Which product categories drive the most revenue?
- Which customer segments are most valuable?

**Customer Behavior**
- What factors influence conversion?
- What factors are associated with customer retention?
- Which customers are at higher risk of churn?

**Experimentation**
- Does a new checkout experience increase conversion?
- Is the observed difference statistically significant, and should it be shipped?

**Operations**
- Does delivery time affect repeat purchase behavior?
- Which locations show weaker performance?

---

## Architecture

```
RAW DATA (Olist dataset + synthetic tables)
        │
        ▼
     AWS S3 (raw + processed storage)
        │
        ▼
  Databricks / PySpark  ← ETL, cleaning, feature engineering
        │
        ▼
  Processed Delta Tables
        │
   ┌────┴─────┐
   ▼          ▼
Statistical   ML Models
Analysis      (Churn Prediction)
   │          │
   └────┬─────┘
        ▼
   A/B Testing
        │
        ▼
    Power BI Dashboards
        │
        ▼
  Business Recommendations
```

---

## Tech Stack

| Layer | Tools |
|---|---|
| Storage | AWS S3 |
| Data Engineering | Apache Spark (PySpark), Databricks, ETL/ELT |
| Analytics | SQL (Spark SQL), Power BI, DAX |
| Statistics & Experimentation | Hypothesis testing, confidence intervals, A/B testing, effect size (Cohen's d/h) |
| Machine Learning | Scikit-learn, XGBoost, SHAP |
| Core | Python, Pandas, NumPy, SciPy |
| Version Control | Git, GitHub |

---

## Data

Base dataset: [Olist Brazilian E-Commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (Kaggle) — real e-commerce transaction data.

**Synthetically generated tables** (clearly labeled, not real company data):
- `sessions` — simulated clickstream data for funnel analysis.
- `experiments` — simulated A/B test assignment and outcome data, with a deliberate conversion uplift built in for the treatment group.

Raw and processed data are not committed to this repository due to size. See `data/raw/` and `data/processed/` for regeneration instructions.

---

## Project Structure

```
MarketPulse/
├── data/
│   ├── raw/            # raw CSVs (not committed)
│   └── processed/      # exported tables for Power BI (not committed)
├── notebooks/
│   ├── 01_data_ingestion.ipynb
│   ├── 02_spark_etl.ipynb
│   ├── 03_sql_analysis.ipynb
│   ├── 04_statistical_analysis.ipynb
│   ├── 05_ab_testing.ipynb
│   ├── 06_churn_model.ipynb
│   └── 07_export_for_powerbi.ipynb
├── dashboards/
│   └── MarketPulse_Dashboards.pbix
├── requirements.txt
└── README.md
```

---

## Methodology

1. **Data Ingestion** — explored raw Olist tables; documented nulls, dtypes, and order status breakdown.
2. **PySpark ETL** — cleaned nulls/duplicates/invalid records, joined tables, engineered RFM features. Two real bugs caught and fixed: item-level payment double-counting, and `customer_id` vs `customer_unique_id` grain mismatch.
3. **SQL Analytics** — monthly revenue, cohort retention (30/60/90-day), conversion funnel, customer/product rankings via window functions.
4. **Statistical Analysis** — descriptive stats, distribution visualization, hypothesis testing (voucher usage vs. order value), correlation analysis (delivery time and review score vs. repeat purchase), with explicit correlation-vs-causation and statistical-vs-practical-significance discipline throughout.
5. **A/B Testing** — full experiment workflow on a simulated checkout redesign: primary metric (conversion rate), secondary metric (revenue per user), two-proportion z-test, confidence intervals, effect size (Cohen's h), and a ship/no-ship recommendation.
6. **Churn Prediction** — Logistic Regression, Random Forest, and XGBoost compared on precision/recall/F1/ROC-AUC; Random Forest selected as primary model; SHAP used for interpretability.
7. **Power BI Dashboards** — Executive Overview, Customer & Product Analytics, and Experimentation Results.
8. **Business Recommendations** — below, grounded in the actual results above.

---

## Results

### Revenue & Growth
Monthly revenue grew from near-zero in late 2016 to a peak of ~₹11.5L in November 2017 (~7,289 orders), consistent with a growing marketplace and likely seasonal effects. Total revenue across ~96,462 delivered orders: **₹15.42M**, average order value **₹159.85**.

### Retention
Only ~3% of customers ever place a second order. 90-day cohort retention sits in the 1–2.5% range across most cohorts — this is a low-repeat marketplace, not a subscription-style business. Neither delivery time (r=-0.0044, p=0.175) nor review score (r=0.0072, p=0.027 but practically negligible) showed a meaningful relationship with repeat-purchase behavior on their own, suggesting repeat purchase is driven by factors not captured in this dataset.

### Discount/Voucher Effect
Voucher-paid orders have significantly lower average value (₹131.02 vs. ₹161.00, p≈0.000000), though the effect size is small (Cohen's d=-0.2229). This is correlational, not causal — vouchers may be used more on smaller purchases rather than causing lower spend.

### A/B Test — Checkout Redesign
Treatment increased conversion from 9.83% to 13.03% (Z=7.10, p<0.001, non-overlapping 95% CIs), with no significant difference in average order value between converters (p=0.52) — meaning the lift isn't a tradeoff against spend. Revenue per user rose ~35% (₹11.81 → ₹15.95). **Recommendation: ship**, while noting the standardized effect size (Cohen's h=0.10) indicates a modest, not dramatic, real-world impact.

### Churn Model
Random Forest selected as the primary model (ROC-AUC 0.710, Precision 0.705, Recall 0.734, F1 0.719) over Logistic Regression (weaker on all metrics) and XGBoost (higher recall at 0.814 but lower precision and ROC-AUC). SHAP analysis shows `avg_order_value` and `monetary_value` as the strongest churn predictors, with a smaller signal from `avg_delivery_days` that wasn't detectable in the simple bivariate correlation test — an example of a multivariate model surfacing a weaker signal that pairwise correlation missed.

**Known limitations:** the model was compared across defaults only — no hyperparameter tuning or cross-validation was performed. `monetary_value` and `avg_order_value` are correlated by construction, limiting how independently their SHAP contributions should be interpreted.

---

## Business Recommendations

1. **Ship the checkout redesign.** The conversion lift is statistically robust and translates to a real ~35% revenue-per-user increase with no evidence of an offsetting cost. Expectations should be calibrated to a modest, not transformative, real-world impact given the standardized effect size.

2. **Retention is the platform's biggest opportunity, not an already-solved problem.** With ~97% of customers never returning, and neither delivery speed nor review score showing meaningful predictive power over repeat purchase, further investment in understanding *why* customers don't return (pricing, assortment, life-stage repurchase timing) is likely higher-leverage than incremental service-quality improvements alone.

3. **Use the churn model to prioritize retention spend, not as a standalone decision-maker.** High `avg_order_value` and `monetary_value` customers are flagged as higher churn risk — this is counterintuitive and worth validating with the business before acting on it, since it may reflect "big one-time purchase" behavior rather than a generalizable pattern.

4. **Treat the voucher finding as a segmentation insight, not a pricing lever on its own.** Lower order value among voucher users is a real, modest association — useful for understanding who uses vouchers, not sufficient evidence that vouchers reduce spend.

5. **Next steps for a production version:** hyperparameter-tune the churn model and validate with cross-validation, expose the model via a deployed API rather than a notebook, and build out the cohort retention matrix as a full interactive Power BI visual rather than the current summary table.

---

## How to Run

1. Download the Olist dataset from Kaggle and place CSVs in `data/raw/`.
2. Run the synthetic data generation script to create `sessions` and `experiments` tables.
3. Upload `data/raw/` contents to an S3 bucket.
4. Run notebooks in Databricks in numerical order (`01` through `07`).
5. Open `dashboards/MarketPulse_Dashboards.pbix` in Power BI Desktop, pointing at the exported CSVs in `data/processed/`.

---

## Disclaimer

This project uses a real public dataset (Olist) supplemented with synthetically generated data for the sessions and experimentation tables, clearly noted above. No proprietary or real company data is used.
