import frappe
from frappe import _
from frappe.utils.password import update_password

@frappe.whitelist(allow_guest=False)
def change_password(user_id, old_password, new_password):
    # Lấy thông tin người dùng từ user_id
    user = frappe.get_doc("User", user_id)

    # Kiểm tra mật khẩu cũ có khớp không
    if not frappe.local.login_manager.check_password(user_id, old_password):
        frappe.throw(_("Old password is incorrect."), frappe.ValidationError)
    
    # Cập nhật mật khẩu mới
    try:
        update_password(user_id, new_password)  # Cập nhật mật khẩu mới
        frappe.db.commit()
        return {"status": "success", "message": _("Password changed successfully.")}
    except Exception as e:
        frappe.throw(_("Failed to change password. Error: {0}").format(str(e)))

@frappe.whitelist()
def create_user_account(first_name, email, password, confirm_password, role):
    try:
        if password != confirm_password:
            return {
                "status": "error",
                "message": "Password and confirm password do not match."
            }
        if frappe.db.exists("User", email):
            return {
                "status": "error",
                "message": "Email already exists."
            }
        user = frappe.get_doc({
            "doctype": "User",
            "email": email,
            "first_name": first_name,
            "enabled": 1,
            "new_password": password,
            "send_welcome_email": 0, 
            "roles": [
              {"role":"System Manager"}
            ]
        })
        user.insert(ignore_permissions=True)

        efe_user = frappe.get_doc({
            "doctype": "EFE User",
            "user": user.name,  
            "role": role  
        })
        efe_user.insert(ignore_permissions=True)

        return {
            "status": "success",
            "message": "User account created successfully",
            "user_id": user.name  
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
