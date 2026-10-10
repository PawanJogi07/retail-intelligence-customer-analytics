"""Validate and summarize the synthetic retail transaction sample."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "retail_transactions_sample.csv"
PROCESSED = ROOT / "data" / "processed"
OUTPUT = ROOT / "reports" / "output"

REQUIRED = [
    "transaction_id", "transaction_date", "customer_id", "product_id",
    "category", "quantity", "unit_price", "discount_pct", "sales_channel", "store_id"
]

def main():
    if not INPUT.exists():
        raise FileNotFoundError(
            f"Dataset not found: {INPUT}. Run `python src/generate_sample_data.py` first."
        )

    df = pd.read_csv(INPUT)
    missing_columns = sorted(set(REQUIRED) - set(df.columns))
    if missing_columns:
        raise ValueError(f"Required columns missing: {missing_columns}")

    print("=== DATA PROFILE ===")
    print(f"Input rows: {len(df)}")
    print("\nMissing values by column:")
    print(df[REQUIRED].isna().sum().to_string())
    print(f"\nExact duplicate rows: {int(df.duplicated().sum())}")
    print(f"Duplicate transaction IDs: {int(df['transaction_id'].duplicated().sum())}")

    df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")
    for col in ["quantity", "unit_price", "discount_pct"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    valid = (
        df["transaction_id"].notna()
        & df["transaction_date"].notna()
        & df["product_id"].notna()
        & df["category"].notna()
        & df["quantity"].notna()
        & df["unit_price"].notna()
        & df["discount_pct"].notna()
        & (df["quantity"] >= 0)
        & (df["unit_price"] >= 0)
        & df["discount_pct"].between(0, 1)
    )
    clean = df.loc[valid].drop_duplicates(subset=["transaction_id"]).copy()
    clean["gross_sales"] = clean["quantity"] * clean["unit_price"]
    clean["net_sales"] = clean["gross_sales"] * (1 - clean["discount_pct"])
    clean["transaction_date"] = clean["transaction_date"].dt.strftime("%Y-%m-%d")

    PROCESSED.mkdir(parents=True, exist_ok=True)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    clean.to_csv(PROCESSED / "retail_transactions_clean.csv", index=False)

    daily = clean.groupby("transaction_date", as_index=False).agg(
        net_sales=("net_sales", "sum"),
        units_sold=("quantity", "sum"),
        transaction_lines=("transaction_id", "count"),
    )
    by_category = clean.groupby("category", as_index=False).agg(
        net_sales=("net_sales", "sum"),
        units_sold=("quantity", "sum"),
        transaction_lines=("transaction_id", "count"),
    ).sort_values("net_sales", ascending=False)
    by_channel = clean.groupby("sales_channel", as_index=False).agg(
        net_sales=("net_sales", "sum"),
        units_sold=("quantity", "sum"),
        transaction_lines=("transaction_id", "count"),
    ).sort_values("net_sales", ascending=False)

    daily.to_csv(OUTPUT / "daily_kpis.csv", index=False)
    by_category.to_csv(OUTPUT / "category_kpis.csv", index=False)
    by_channel.to_csv(OUTPUT / "channel_kpis.csv", index=False)

    print("\n=== SUMMARY ===")
    print(f"Valid rows retained: {len(clean)}")
    print(f"Rows removed by validation/deduplication: {len(df) - len(clean)}")
    print(f"Total units sold: {clean['quantity'].sum():,.0f}")
    print(f"Gross sales: {clean['gross_sales'].sum():,.2f}")
    print(f"Net sales after discount: {clean['net_sales'].sum():,.2f}")
    print("\nNet sales by category:")
    print(by_category.to_string(index=False))
    print("\nNet sales by channel:")
    print(by_channel.to_string(index=False))
    print(f"\nClean data: {PROCESSED / 'retail_transactions_clean.csv'}")
    print(f"Summary reports: {OUTPUT}")

if __name__ == "__main__":
    main()
