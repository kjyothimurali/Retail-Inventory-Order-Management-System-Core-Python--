# src/dao/customer_dao.py
from typing import Optional, List, Dict
from src.config import get_supabase
class CustomerDao:
 
    def _sb(self):
        return get_supabase()
 
    def create_customer(self,name: str, email: str, phone: int, city: str) -> Optional[Dict]:
        """
        Insert a product and return the inserted row (two-step: insert then select by unique sku).
        """
        payload = {"name": name, "email": email, "phone": phone, "city": city}
        
 
        # Insert (no select chaining)
        self._sb().table("customers").insert(payload).execute()
 
        # Fetch inserted row by unique column (email)
        resp = self._sb().table("customers").select("*").eq("email", email).limit(1).execute()
        return resp.data[0] if resp.data else None
 
    def get_customer_by_id(self,cust_id: int) -> Optional[Dict]:
        resp = self._sb().table("customers").select("*").eq("cust_id", cust_id).limit(1).execute()
        return resp.data[0] if resp.data else None
 
    def get_customer_by_email(self,email: str) -> Optional[Dict]:
        resp = self._sb().table("customers").select("*").eq("email", email).limit(1).execute()
        return resp.data[0] if resp.data else None
 
    def update_phone(self,cust_id: int, fields: Dict) -> Optional[Dict]:
        """
        Update and then return the updated row (two-step).
        """
        self._sb().table("customers").update(fields).eq("cust_id", cust_id).execute()
        resp = self._sb().table("customers").select("*").eq("cust_id", cust_id).limit(1).execute()
        return resp.data[0] if resp.data else None
    
    def update_city(self,cust_id: int, fields: Dict) -> Optional[Dict]:
        """
        Update and then return the updated row (two-step).
        """
        self._sb().table("customers").update(fields).eq("cust_id", cust_id).execute()
        resp = self._sb().table("customers").select("*").eq("cust_id", cust_id).limit(1).execute()
        return resp.data[0] if resp.data else None
 
    def delete_customer(self, cust_id: int) -> Optional[Dict]:
        sb = self._sb()

        # ✅ Check if the customer has any orders
        orders = sb.table("orders").select("order_id").eq("cust_id", cust_id).limit(1).execute()
        if orders.data:
            raise ValueError(f"Cannot delete customer {cust_id}: Orders exist for this customer.")

        # ✅ Fetch row before deleting (to return it later)
        resp_before = sb.table("customers").select("*").eq("cust_id", cust_id).limit(1).execute()
        row = resp_before.data[0] if resp_before.data else None

        if row:
            sb.table("customers").delete().eq("cust_id", cust_id).execute()

        return row
 
    def list_customers(self,limit: int = 100) -> List[Dict]:
        q = self._sb().table("customers").select("*").order("cust_id", desc=False).limit(limit)
        
        resp = q.execute()
        return resp.data or []
 
 