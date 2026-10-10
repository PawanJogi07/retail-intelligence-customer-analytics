# Week 1 — Retail Data Science Strategy and Requirements

## Scenario
This project models a hypothetical mid-sized retailer with physical stores and an online channel. The first objective is to create a trustworthy foundation for retail reporting before adding predictive models.

## Business questions
1. Which product categories and channels generate the most net sales?
2. How do sales vary over time?
3. Which categories have the highest unit volume?
4. What data quality issues need attention before modeling?
5. Which future use cases are feasible with available fields?

## Initial KPIs
- Gross sales: quantity × unit price.
- Net sales: quantity × unit price × (1 − discount percentage).
- Units sold: sum of quantity.
- Transaction-line count: count of valid transaction IDs.
- Category and channel contribution: net sales grouped by category or channel.

Definitions must be agreed with stakeholders before use on real business data. This prototype does not model returns, tax, cost of goods, or inventory availability.

## Technical requirements
- Python and Pandas for ingestion, validation, cleaning, and summaries.
- SQL/database storage can be added after source data and scale are known.
- Power BI can be connected to the cleaned tables in a later phase.
- GitHub must contain code and documentation only; never commit private customer data, credentials, or confidential business files.

## Data requirements and sources
Preferred sources, subject to authorization: POS transactions, e-commerce orders, product master, inventory snapshots, promotion calendar, and returns. If business data is unavailable, use a public dataset only after checking license and data limitations. This repository uses a clearly labeled synthetic sample.

## Data quality checks
- Required columns exist.
- Dates parse correctly.
- Quantity and price are non-negative in this simplified sample.
- Discount fraction is between 0 and 1.
- Transaction IDs are unique.
- Missing values and duplicate rows are reported.

## Risks and controls
- **Incorrect KPI definitions:** document formulas and get stakeholder agreement.
- **Incomplete data:** report nulls and row counts.
- **Privacy:** use pseudonymous IDs and avoid personal identifiers.
- **Misleading conclusions:** label synthetic data and do not generalize from it.
- **Reproducibility:** keep code, requirements, and execution steps in GitHub.

## High-level flow
Sources → ingestion → raw storage → validation/cleaning → curated tables → KPI summaries/dashboard → stakeholder review → iteration.

## Future roadmap
Week 2: pipeline architecture and implementation.  
Week 3: model selection, training, and evaluation.  
Week 4: recommendation-system strategy.  
Week 5: customer forecasting and segmentation.  
Week 6: deployment, monitoring, and reporting.

## Acceptance criteria for Week 1
The strategy documents the business questions, KPIs, data needs, technology choices, validation rules, privacy considerations, risks, and future deliverables. This is a plan and starter prototype, not a production deployment.
