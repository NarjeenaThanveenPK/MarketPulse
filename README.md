![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![PySpark](https://img.shields.io/badge/PySpark-Databricks-orange?logo=apachespark&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-S3-orange?logo=amazonaws&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-Dashboards-yellow?logo=powerbi&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

# MarketPulse — E-commerce Product Analytics & Experimentation Platform

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
     AWS S3 (raw storage)
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
| Analytics | SQL (Spark SQL), Power BI, DAX, Power Query |
| Statistics & Experimentation | Hypothesis testing, confidence intervals, A/B testing, experimental design |
| Machine Learning | Scikit-learn, XGBoost, SHAP |
| Core | Python, Pandas, NumPy |
| Version Control | Git, GitHub |

---

## Data

Base dataset: [Olist Brazilian E-Commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (Kaggle) — real e-commerce transaction data including customers, orders, order items, products, payments, and reviews.

**Synthetically generated tables** (clearly labeled, not real company data):
- `sessions` — simulated clickstream data (pages viewed, time on site, cart/checkout events) derived from and extending the order data, including non-converting sessions.
- `experiments` — simulated A/B test assignment and outcome data (variant, exposure date, conversion, revenue) used for the experimentation module.

Raw data is not committed to this repository due to size. See `data/raw/` for download instructions.

---

## Project Structure

```
MarketPulse/
├── data/
│   ├── raw/            # raw CSVs (not committed — see download instructions)
│   └── processed/      # cleaned/processed outputs (not committed)
├── notebooks/
│   ├── 01_data_ingestion.ipynb
│   ├── 02_spark_etl.ipynb
│   ├── 03_sql_analysis.ipynb
│   ├── 04_statistical_analysis.ipynb
│   ├── 05_ab_testing.ipynb
│   └── 06_churn_model.ipynb
├── dashboards/          # Power BI files / exported dashboard images
├── src/                 # reusable scripts (data generation, utils)
├── architecture.png
├── requirements.txt
└── README.md
```

---

## Methodology

1. **Data Ingestion** — load raw and synthetic data into S3, then into Databricks.
2. **PySpark ETL** — clean nulls/duplicates/invalid records, join tables, engineer features (RFM, average order value, conversion rate, repeat purchase rate, delivery time).
3. **SQL Analytics** — monthly revenue, cohort retention (30/60/90-day), conversion funnel, top customers/products via window functions.
4. **Statistical Analysis** — descriptive statistics, distributions, correlation analysis (with explicit correlation-vs-causation caveats), and a formal hypothesis test (e.g., does a discount affect average order value).
5. **A/B Testing** — simulated checkout experiment: hypothesis, primary/secondary metrics, sample size, two-proportion z-test, p-value, confidence interval, effect size, and a ship/no-ship recommendation.
6. **Churn Prediction** — Logistic Regression, Random Forest, and XGBoost models compared on precision/recall/F1/ROC-AUC, interpreted with SHAP.
7. **Power BI Dashboards** — Executive Overview, Customer & Product Analytics, and Experimentation Results.
8. **Business Recommendations** — conclusions grounded in the actual results above.

---

## Results

*(To be filled in as each phase is completed.)*

---

## Business Recommendations

*(To be filled in once experimentation and modeling results are available.)*

---

## How to Run

1. Download the Olist dataset from Kaggle and place CSVs in `data/raw/`.
2. Run `src/generate_synthetic_tables.py` to create the `sessions` and `experiments` tables.
3. Upload `data/raw/` contents to your S3 bucket.
4. Open notebooks in Databricks in numerical order (`01` through `06`).
5. Open dashboard files in Power BI Desktop, pointing at the processed data outputs.

---

## Disclaimer

This project uses a real public dataset (Olist) supplemented with synthetically generated data for the sessions and experimentation tables, clearly noted above. No proprietary or real company data is used.
