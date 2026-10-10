# Week 2 — Retail Data Pipeline Architecture and Implementation Plan

## Objective
Design a practical end-to-end pipeline for ingesting, validating, cleaning, integrating, and storing retail data for analytics and future machine-learning tasks. This is a proposed design for a hypothetical retailer; production connections are not claimed as implemented.

## Architecture flow
```text
POS / E-commerce / Product / Inventory / Public datasets
                         |
                         v
               Ingestion connectors
           CSV / API / SQL extract / file drop
                         |
                         v
               Raw immutable landing
                         |
                         v
             Schema and quality checks
                 /              \
                v                v
         Quarantine/errors   Accepted records
                                  |
                                  v
                       Cleaning and transforms
                                  |
                                  v
                        Curated analytical layer
                                  |
                  +---------------+---------------+
                  v               v               v
              BI reports     ML feature sets   Exports/API

Cross-cutting: logs, metrics, lineage, access control, retries,
scheduling, alerts, configuration, and documentation.
```

## Sources and ingestion
- POS transaction exports: scheduled CSV/Excel or read-only SQL extract.
- E-commerce orders: approved REST API or scheduled export.
- Product catalogue and inventory: API or database extracts.
- Promotions/pricing: CSV, API, or database.
- Public retail datasets: use only after reviewing licence, schema, and limitations.
- Prototype input: clearly labelled synthetic transaction data in `data/`.

## Processing stages
1. **Ingest:** attach source, run ID, ingestion timestamp, and checksum where practical.
2. **Raw landing:** preserve original inputs to support audit and reprocessing.
3. **Validate:** check schema, required fields, types, dates, duplicates, ranges, and keys.
4. **Quarantine:** retain invalid records with source identifiers and rejection reasons.
5. **Transform:** standardise names and labels, parse dates, safely convert numeric values, deduplicate using documented business keys, and derive sales measures.
6. **Integrate:** join transactions with product, store, promotion, and inventory dimensions; report unmatched keys and unexpected join cardinality.
7. **Curate and publish:** provide documented CSV/Parquet files or SQL tables for BI and model development.

## Tools
- Python 3.10+, Pandas, NumPy for the MVP.
- CSV/JSON initially; Parquet for larger analytical files.
- SQLite/PostgreSQL for a small relational store; cloud object storage and an analytical warehouse for scale.
- Python validation functions initially; consider Pandera or Great Expectations for stronger data contracts.
- On-demand execution initially; cron/GitHub Actions for a controlled demo; Airflow or Prefect for more complex scheduled dependencies.
- Git/GitHub for version control; never commit credentials or tokens.

## Reliability and error handling
- Use bounded exponential-backoff retries for temporary API/network errors.
- Treat authentication and schema failures as actionable errors, not infinite retries.
- Log run ID, source, stage, duration, row counts, and error category; exclude secrets.
- Make runs idempotent using stable business keys and file/run identifiers.
- Reconcile input/output counts and sales totals; block publication when critical quality gates fail.
- Track accepted, rejected, and transformed row counts for every run.

## Scheduling and scalability
The prototype runs on demand. Future schedules may follow POS daily close, more frequent e-commerce refreshes, and agreed inventory snapshots. Enforce ingestion → validation → transformation → publication dependencies and display last-successful-refresh time. Begin with local processing; use chunking and Parquet as needed; introduce incremental loads and distributed compute only when measured data volume and runtime justify the added complexity.

## Acceptance criteria
- Repeat runs do not create duplicate records.
- Required fields and data types are validated.
- Invalid rows are quarantined with reasons.
- Logs report input, accepted, rejected, and output counts.
- Critical validation failures prevent unreliable publication.
- Setup, execution, output expectations, and synthetic-data limitations are documented.

## Assumptions and privacy
Real operational integrations require approved access, stable source identifiers, clear data ownership, and documented refresh schedules. Minimise customer data, apply least-privilege access, protect secrets, and follow retention and licence requirements. The architecture is a design plan, not evidence of production deployment.
