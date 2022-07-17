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
    if doc.reference_link and reference_doctype == "Ticket":
        frappe.db.set_value('Ticket', doc.reference_link, "payment_entry_status", doc.status)
@frappe.whitelist()
def on_cancel(doc, method=None):
    if doc.reference_link and reference_doctype == "Ticket":
        frappe.db.sql(""" update `tabTicket` set payment_entry = "" where name = %s""", doc.reference_link)
        frappe.db.sql(""" update `tabTicket` set payment_entry_status = "" where name = %s""", doc.reference_link)
        frappe.db.sql(""" update `tabPayment Entry set reference_name = "" where name = %s""", doc.name)
        #frappe.db.set_value('Ticket', doc.reference_link, "payment_entry", "")
        #frappe.db.set_value('Ticket', doc.reference_link, "payment_entry_status", "")
        #doc.reference_name = None
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
