import frappe
from frappe import _
from frappe.utils import flt, getdate, add_days

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

@frappe.whitelist()
def get_sales_data_by_date(start_date, end_date):
    if not start_date or not end_date:
        frappe.throw("Start Date and End Date are required")
    
    # Chuyển đổi start_date và end_date sang định dạng ngày
    start_date = getdate(start_date)
    end_date = getdate(end_date)
    
    # Để bao gồm cả order trong ngày end_date, ta tăng end_date lên thêm 1 ngày và lấy đến trước 00:00:00 của ngày sau
    adjusted_end_date = add_days(end_date, 1)
    
    sales_data = frappe.db.sql("""
        SELECT 
            DATE(order_date) as order_date,
            SUM(total_amount) as total_sales
        FROM `tabEFE Order`
        WHERE 
            order_date >= %s AND order_date < %s
        GROUP BY DATE(order_date)
        ORDER BY order_date ASC
    """, (start_date, adjusted_end_date), as_dict=True)
    
 
    return {
        "sales_data": sales_data
    }
