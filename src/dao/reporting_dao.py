# src/dao/reporting_dao.py
from src.config import get_supabase
from collections import Counter

class ReportingDao:
    def __init__(self):
        self.sb = get_supabase()

    def top_selling_products(self, limit=5):
        # Fetch all order_items
        result = self.sb.table("order_items").select("*").execute()
        items = result.data

        # Count total quantity per product
        counter = Counter()
        for item in items:
            counter[item["prod_id"]] += item["quantity"]

        # Get top N products
        top = counter.most_common(limit)

        # Fetch product names
        prod_ids = [prod_id for prod_id, _ in top]
        prods_res = self.sb.table("products_retail").select("*").in_("prod_id", prod_ids).execute()
        products = {p["prod_id"]: p for p in prods_res.data}

        # Return list of dicts
        return [{"prod_id": pid, "name": products[pid]["name"], "total_qty": qty} for pid, qty in top]

    def total_revenue_last_month(self):
        from datetime import datetime, timedelta
        now = datetime.utcnow()
        first_day = datetime(now.year, now.month, 1)
        last_month_last_day = first_day - timedelta(days=1)
        last_month_first_day = datetime(last_month_last_day.year, last_month_last_day.month, 1)

        result = self.sb.table("orders")\
            .select("total_amount, order_date")\
            .gte("order_date", last_month_first_day.isoformat())\
            .lte("order_date", last_month_last_day.isoformat())\
            .execute()

        total = sum([o["total_amount"] for o in result.data])
        return total

    def total_orders_per_customer(self):
        result = self.sb.table("orders").select("*").execute()
        counts = {}
        for o in result.data:
            counts[o["cust_id"]] = counts.get(o["cust_id"], 0) + 1
        return counts

    def customers_with_multiple_orders(self, min_orders=2):
        counts = self.total_orders_per_customer()
        return [cust_id for cust_id, c in counts.items() if c > min_orders]
