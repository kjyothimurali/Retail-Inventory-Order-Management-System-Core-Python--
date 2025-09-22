# src/services/reporting_service.py
from src.dao.reporting_dao import ReportingDao

class ReportingService:
    def __init__(self):
        self.dao = ReportingDao()

    def top_selling_products(self, limit=5):
        return self.dao.top_selling_products(limit=limit)

    def total_revenue_last_month(self):
        return self.dao.total_revenue_last_month()

    def total_orders_per_customer(self):
        return self.dao.total_orders_per_customer()

    def customers_with_multiple_orders(self, min_orders=2):
        return self.dao.customers_with_multiple_orders(min_orders=min_orders)
