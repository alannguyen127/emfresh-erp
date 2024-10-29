app_name = "emfresh_erp"
app_title = "Em Fresh ERP "
app_publisher = "Nghiem Nguyen"
app_description = "Enterprise Resource Planning for Em Fresh "
app_email = "huannghiem2711@gmail.com"
app_license = "apache-2.0"
doc_events = {
    "EFE Customer": {
        "get_customers": "emfresh_erp.em_fresh_erp.api.customer.customer.get_customers",
        "create_customer": "emfresh_erp.em_fresh_erp.api.customer.customer.create_customer",
        "get_customer_detail": "emfresh_erp.em_fresh_erp.api.customer.customer.get_customer_detail",
        "update_customer": "emfresh_erp.em_fresh_erp.api.customer.customer.update_customer",
        "delete_customer": "emfresh_erp.em_fresh_erp.api.customer.customer.delete_customer",
        "get_customer_gender_data": "emfresh_erp.em_fresh_erp.api.customer.customer.get_customer_gender_data",
        
    },
    "EFE Meal Package": {
        "get_meals": "emfresh_erp.em_fresh_erp.api.meal_package.meal_package.get_meals"
    },
    "EFE Order": {
        "get_orders": "emfresh_erp.em_fresh_erp.api.order.order.get_orders",
        "get_sales_data": "emfresh_erp.em_fresh_erp.api.order.order.get_sales_data_by_date",
        "create_order": "emfresh_erp.em_fresh_erp.api.order.order.create_order",
        "count_order_by_date": "emfresh_erp.em_fresh_erp.api.order.order.count_order_by_date",
        "update_order":"emfresh_erp.em_fresh_erp.api.order.order.update_order",
    },
    "User": {
      "change_password": "emfresh_erp.em_fresh_erp.api.user.user.change_password"
    }

}
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/emfresh_erp/css/emfresh_erp.css"
# app_include_js = "/assets/emfresh_erp/js/emfresh_erp.js"

# include js, css files in header of web template
# web_include_css = "/assets/emfresh_erp/css/emfresh_erp.css"
# web_include_js = "/assets/emfresh_erp/js/emfresh_erp.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "emfresh_erp/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "emfresh_erp/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "emfresh_erp.utils.jinja_methods",
# 	"filters": "emfresh_erp.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "emfresh_erp.install.before_install"
# after_install = "emfresh_erp.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "emfresh_erp.uninstall.before_uninstall"
# after_uninstall = "emfresh_erp.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "emfresh_erp.utils.before_app_install"
# after_app_install = "emfresh_erp.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "emfresh_erp.utils.before_app_uninstall"
# after_app_uninstall = "emfresh_erp.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "emfresh_erp.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"emfresh_erp.tasks.all"
# 	],
# 	"daily": [
# 		"emfresh_erp.tasks.daily"
# 	],
# 	"hourly": [
# 		"emfresh_erp.tasks.hourly"
# 	],
# 	"weekly": [
# 		"emfresh_erp.tasks.weekly"
# 	],
# 	"monthly": [
# 		"emfresh_erp.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "emfresh_erp.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "emfresh_erp.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "emfresh_erp.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["emfresh_erp.utils.before_request"]
# after_request = ["emfresh_erp.utils.after_request"]

# Job Events
# ----------
# before_job = ["emfresh_erp.utils.before_job"]
# after_job = ["emfresh_erp.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"emfresh_erp.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

