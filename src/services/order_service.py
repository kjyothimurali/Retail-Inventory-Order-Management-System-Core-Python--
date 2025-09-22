# src/services/order_service.py
from typing import List, Dict
from src.dao.order_dao import OrderDao
from src.services.payment_service import PaymentService

class OrderError(Exception):
    pass

class OrderService:
    def __init__(self):
        self.dao = OrderDao()  # Initialize DAO here

    def create_order(self, customer_id, products) -> Dict:
        """
        products: list of dicts like [{'prod_id':1,'qty':2}, ...]
        """
        # 1️⃣ Check customer exists
        if not self.dao.check_customer_exists(customer_id):
            raise ValueError(f"Customer {customer_id} does not exist")

        # 2️⃣ Get current product info
        product_ids = [p["prod_id"] for p in products]
        db_products = self.dao.get_products_by_ids(product_ids)

        # 3️⃣ Validate stock and prepare order items
        order_items = []
        total_amount = 0
        for p in products:
            prod_id = p["prod_id"]
            qty = p["qty"]

            if prod_id not in db_products:
                raise ValueError(f"Product {prod_id} does not exist")

            product = db_products[prod_id]
            if product["stock"] < qty:
                raise ValueError(f"Not enough stock for product {product['name']} (requested {qty}, available {product['stock']})")

            # Deduct stock
            new_stock = product["stock"] - qty
            self.dao.update_product_stock(prod_id, new_stock)

            # Prepare order item and total
            order_items.append({"product_id": prod_id, "quantity": qty, "price": product["price"]})
            total_amount += product["price"] * qty

            
        payment_service = PaymentService()
        order_id = self.dao.create_order(customer_id, order_items, total_amount)
        payment_service.create_payment_for_order(order_id, total_amount)
        return {"order_id": order_id, "total_amount": total_amount, "items": order_items}
    
    def get_order_details(self, order_id):
        details = self.dao.get_order_details(order_id)
        if not details:
            raise ValueError(f"Order {order_id} not found")
        return details

    def list_orders_for_customer(self, cust_id):
        return self.dao.list_orders_by_customer(cust_id)

    def cancel_order(self, order_id):
        details = self.dao.get_order_details(order_id)
        if not details:
            raise ValueError(f"Order {order_id} not found")
        if details["order"]["status"] != "PLACED":
            raise ValueError("Only orders with status=PLACED can be cancelled")

        # Restore stock
        items = self.dao.get_order_items(order_id)
        for item in items:
            product = self.dao.get_products_by_ids([item["prod_id"]])[item["prod_id"]]
            self.dao.update_product_stock(item["prod_id"], product["stock"] + item["quantity"])

        # Update order status
        self.dao.update_order_status(order_id, "CANCELLED")
        return {"order_id": order_id, "status": "CANCELLED"}

    def mark_order_completed(self, order_id):
        details = self.dao.get_order_details(order_id)
        if not details:
            raise ValueError(f"Order {order_id} not found")
        if details["order"]["status"] != "PLACED":
            raise ValueError("Only orders with status=PLACED can be marked completed")
        self.dao.update_order_status(order_id, "COMPLETED")
        return {"order_id": order_id, "status": "COMPLETED"}
    

    def list_products(self, limit=100) -> List[Dict]:
        return self.dao.list_products(limit=limit)
