# Retail Intelligence & Customer Analytics Platform

**Internship project:** Retail Data Science Solution Architect  
**Author:** Pawan Jogi  
**Current phase:** Week 1 — Strategy and Requirements Analysis

A portfolio project blueprint for a hypothetical retailer. The repository starts with a small **synthetic sample dataset** so the workflow can be demonstrated without exposing private customer data. Replace it with a properly licensed public retail dataset or authorized business data before drawing real-world conclusions.

## Project goals
- Define retail business requirements and KPIs.
- Load, validate, clean, and summarize transaction data.
- Create repeatable Python workflows and document assumptions.
- Extend in later phases to a full pipeline, forecasting, customer segmentation, recommendations, and deployment monitoring.

## Repository structure
```text
Retail_Intelligence_Customer_Analytics/
├── data/
│   └── retail_transactions_sample.csv
├── reports/
│   └── week1_requirements.md
├── src/
│   ├── generate_sample_data.py
│   └── retail_analysis.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup
Python 3.10+ recommended.

```bash
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows:
# .venv\Scripts\activate

pip install -r requirements.txt
python src/retail_analysis.py
```

The script reads `data/retail_transactions_sample.csv`, validates expected columns, reports missing values and duplicates, creates a cleaned file under `data/processed/`, and writes summary tables to `reports/output/`.

## Dataset fields
- `transaction_id`: unique transaction-line identifier
- `transaction_date`: transaction date
- `customer_id`: pseudonymous sample customer ID
- `product_id`: product identifier
- `category`: product category
- `quantity`: units sold
- `unit_price`: selling price per unit
- `discount_pct`: discount fraction from 0 to 1
- `sales_channel`: `Store` or `Online`
- `store_id`: store code; `ONLINE` for online orders

## KPIs in this prototype
- Gross sales before discount = `quantity × unit_price`
- Net sales after discount = `quantity × unit_price × (1 − discount_pct)`
- Units sold
- Transaction-line count
- Sales by category, channel, and date

**Limitations:** The sample is synthetic and small. It has no actual inventory, cost/margin, returns, campaign exposure, or real customer demographics. Do not claim production performance or business impact from this demo.

## Week 1 deliverable
See `reports/week1_requirements.md` and the accompanying Word report. Future weeks should build on this repository rather than create disconnected assignments.
