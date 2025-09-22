# src/services/product_service.py
from typing import List, Dict
from src.dao.product_dao import ProductDao

pdao=ProductDao()
class ProductError(Exception):
    pass
 
class ProductService:
    
    def add_product(self,name: str, sku: str, price: float, stock: int = 0, category: str | None = None) -> Dict:
        """
        Validate and insert a new product.
        Raises ProductError on validation failure.
        """
        
        if price <= 0:
            raise ProductError("Price must be greater than 0")
        existing = pdao.get_product_by_sku(sku)
        if existing:
            raise ProductError(f"SKU already exists: {sku}")
        return pdao.create_product(name, sku, price, stock, category)
 
    def restock_product(self,prod_id: int, delta: int) -> Dict:
        if delta <= 0:
            raise ProductError("Delta must be positive")
        p = pdao.get_product_by_id(prod_id)
        if not p:
            raise ProductError("Product not found")
        new_stock = (p.get("stock") or 0) + delta
        return pdao.update_product(prod_id, {"stock": new_stock})
 
    def get_low_stock(self,threshold: int = 5) -> List[Dict]:
        
        allp = pdao.list_products(limit=1000)
        return [p for p in allp if (p.get("stock") or 0) <= threshold]
      

    def list_products(self, limit=100):
        # Assuming your DAO has a get_all_products method
        return pdao.list_products(limit=limit)

 
 