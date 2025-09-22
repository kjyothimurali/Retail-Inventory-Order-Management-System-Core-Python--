from src.config import get_supabase

class OrderDao:
    
    def check_customer_exists(self, cust_id):
        sb = get_supabase()  # ← call the function to get client
        result = sb.table("customers").select("*").eq("cust_id", cust_id).execute()
        return len(result.data) > 0

    def get_products_by_ids(self, prod_ids):
        sb = get_supabase()
        result = sb.table("products_retail").select("*").in_("prod_id", prod_ids).execute()
        return {p["prod_id"]: p for p in result.data}

    def update_product_stock(self, prod_id, new_stock):
        sb = get_supabase()
        sb.table("products_retail").update({"stock": new_stock}).eq("prod_id", prod_id).execute()

    def create_order(self, cust_id, order_items, total_amount):
        sb = get_supabase()
        order_res = sb.table("orders").insert({"cust_id": cust_id, "total_amount": total_amount}).execute()
        order_id = order_res.data[0]["order_id"]
        for item in order_items:
            sb.table("order_items").insert({
                "order_id": order_id,
                "prod_id": item["product_id"],
                "quantity": item["quantity"],
                "price": item["price"]
            }).execute()
        return order_id

    def list_products(self, limit=100):
        sb = get_supabase()
        result = sb.table("products_retail").select("*").limit(limit).execute()
        return result.data
    def get_order_details(self, order_id):
        sb = get_supabase()
        # Fetch order info
        order_res = sb.table("orders").select("*").eq("order_id", order_id).execute()
        if not order_res.data:
            return None
        order = order_res.data[0]
        # Fetch customer info
        cust_res = sb.table("customers").select("*").eq("cust_id", order["cust_id"]).execute()
        customer = cust_res.data[0] if cust_res.data else None
        # Fetch order items
        items_res = sb.table("order_items").select("*").eq("order_id", order_id).execute()
        return {"order": order, "customer": customer, "items": items_res.data}

    def list_orders_by_customer(self, cust_id):
        sb = get_supabase()
        return sb.table("orders").select("*").eq("cust_id", cust_id).execute().data

    def update_order_status(self, order_id, status):
        sb = get_supabase()
        sb.table("orders").update({"status": status}).eq("order_id", order_id).execute()

    def get_order_items(self, order_id):
        sb = get_supabase()
        return sb.table("order_items").select("*").eq("order_id", order_id).execute().data
    
    def get_order(self, order_id):
        sb = get_supabase()
        result = sb.table("orders").select("*").eq("order_id", order_id).execute()
        return result.data[0] if result.data else None
