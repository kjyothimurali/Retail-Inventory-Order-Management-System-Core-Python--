# src/services/product_service.py
from typing import  Dict
from src.dao.customer_dao import CustomerDao
cdao=CustomerDao()
 
class CustomerError(Exception):
    pass
 
class CustomerService:
    
    
    def add_customer(self,name: str, email: str, phone: int, city: str) -> Dict:
        """
        Validate and insert a new customer.
        Raises CustomerError on validation failure.
        """
        
        
        existing = cdao.get_customer_by_email(email)
        if existing:
            raise CustomerError(f"Email already exists: {email}")
        return cdao.create_customer(name, email, phone, city)
 
    def update_phone(self,cust_id: int, delta: int) -> Dict:
        
        
        p = cdao.get_customer_by_id(cust_id)
        if not p:
            raise CustomerError("Customer not found")
        new_phone = delta
        return cdao.update_phone(cust_id, {"phone": new_phone})
 
    def update_city(self,cust_id: int, delta: str) -> Dict:
        
        
        p = cdao.get_customer_by_id(cust_id)
        if not p:
            raise CustomerError("Customer not found")
        new_city = delta
        return cdao.update_city(cust_id, {"city": new_city})
    
    def delete_customer(self, cust_id):
        return cdao.delete_customer(cust_id)
      

    def list_products(self, limit=100):
        
        # Assuming your DAO has a get_all_products method
        return cdao.list_products(limit=limit)

 
 