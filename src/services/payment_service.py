# src/services/payment_service.py
from src.dao.payment_dao import PaymentDao
from src.dao.order_dao import OrderDao

class PaymentService:
    def __init__(self):
        self.payment_dao = PaymentDao()
        self.order_dao = OrderDao()

    def create_payment_for_order(self, order_id: int, amount: float):
        return self.payment_dao.create_payment(order_id, amount)

    def process_payment(self, order_id: int, method: str):
        order = self.order_dao.get_order(order_id)
        if not order:
            raise ValueError("Order not found")

        payment = self.payment_dao.get_payment(order_id)
        if not payment:
            raise ValueError("Payment record not found")

        if order["status"] != "PLACED":
            raise ValueError("Order must be PLACED to process payment")

        # Mark as PAID
        updated_payment = self.payment_dao.update_payment(order_id, "PAID", method)
        self.order_dao.update_order_status(order_id, "COMPLETED")
        return updated_payment

    def refund_payment(self, order_id: int):
        payment = self.payment_dao.get_payment(order_id)
        if not payment:
            raise ValueError("Payment record not found")

        if payment["status"] != "PAID":
            raise ValueError("Only PAID payments can be refunded")

        updated_payment = self.payment_dao.update_payment(order_id, "REFUNDED")
        return updated_payment
