import frappe
from frappe import _
from frappe.utils import flt, getdate, add_days
from frappe.model.document import Document

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