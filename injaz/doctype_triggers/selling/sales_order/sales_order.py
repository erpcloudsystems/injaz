from __future__ import unicode_literals
import frappe
from frappe import _


@frappe.whitelist()
def before_insert(doc, method=None):
    pass
@frappe.whitelist()
def after_insert(doc, method=None):
    pass
@frappe.whitelist()
def onload(doc, method=None):
    pass
@frappe.whitelist()
def before_validate(doc, method=None):
    pass
@frappe.whitelist()
def validate(doc, method=None):
    pass
@frappe.whitelist()
def on_submit(doc, method=None):
    user = frappe.session.user
    lang = frappe.db.get_value("User", {'name': user}, "language")

    ## Auto Create Project On Submit
    if doc.auto_create_project_on_submit == "Yes":
        new_doc2 = frappe.get_doc({
            "doctype": "Project",
            "project_name": str(doc.project_name),
            "customer": doc.customer,
            "sales_order": doc.name,
            "status": "Open",
            "expected_start_date": doc.transaction_date,
            "priority": "High",
        })
        new_doc2.insert(ignore_permissions=True)
        doc.project = new_doc2.name
        if lang == "ar":
            frappe.msgprint("  تم إنشاء مشروع رقم " + new_doc2.name)
        else:
            frappe.msgprint(" Project " + new_doc2.name + " Created ")
@frappe.whitelist()
def on_cancel(doc, method=None):
    pass
@frappe.whitelist()
def on_update_after_submit(doc, method=None):
    pass
@frappe.whitelist()
def before_save(doc, method=None):
    pass
@frappe.whitelist()
def before_cancel(doc, method=None):
    pass
@frappe.whitelist()
def on_update(doc, method=None):
    pass
