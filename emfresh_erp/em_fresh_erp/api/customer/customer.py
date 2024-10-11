import frappe
from frappe import _

@frappe.whitelist() 
def get_customers():
    try:
        customers = frappe.get_all('EFE Customer', fields=["*"])
        return {
            "status": "success",
            "customers": customers
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@frappe.whitelist() 
def get_customer_detail(customer_id):
    try:
        customer_detail = frappe.get_doc('EFE Customer', customer_id)
        return {
            "status": "success",
            "customer_detail": customer_detail
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


@frappe.whitelist()
def create_customer(nick_name, full_name, gender, address_1, status, phone_number):
    try:
        # Tạo mới khách hàng trong Frappe
        new_customer = frappe.get_doc({
            'doctype': 'EFE Customer',
            'nick_name': nick_name,
            'full_name': full_name,
            'phone_number': phone_number,
            'gender': gender,
            'address_1': address_1,
            'status': status,
        })
        new_customer.insert()
        frappe.db.commit()  # Commit thay đổi vào database
        return {
            "status": "success",
            "message": "Customer created successfully"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }