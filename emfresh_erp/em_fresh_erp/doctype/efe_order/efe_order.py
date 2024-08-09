# Copyright (c) 2024, Nghiem Nguyen and contributors
# For license information, please see license.txt

import frappe

@frappe.whitelist()
def get_meal_boxes(day_menu):
    if not day_menu:
        return []

    # Lấy tài liệu của EFE Day Menu
    day_menu_doc = frappe.get_doc("EFE Day Menu", day_menu)
    
    # Lấy danh sách các meal_box từ trường multi-select
    meal_boxes = [box.meal_box for box in day_menu_doc.meal_box]
    
    return meal_boxes




from frappe.model.document import Document


class EFEOrder(Document):
	pass
