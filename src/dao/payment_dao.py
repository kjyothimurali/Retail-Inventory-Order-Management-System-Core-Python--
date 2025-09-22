# src/dao/payment_dao.py
from src.config import get_supabase


class PaymentDao:
    

    def create_payment(self, order_id: int, amount: float):
        sb = get_supabase()
        data = {
            "order_id": order_id,
            "amount": amount,
            "status": "PENDING"
        }
        res = sb.table("payments").insert(data).execute()
        return res.data[0] if res.data else None

    def update_payment(self, order_id: int, status: str, method: str = None):
        sb = get_supabase()

        update_data = {"status": status}
        if method:
            update_data["method"] = method
        res = (
            sb.table("payments")
            .update(update_data)
            .eq("order_id", order_id)
            .execute()
        )
        return res.data[0] if res.data else None

    def get_payment(self, order_id: int):
        sb = get_supabase()

        res = sb.table("payments").select("*").eq("order_id", order_id).execute()
        return res.data[0] if res.data else None
    
    