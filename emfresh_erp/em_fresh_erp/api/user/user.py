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
