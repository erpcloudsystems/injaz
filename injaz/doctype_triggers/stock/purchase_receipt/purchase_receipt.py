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
    new_doc = frappe.get_doc({
        "doctype": "Purchase Invoice",
        "posting_date": doc.posting_date,
        "company": doc.company,
        "supplier": doc.supplier,
        "supplier_address": doc.supplier_address,
        "address_display": doc.address_display,
        "contact_person": doc.contact_person,
        "contact_display": doc.contact_display,
        "contact_mobile": doc.contact_mobile,
        "contact_email": doc.contact_email,
        "set_warehouse": doc.set_warehouse,
        "currency": doc.currency,
        "conversion_rate": doc.conversion_rate,
        "buying_price_list": doc.buying_price_list,
        "price_list_currency": doc.price_list_currency,
        "plc_conversion_rate": doc.plc_conversion_rate,
        "tc_name": doc.tc_name,
        "terms": doc.terms,
        "apply_discount_on": doc.apply_discount_on,
        "base_discount_amount": doc.base_discount_amount,
        "additional_discount_percentage": doc.additional_discount_percentage,
        "discount_amount": doc.discount_amount,


    })
    is_items = frappe.db.sql(""" select a.idx, a.item_code, a.item_name, a.item_group, a.qty, a.uom , a.qty, a.rate
    		                                                           from `tabPurchase Receipt Item` a join `tabPurchase Receipt` b
    		                                                           on a.parent = b.name
    		                                                           where b.name = '{name}'
    		                                                       """.format(name=doc.name), as_dict=1)

    for c in is_items:
        items = new_doc.append("items", {})
        items.idx = c.idx
        items.item_code = c.item_code
        items.item_name = c.item_name
        items.qty = c.qty
        items.uom = c.uom
        items.rate = c.rate
        items.purchase_receipt = doc.name

    is_taxes = frappe.db.sql(""" select a.idx, a.charge_type, a.row_id, a.account_head, a.description, a.included_in_print_rate, a.included_in_paid_amount, a.rate, a.account_currency, a.tax_amount,
                                                a.total, a.tax_amount_after_discount_amount, a.base_tax_amount, a.base_total, a.base_tax_amount_after_discount_amount, a.item_wise_tax_detail, a.add_deduct_tax
                                               from `tabPurchase Taxes and Charges` a join `tabPurchase Receipt` b
                                               on a.parent = b.name
                                               where b.name = '{name}'
                                           """.format(name=doc.name), as_dict=1)

    for x in is_taxes:
        taxes = new_doc.append("taxes", {})
        taxes.idx = x.idx
        taxes.charge_type = x.charge_type
        taxes.row_id = x.row_id
        taxes.rate = x.rate
        taxes.tax_amount = x.tax_amount
        taxes.account_head = x.account_head
        taxes.tax_amount_after_discount_amount = x.tax_amount_after_discount_amount
        taxes.base_tax_amount = x.base_tax_amount
        taxes.base_total = x.base_total
        taxes.total = x.total
        taxes.item_wise_tax_detail = x.item_wise_tax_detail
        taxes.account_currency = x.account_currency
        taxes.description = x.description
        taxes.included_in_print_rate = x.included_in_print_rate
        taxes.included_in_paid_amount = x.included_in_paid_amount
        taxes.add_deduct_tax = x.add_deduct_tax

    new_doc.insert(ignore_permissions=True)
    frappe.msgprint("  تم إنشاء فاتورة مشتريات بحالة مسودة رقم " + new_doc.name)
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
