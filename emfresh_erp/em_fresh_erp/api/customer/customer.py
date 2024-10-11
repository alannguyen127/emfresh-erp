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
    
@frappe.whitelist() 
def update_customer(customer_id, **kwargs):
    try:
   
        customer_doc = frappe.get_doc("EFE Customer", customer_id)
        

        for key, value in kwargs.items():
            if key in customer_doc.as_dict():
                customer_doc.set(key, value)

       
        customer_doc.save()

        return {
            "status": "success",
            "message": "Customer updated successfully",
            "customer": customer_doc.as_dict()
        }

    except frappe.DoesNotExistError:
    
        frappe.throw(f"Customer with ID {customer_id} does not exist")
    
    except Exception as e:

        frappe.log_error(message=str(e), title="Customer Update Error")
        return {
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        }
    

@frappe.whitelist()
def get_customer_gender_data():
    """
    Trả về tổng số khách hàng, số khách hàng là Nam và Nữ
    """

    # Query đếm tổng số khách hàng
    total_customers = frappe.db.sql("""SELECT COUNT(*) FROM `tabEFE Customer`""")[0][0]

    # Query đếm số khách hàng là Nam
    male_customers = frappe.db.sql("""SELECT COUNT(*) FROM `tabEFE Customer` WHERE gender = 'Male'""")[0][0]

    # Query đếm số khách hàng là Nữ
    female_customers = frappe.db.sql("""SELECT COUNT(*) FROM `tabEFE Customer` WHERE gender = 'Female'""")[0][0]
    
    # Query đếm số khách hàng là Nữ
    no_info_customers = frappe.db.sql("""SELECT COUNT(*) FROM `tabEFE Customer` WHERE gender = 'No Info'""")[0][0]

    # Trả về dữ liệu dưới dạng JSON
    return {
        "total_customers": total_customers,
        "male_customers": male_customers,
        "female_customers": female_customers,
        "no_info_customers": no_info_customers,
    }
