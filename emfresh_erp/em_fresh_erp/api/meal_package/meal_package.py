import frappe
from frappe import _

@frappe.whitelist()  
def get_meals():
    try:
        
        meals = frappe.get_all('EFE Meal Package', fields=["*"])

        
        return {
            "status": "success",
            "meals": meals
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
