# src/cli/main.py
import argparse
import json

from src.services.customer_service import CustomerService
from src.services import order_service
from src.services.product_service import ProductService
from src.services.payment_service import PaymentService
from src.services.reporting_service import ReportingService


po = ProductService()
payo=PaymentService()


co=CustomerService()
def cmd_product_add(args):
    try:
        
        p = po.add_product(args.name, args.sku, args.price, args.stock, args.category)
        print("Created product:")
        print(json.dumps(p, indent=2, default=str))
    except Exception as e:
        print("Error:", e)
 
def cmd_product_list(args):
    
    ps = po.list_products(limit=100)
    print(json.dumps(ps, indent=2, default=str))
 
def cmd_customer_add(args):
    try:
        c = co.add_customer(args.name, args.email, args.phone, args.city)
        print("Created customer:")
        print(json.dumps(c, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_customer_update_phone(args):
    try:
        c = co.update_phone(args.id, args.phone)
        print("Updated customer:")
        print(json.dumps(c, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_customer_delete(args):
    from src.services.customer_service import CustomerService
    service = CustomerService()
    try:
        deleted = service.delete_customer(args.id)
        if deleted:
            print(f"Customer {args.id} deleted successfully.")
        else:
            print(f"No customer found with ID {args.id}.")
    except ValueError as e:
        print(f"{e}")

 
def cmd_order_create(args):
    from src.services.order_service import OrderService
    service = OrderService()

    # Parse items from prod_id:qty strings
    products = []
    try:
        for s in args.item:
            if ":" not in s:
                raise ValueError(f"Invalid item format: {s}")
            prod_id_str, qty_str = s.split(":")
            products.append({"prod_id": int(prod_id_str), "qty": int(qty_str)})
    except ValueError as e:
        print(f"Error parsing items: {e}")
        return

    try:
        result = service.create_order(args.customer, products)
        print(f"Order created successfully: {result}")
    except ValueError as e:
        print(f"Error: {e}")

 
def cmd_order_show(args):
    try:
        o = order_service.get_order_details(args.order)
        print(json.dumps(o, indent=2, default=str))
    except Exception as e:
        print("Error:", e)
 
def cmd_order_cancel(args):
    try:
        o = order_service.cancel_order(args.order)
        print("Order cancelled (updated):")
        print(json.dumps(o, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_order_list(args):
    from src.services.order_service import OrderService
    service = OrderService()
    try:
        orders = service.list_orders_for_customer(args.customer)
        print(json.dumps(orders, indent=2, default=str))
    except Exception as e:
        print("Error:", e)


def cmd_order_complete(args):
    from src.services.order_service import OrderService
    service = OrderService()
    try:
        result = service.mark_order_completed(args.order)
        print("Order marked as completed:")
        print(json.dumps(result, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_payment_pay(args):
    from src.services.payment_service import PaymentService
    service = PaymentService()
    try:
        result = service.process_payment(args.order, args.method)
        print(f"Payment successful: {result}")
    except Exception as e:
        print(f"Error: {e}")

def cmd_payment_refund(args):
    from src.services.payment_service import PaymentService
    ps = PaymentService()
    try:
        res = ps.refund_order(args.order)
        print("Payment refunded:", res)
    except Exception as e:
        print("Error:", e)


 
def build_parser():
    parser = argparse.ArgumentParser(prog="retail-cli")
    sub = parser.add_subparsers(dest="cmd")
 
    # product add/list
    p_prod = sub.add_parser("product", help="product commands")
    pprod_sub = p_prod.add_subparsers(dest="action")
    addp = pprod_sub.add_parser("add")
    addp.add_argument("--name", required=True)
    addp.add_argument("--sku", required=True)
    addp.add_argument("--price", type=float, required=True)
    addp.add_argument("--stock", type=int, default=0)
    addp.add_argument("--category", default=None)
    addp.set_defaults(func=cmd_product_add)
 
    listp = pprod_sub.add_parser("list")
    listp.set_defaults(func=cmd_product_list)
 
    # customer add
    pcust = sub.add_parser("customer")
    pcust_sub = pcust.add_subparsers(dest="action")
    addc = pcust_sub.add_parser("add")
    addc.add_argument("--name", required=True)
    addc.add_argument("--email", required=True)
    addc.add_argument("--phone", required=True)
    addc.add_argument("--city", default=None)
    addc.set_defaults(func=cmd_customer_add)

    # customer update
    
    update_parser = pcust_sub.add_parser("update-phone")
    update_parser.add_argument("--id", type=int, required=True)
    update_parser.add_argument("--phone", required=True)
    update_parser.set_defaults(func=cmd_customer_update_phone) 

    # customer delete
    del_parser = pcust_sub.add_parser("delete")
    del_parser.add_argument("--id", type=int, required=True)
    del_parser.set_defaults(func=cmd_customer_delete)

 
    # order
    porder = sub.add_parser("order")
    porder_sub = porder.add_subparsers(dest="action")
 

    createo = porder_sub.add_parser("create")
    createo.add_argument("--customer", type=int, required=True)
    createo.add_argument("--item", required=True, nargs="+", help="prod_id:qty (repeatable)")
    createo.set_defaults(func=cmd_order_create)

    showo = porder_sub.add_parser("show")
    showo.add_argument("--order", type=int, required=True)
    showo.set_defaults(func=cmd_order_show)

    listo = porder_sub.add_parser("list")
    listo.add_argument("--customer", type=int, required=True)
    listo.set_defaults(func=cmd_order_list)

    cano = porder_sub.add_parser("cancel")
    cano.add_argument("--order", type=int, required=True)
    cano.set_defaults(func=cmd_order_cancel)

    completeo = porder_sub.add_parser("complete")
    completeo.add_argument("--order", type=int, required=True)
    completeo.set_defaults(func=cmd_order_complete)

    # payment
    ppayment = sub.add_parser("payment", help="payment commands")
    ppayment_sub = ppayment.add_subparsers(dest="action")

    # Pay for order
    ppay = ppayment_sub.add_parser("pay")
    ppay.add_argument("--order", type=int, required=True)
    ppay.add_argument("--method", type=str, required=True, choices=["Cash","Card","UPI"])
    ppay.set_defaults(func=cmd_payment_pay)

    # Refund payment
    prefund = ppayment_sub.add_parser("refund")
    prefund.add_argument("--order", type=int, required=True)
    prefund.set_defaults(func=cmd_payment_refund)

    # Reporting CLI
    preport = sub.add_parser("report", help="sales reports")
    preport_sub = preport.add_subparsers(dest="action")

    # Top products
    topprod = preport_sub.add_parser("top-products")
    topprod.set_defaults(func=lambda args: print(ReportingService().top_selling_products()))

    # Revenue last month
    rev = preport_sub.add_parser("revenue-last-month")
    rev.set_defaults(func=lambda args: print(ReportingService().total_revenue_last_month()))

    # Orders per customer
    orders_per_cust = preport_sub.add_parser("orders-per-customer")
    orders_per_cust.set_defaults(func=lambda args: print(ReportingService().total_orders_per_customer()))

    # Customers with >2 orders
    multi_cust = preport_sub.add_parser("multi-order-customers")
    multi_cust.set_defaults(func=lambda args: print(ReportingService().customers_with_multiple_orders(2)))



 
    return parser




 
def main():
    parser = build_parser()
    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        return
    args.func(args)
 
if __name__ == "__main__":
    main()