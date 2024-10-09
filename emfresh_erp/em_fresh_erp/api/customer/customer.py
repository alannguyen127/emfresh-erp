import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)  # Đánh dấu phương thức này là có thể gọi từ bên ngoài qua API
def get_customers():
    try:
        # Lấy tất cả khách hàng từ doctype Customer
        customers = frappe.get_all('EFE Customer', fields=["*"])

        # Trả về kết quả dưới dạng JSON
        return {
            "status": "success",
            "customers": customers
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
