"""Generate a small, clearly synthetic retail transaction dataset."""
from pathlib import Path
import csv
import random
from datetime import date, timedelta

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "retail_transactions_sample.csv"
random.seed(42)

categories = {
    "Grocery": [("P100", 35.0), ("P101", 80.0), ("P102", 120.0)],
    "Home": [("P200", 250.0), ("P201", 499.0), ("P202", 899.0)],
    "Electronics": [("P300", 799.0), ("P301", 1499.0), ("P302", 2499.0)],
    "Apparel": [("P400", 299.0), ("P401", 599.0), ("P402", 999.0)],
}
customers = [f"C{i:03d}" for i in range(1, 31)]
start = date(2026, 8, 1)
rows = []
for i in range(1, 301):
    day = start + timedelta(days=random.randint(0, 60))
    category = random.choice(list(categories))
    product_id, price = random.choice(categories[category])
    channel = random.choice(["Store", "Online"])
    rows.append({
        "transaction_id": f"T{i:05d}",
        "transaction_date": day.isoformat(),
        "customer_id": random.choice(customers),
        "product_id": product_id,
        "category": category,
        "quantity": random.randint(1, 5),
        "unit_price": round(price * random.uniform(0.85, 1.15), 2),
        "discount_pct": random.choice([0.0, 0.0, 0.05, 0.10, 0.15]),
        "sales_channel": channel,
        "store_id": random.choice(["S01", "S02", "S03"]) if channel == "Store" else "ONLINE",
    })

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)
print(f"Wrote {len(rows)} synthetic transaction rows to {OUT}")
