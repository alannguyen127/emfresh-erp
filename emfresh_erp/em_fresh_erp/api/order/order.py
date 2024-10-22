import frappe
from frappe import _
from frappe.utils import getdate, today, add_days, get_first_day, get_last_day
from datetime import timedelta

from frappe.model.document import Document

@frappe.whitelist()  
def get_orders():
    try:
        
        orders = frappe.get_all('EFE Order', fields=["*"])
        # Iterate through each order to replace customer_nick_name with the corresponding nick_name
        for order in orders:
            customer_name = order.get("customer_nick_name")
            
            if customer_name:
                # Fetch the corresponding nick_name from EFE Customer
                customer_info = frappe.get_value("EFE Customer", customer_name, "nick_name")
                
                # Replace the customer_nick_name with the actual nick_name
                order["customer_nick_name"] = customer_info
        
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
        return {
            "status": "error",
            "message": "Start Date and End Date are required",
            "sales_data": []
        }

  
  
    start_date = getdate(start_date)
    end_date = getdate(end_date)
    
  
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

@frappe.whitelist()
def get_total_order_data_by_date(start_date, end_date):
    if not start_date or not end_date:
        return {
            "status": "error",
            "message": "Start Date and End Date are required",
            "total_order_data": []
        }


    start_date = getdate(start_date)
    end_date = getdate(end_date)
    
  
    adjusted_end_date = add_days(end_date, 1)
    
    total_order_data = frappe.db.sql("""
        SELECT 
            COUNT(name) as total_orders,
            SUM(CASE WHEN payment_status = 'COD' THEN 1 ELSE 0 END) as cod_orders,
            SUM(CASE WHEN payment_status = 'Paid' THEN 1 ELSE 0 END) as paid_orders,
            SUM(CASE WHEN payment_status = 'Not yet' THEN 1 ELSE 0 END) as not_yet_orders
        FROM `tabEFE Order`
        WHERE 
            order_date >= %s AND order_date < %s
    """, (start_date, adjusted_end_date), as_dict=True)
 
    return {
        "total_order_data": total_order_data
    }

@frappe.whitelist()
def get_revenue_week_and_month():
    # Lấy ngày hiện tại
    current_date = getdate(today())
    
    # Tính ngày bắt đầu của tuần (thứ 2)
    week_start = current_date - timedelta(days=current_date.weekday())  # Monday

    # Tính ngày cuối cùng của hôm nay (23:59:59)
    end_of_today = current_date + timedelta(days=1) - timedelta(seconds=1)  # 23:59:59 của ngày hôm nay
    
    # Tính ngày bắt đầu và kết thúc của tháng
    month_start = get_first_day(current_date)
    
    # Tính doanh thu tuần này (từ thứ 2 đến ngày hôm nay)
    revenue_week = frappe.db.sql("""
        SELECT 
            SUM(total_amount) as revenue_week
        FROM `tabEFE Order`
        WHERE order_date >= %s AND order_date <= %s
    """, (week_start, end_of_today), as_dict=True)
    
    # Tính doanh thu tháng này (từ ngày 1 đến ngày hiện tại)
    revenue_month = frappe.db.sql("""
        SELECT 
            SUM(total_amount) as revenue_month
        FROM `tabEFE Order`
        WHERE order_date >= %s AND order_date <= %s
    """, (month_start, current_date), as_dict=True)

    return {
        "revenue_week": revenue_week[0].get("revenue_week") or 0,
        "revenue_month": revenue_month[0].get("revenue_month") or 0
    }

class EFEOrder(Document):
    def before_save(self):
        # Reset total_amount trước khi tính toán lại
        self.total_amount = 0

        # Duyệt qua từng dòng trong child table EFE Order Meal Package
        for item in self.efe_order_meal_package:
            # Lấy giá đơn vị từ Meal Package
            meal_package = frappe.get_doc("EFE Meal Package", item.meal_package)
            item.unit_price = meal_package.price

            # Tính toán tổng giá (Quantity * Unit Price)
            item.total_price = item.quantity * item.unit_price

            # Cộng tổng giá vào tổng số tiền của toàn bộ order
            self.total_amount += item.total_price


@frappe.whitelist()
def create_order(data):
    try:
        data = frappe.parse_json(data)
        customer_name = data.get('customerName')
        order_date = data.get('orderDate')
        delivery_address = data.get('deliveryAddress')
        order_status = data.get('orderStatus')
        payment_status = data.get('paymentStatus')
        shipping_fee = data.get('shippingFee', 0)
        order_note = data.get('orderNote', '')
        shipping_note = data.get('shippingNote', '')
        
        # Validate the data
        if not customer_name or not order_date or not delivery_address or not payment_status:
            frappe.throw(_("Mandatory fields are missing"))

        order = frappe.get_doc({
            "doctype": "EFE Order",
            "customer_nick_name": customer_name,
            "order_date": order_date,
            "delivery_address": delivery_address,
            "order_status": order_status,
            "payment_status": payment_status,
            "shipping_fee": shipping_fee,
            "order_note": order_note,
            "shipping_note": shipping_note,
        })
        total_price = 0
        order_meals = data.get("orderMeals", [])
        for meal in order_meals:
          item_price = get_unit_price(meal.get("packageId"))
          meal_total_price = meal.get("quantity") * item_price
          total_price += meal_total_price 
        
          order.append("order_meal_package", {
            "meal_package": meal.get("packageId"),
            "quantity": meal.get("quantity"),
            "unit_price": item_price, 
            "total_price": meal_total_price,
          })
        order.total_amount = total_price + shipping_fee
        order.insert()
        order.save()

      
        frappe.db.commit()
        return {
                'status': 'success',
                'message': 'Order created successfully',
            }
        
    except Exception as e:
      frappe.log_error(frappe.get_traceback(), "Create Order Failed")
      return {
        'status':'error',
        'message': str(e)
      }


def get_unit_price(package_name):
    try:
        meal_package = frappe.get_doc("EFE Meal Package", package_name)
        return meal_package.unit_price
      
    except frappe.DoesNotExistError:
        frappe.throw(f"Meal Package '{package_name}' does not exist.")


@frappe.whitelist() 
def get_order_detail(order_id):
    try:
        order_detail = frappe.get_doc('EFE Order', order_id)

        customer_name = order_detail.get("customer_nick_name")
        # Create a dictionary to store the order details
        order_data = order_detail.as_dict()

        if customer_name:
            # Fetch the nick_name from EFE Customer using the customer_nick_name
            customer_info = frappe.get_value("EFE Customer", customer_name, "nick_name")
            
            # Assign the nick_name to the customer_nick_name field in the order detail
            order_data["customer_nick_name"] = customer_info
        return {
            "status": "success",
            "order_detail": order_data
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@frappe.whitelist()  
def delete_order(order_id):
    try:
        # Check if the order exists
        if frappe.db.exists("EFE Order", order_id):
            frappe.delete_doc("EFE Order", order_id)  # Delete the order
            frappe.db.commit()  # Commit the transaction
            return {"status": "success", "message": f"Order deleted successfully."}
        else:
            return {"status": "error", "message": "Order not found."}
    except Exception as e:
        return {"status": "error", "message": str(e)}