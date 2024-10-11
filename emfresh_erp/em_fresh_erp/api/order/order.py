import frappe
from frappe import _

@frappe.whitelist()  
def get_orders():
    try:
        
        orders = frappe.get_all('EFE Order', fields=["*"])

        
        return {
            "status": "success",
            "orders": orders
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
