from __future__ import unicode_literals
import frappe
from frappe import auth
import datetime
import json, ast


################ Quotation
@frappe.whitelist()
def quot_before_insert(doc, method=None):
    pass
@frappe.whitelist()
def quot_after_insert(doc, method=None):
    pass
@frappe.whitelist()
def quot_onload(doc, method=None):
    pass
@frappe.whitelist()
def quot_before_validate(doc, method=None):
    pass
@frappe.whitelist()
def quot_validate(doc, method=None):
    pass
@frappe.whitelist()
def quot_on_submit(doc, method=None):
    pass
@frappe.whitelist()
def quot_on_cancel(doc, method=None):
    pass
@frappe.whitelist()
def quot_on_update_after_submit(doc, method=None):
    pass
@frappe.whitelist()
def quot_before_save(doc, method=None):
    pass
@frappe.whitelist()
def quot_before_cancel(doc, method=None):
    pass
@frappe.whitelist()
def quot_on_update(doc, method=None):
    pass


################ Sales Order
@frappe.whitelist()
def so_before_insert(doc, method=None):
    pass
@frappe.whitelist()
def so_after_insert(doc, method=None):
    pass
@frappe.whitelist()
def so_onload(doc, method=None):
    pass
@frappe.whitelist()
def so_before_validate(doc, method=None):
    pass
@frappe.whitelist()
def so_validate(doc, method=None):
    pass
@frappe.whitelist()
def so_on_submit(doc, method=None):
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
def so_on_cancel(doc, method=None):
    pass
@frappe.whitelist()
def so_on_update_after_submit(doc, method=None):
    pass
@frappe.whitelist()
def so_before_save(doc, method=None):
    pass
@frappe.whitelist()
def so_before_cancel(doc, method=None):
    pass
@frappe.whitelist()
def so_on_update(doc, method=None):
    pass


################ Delivery Note
@frappe.whitelist()
def dn_before_insert(doc, method=None):
    pass
@frappe.whitelist()
def dn_after_insert(doc, method=None):
    pass
@frappe.whitelist()
def dn_onload(doc, method=None):
    pass
@frappe.whitelist()
def dn_before_validate(doc, method=None):
    pass
@frappe.whitelist()
def dn_validate(doc, method=None):
    pass
@frappe.whitelist()
def dn_on_submit(doc, method=None):
    user = frappe.session.user
    lang = frappe.db.get_value("User", {'name': user}, "language")
    ## Auto Create Draft Sales Invoice On Submit
    new_doc = frappe.get_doc({
        "doctype": "Sales Invoice",
        "customer": doc.customer,
        "customer_group": doc.customer_group,
        "territory": doc.territory,
        "posting_date": doc.posting_date,
        "is_return": doc.is_return,
        "po_no": doc.po_no,
        "po_date": doc.po_date,
        "customer_address": doc.customer_address,
        "shipping_address_name": doc.shipping_address_name,
        "dispatch_address_name": doc.dispatch_address_name,
        "company_address": doc.company_address,
        "contact_person": doc.contact_person,
        "tax_id": doc.tax_id,
        "currency": doc.currency,
        "conversion_rate": doc.conversion_rate,
        "selling_price_list": doc.selling_price_list,
        "price_list_currency": doc.price_list_currency,
        "plc_conversion_rate": doc.plc_conversion_rate,
        "ignore_pricing_rule": doc.ignore_pricing_rule,
        "set_warehouse": doc.set_warehouse,
        "tc_name": doc.tc_name,
        "terms": doc.terms,
        "taxes_and_charges": doc.taxes_and_charges,
        "apply_discount_on": doc.apply_discount_on,
        "base_discount_amount": doc.base_discount_amount,
        "additional_discount_percentage": doc.additional_discount_percentage,
        "discount_amount": doc.discount_amount,
        "project": doc.project,
    })

    dn_items = frappe.db.sql(""" select a.name, a.idx, a.item_code, a.item_name, a.description, a.qty, a.stock_qty, a.uom, a.stock_uom, a.conversion_factor, a.rate, a.amount,
                                           a.price_list_rate, a.base_price_list_rate, a.base_rate, a.base_amount, a.net_rate, a.net_amount, a.margin_type, a.margin_rate_or_amount, a.rate_with_margin,
                                           a.discount_percentage, a.discount_amount, a.base_rate_with_margin, a.item_tax_template
                                           from `tabDelivery Note Item` a join `tabDelivery Note` b
                                           on a.parent = b.name
                                           where b.name = '{name}'
                                       """.format(name=doc.name), as_dict=1)

    for c in dn_items:
        items = new_doc.append("items", {})
        items.idx = c.idx
        items.item_code = c.item_code
        items.item_name = c.item_name
        items.description = c.description
        items.qty = c.qty
        items.uom = c.uom
        items.stock_uom = c.stock_uom
        items.conversion_factor = c.conversion_factor
        items.price_list_rate = c.price_list_rate
        items.base_price_list_rate = c.base_price_list_rate
        items.base_rate = c.base_rate
        items.base_amount = c.base_amount
        items.rate = c.rate
        items.net_rate = c.net_rate
        items.net_amount = c.net_amount
        items.amount = c.amount
        items.margin_type = c.margin_type
        items.margin_rate_or_amount = c.margin_rate_or_amount
        items.rate_with_margin = c.rate_with_margin
        items.discount_percentage = c.discount_percentage
        items.discount_amount = c.discount_amount
        items.base_rate_with_margin = c.base_rate_with_margin
        items.item_tax_template = c.item_tax_template
        items.delivered_qty = c.qty
        items.dn_detail = c.name
        items.delivery_note = doc.name

    dn_taxes = frappe.db.sql(""" select a.charge_type, a.row_id, a.account_head, a.description, a.included_in_print_rate, a.included_in_paid_amount, a.rate, a.account_currency, a.tax_amount,
                                        a.total, a.tax_amount_after_discount_amount, a.base_tax_amount, a.base_total, a.base_tax_amount_after_discount_amount, a.item_wise_tax_detail, a.dont_recompute_tax
                                       from `tabSales Taxes and Charges` a join `tabDelivery Note` b
                                       on a.parent = b.name
                                       where b.name = '{name}'
                                   """.format(name=doc.name), as_dict=1)

    for x in dn_taxes:
        taxes = new_doc.append("taxes", {})
        taxes.charge_type = x.charge_type
        taxes.row_id = x.row_id
        taxes.account_head = x.account_head
        taxes.description = x.description
        taxes.included_in_print_rate = x.included_in_print_rate
        taxes.included_in_paid_amount = x.included_in_paid_amount
        taxes.rate = x.rate
        taxes.account_currency = x.account_currency
        taxes.tax_amount = x.tax_amount
        taxes.total = x.total
        taxes.tax_amount_after_discount_amount = x.tax_amount_after_discount_amount
        taxes.base_tax_amount = x.base_tax_amount
        taxes.base_total = x.base_total
        taxes.base_tax_amount_after_discount_amount = x.base_tax_amount_after_discount_amount
        taxes.item_wise_tax_detail = x.item_wise_tax_detail
        taxes.dont_recompute_tax = x.dont_recompute_tax

    new_doc.insert(ignore_permissions=True)
    if lang == "ar":
        frappe.msgprint("  تم إنشاء فاتورة مبيعات بحالة مسودة رقم " + new_doc.name)
    else:
        frappe.msgprint(" Sales Invoice " + new_doc.name + " Created ")


@frappe.whitelist()
def dn_on_cancel(doc, method=None):
    pass
@frappe.whitelist()
def dn_on_update_after_submit(doc, method=None):
    pass
@frappe.whitelist()
def dn_before_save(doc, method=None):
    pass
@frappe.whitelist()
def dn_before_cancel(doc, method=None):
    pass
@frappe.whitelist()
def dn_on_update(doc, method=None):
    pass

################ Sales Invoice
@frappe.whitelist()
def siv_before_insert(doc, method=None):
    pass
@frappe.whitelist()
def siv_after_insert(doc, method=None):
    pass
def siv_onload(doc, method=None):
    pass
@frappe.whitelist()
def siv_before_validate(doc, method=None):
    pass
@frappe.whitelist()
def siv_validate(doc, method=None):
    pass
@frappe.whitelist()
def siv_on_submit(doc, method=None):
    pass
@frappe.whitelist()
def siv_on_cancel(doc, method=None):
    pass
@frappe.whitelist()
def siv_on_update_after_submit(doc, method=None):
    pass
@frappe.whitelist()
def siv_before_save(doc, method=None):
    pass
@frappe.whitelist()
def siv_before_cancel(doc, method=None):
    pass
@frappe.whitelist()
def siv_on_update(doc, method=None):
    pass


################ Payment Entry
@frappe.whitelist()
def pe_before_insert(doc, method=None):
    pass
@frappe.whitelist()
def pe_after_insert(doc, method=None):
    pass
@frappe.whitelist()
def pe_onload(doc, method=None):
    pass
@frappe.whitelist()
def pe_before_validate(doc, method=None):
    pass
@frappe.whitelist()
def pe_validate(doc, method=None):
    pass
@frappe.whitelist()
def pe_on_submit(doc, method=None):
    if doc.reference_link and reference_doctype == "Ticket":
        frappe.db.set_value('Ticket', doc.reference_link, "payment_entry_status", doc.status)

@frappe.whitelist()
def pe_on_cancel(doc, method=None):
    if doc.reference_link and reference_doctype == "Ticket":
        frappe.db.sql(""" update `tabTicket` set payment_entry = "" where name = %s""", doc.reference_link)
        frappe.db.sql(""" update `tabTicket` set payment_entry_status = "" where name = %s""", doc.reference_link)
        frappe.db.sql(""" update `tabPayment Entry set reference_name = "" where name = %s""", doc.name)
        #frappe.db.set_value('Ticket', doc.reference_link, "payment_entry", "")
        #frappe.db.set_value('Ticket', doc.reference_link, "payment_entry_status", "")
        #doc.reference_name = None

@frappe.whitelist()
def pe_on_update_after_submit(doc, method=None):
    pass
@frappe.whitelist()
def pe_before_save(doc, method=None):
    pass
@frappe.whitelist()
def pe_before_cancel(doc, method=None):
    pass
@frappe.whitelist()
def pe_on_update(doc, method=None):
    pass

################ Material Request
@frappe.whitelist()
def mr_before_insert(doc, method=None):
    pass
@frappe.whitelist()
def mr_after_insert(doc, method=None):
    pass
@frappe.whitelist()
def mr_onload(doc, method=None):
    pass
@frappe.whitelist()
def mr_before_validate(doc, method=None):
    pass
@frappe.whitelist()
def mr_validate(doc, method=None):
    pass
@frappe.whitelist()
def mr_on_submit(doc, method=None):
    pass
@frappe.whitelist()
def mr_on_cancel(doc, method=None):
    pass
@frappe.whitelist()
def mr_on_update_after_submit(doc, method=None):
    pass
@frappe.whitelist()
def mr_before_save(doc, method=None):
    pass
@frappe.whitelist()
def mr_before_cancel(doc, method=None):
    pass
@frappe.whitelist()
def mr_on_update(doc, method=None):
    pass

################ Purchase Order
@frappe.whitelist()
def po_before_insert(doc, method=None):
    pass
@frappe.whitelist()
def po_after_insert(doc, method=None):
    pass
@frappe.whitelist()
def po_onload(doc, method=None):
    pass
@frappe.whitelist()
def po_before_validate(doc, method=None):
    pass
@frappe.whitelist()
def po_validate(doc, method=None):
    pass
@frappe.whitelist()
def po_on_submit(doc, method=None):
    pass
@frappe.whitelist()
def po_on_cancel(doc, method=None):
    pass
@frappe.whitelist()
def po_on_update_after_submit(doc, method=None):
    pass
@frappe.whitelist()
def po_before_save(doc, method=None):
    pass
@frappe.whitelist()
def po_before_cancel(doc, method=None):
    pass
@frappe.whitelist()
def po_on_update(doc, method=None):
    pass

################ Purchase Receipt
@frappe.whitelist()
def pr_before_insert(doc, method=None):
    pass
@frappe.whitelist()
def pr_after_insert(doc, method=None):
    pass
@frappe.whitelist()
def pr_onload(doc, method=None):
    pass
@frappe.whitelist()
def pr_before_validate(doc, method=None):
    pass
@frappe.whitelist()
def pr_validate(doc, method=None):
    pass
@frappe.whitelist()
def pr_on_submit(doc, method=None):
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
def pr_on_cancel(doc, method=None):
    pass
@frappe.whitelist()
def pr_on_update_after_submit(doc, method=None):
    pass
@frappe.whitelist()
def pr_before_save(doc, method=None):
    pass
@frappe.whitelist()
def pr_before_cancel(doc, method=None):
    pass
@frappe.whitelist()
def pr_on_update(doc, method=None):
    pass


################ Purchase Invoice
@frappe.whitelist()
def piv_before_insert(doc, method=None):
    pass
@frappe.whitelist()
def piv_after_insert(doc, method=None):
    pass
@frappe.whitelist()
def piv_onload(doc, method=None):
    pass
@frappe.whitelist()
def piv_before_validate(doc, method=None):
    pass
@frappe.whitelist()
def piv_validate(doc, method=None):
    pass
@frappe.whitelist()
def piv_on_submit(doc, method=None):
    pass
@frappe.whitelist()
def piv_on_cancel(doc, method=None):
    pass
@frappe.whitelist()
def piv_on_update_after_submit(doc, method=None):
    pass
@frappe.whitelist()
def piv_before_save(doc, method=None):
    pass
@frappe.whitelist()
def piv_before_cancel(doc, method=None):
    pass
@frappe.whitelist()
def piv_on_update(doc, method=None):
    pass

################ Employee Advance
@frappe.whitelist()
def emad_before_insert(doc, method=None):
    pass
@frappe.whitelist()
def emad_after_insert(doc, method=None):
    pass
@frappe.whitelist()
def emad_onload(doc, method=None):
    pass
@frappe.whitelist()
def emad_before_validate(doc, method=None):
    pass
@frappe.whitelist()
def emad_validate(doc, method=None):
    pass
@frappe.whitelist()
def emad_on_submit(doc, method=None):
    pass
@frappe.whitelist()
def emad_on_cancel(doc, method=None):
    pass
@frappe.whitelist()
def emad_on_update_after_submit(doc, method=None):
    pass
@frappe.whitelist()
def emad_before_save(doc, method=None):
    pass
@frappe.whitelist()
def emad_before_cancel(doc, method=None):
    pass
@frappe.whitelist()
def emad_on_update(doc, method=None):
    pass

################ Expense Claim
@frappe.whitelist()
def excl_before_insert(doc, method=None):
    pass
@frappe.whitelist()
def excl_after_insert(doc, method=None):
    pass
@frappe.whitelist()
def excl_onload(doc, method=None):
    pass
@frappe.whitelist()
def excl_before_validate(doc, method=None):
    pass
@frappe.whitelist()
def excl_validate(doc, method=None):
    pass
@frappe.whitelist()
def excl_on_submit(doc, method=None):
    pass
@frappe.whitelist()
def excl_on_cancel(doc, method=None):
    pass
@frappe.whitelist()
def excl_on_update_after_submit(doc, method=None):
    pass
@frappe.whitelist()
def excl_before_save(doc, method=None):
    pass
@frappe.whitelist()
def excl_before_cancel(doc, method=None):
    pass
@frappe.whitelist()
def excl_on_update(doc, method=None):
    pass

################ Stock Entry
@frappe.whitelist()
def ste_before_insert(doc, method=None):
    pass
@frappe.whitelist()
def ste_after_insert(doc, method=None):
    pass
@frappe.whitelist()
def ste_onload(doc, method=None):
    pass
@frappe.whitelist()
def ste_before_validate(doc, method=None):
    pass
@frappe.whitelist()
def ste_validate(doc, method=None):
    if doc.ticket:
        frappe.db.set_value('Ticket Items', doc.ticket_item, "stock_entry", doc.name)
        if doc.docstatus == 0:
            frappe.db.set_value('Ticket Items', doc.ticket_item, "stock_entry_status", "Draft")
        if doc.docstatus == 1:
            frappe.db.set_value('Ticket Items', doc.ticket_item, "stock_entry_status", "Submitted")
@frappe.whitelist()
def ste_on_submit(doc, method=None):
    pass
@frappe.whitelist()
def ste_on_cancel(doc, method=None):
    if doc.ticket:
        frappe.db.set_value('Ticket Items', doc.ticket_item, "stock_entry", "")
        frappe.db.set_value('Ticket Items', doc.ticket_item, "stock_entry_status", "")

@frappe.whitelist()
def ste_on_update_after_submit(doc, method=None):
    pass
@frappe.whitelist()
def ste_before_save(doc, method=None):
    pass
@frappe.whitelist()
def ste_before_cancel(doc, method=None):
    pass
@frappe.whitelist()
def ste_on_update(doc, method=None):
    pass

################ Blanket Order
@frappe.whitelist()
def blank_before_insert(doc, method=None):
    pass
@frappe.whitelist()
def blank_after_insert(doc, method=None):
    pass
@frappe.whitelist()
def blank_onload(doc, method=None):
    pass
@frappe.whitelist()
def blank_before_validate(doc, method=None):
    pass
@frappe.whitelist()
def blank_validate(doc, method=None):
    pass
@frappe.whitelist()
def blank_on_submit(doc, method=None):
    pass
@frappe.whitelist()
def blank_on_cancel(doc, method=None):
    pass
@frappe.whitelist()
def blank_on_update_after_submit(doc, method=None):
    pass
@frappe.whitelist()
def blank_before_save(doc, method=None):
    pass
@frappe.whitelist()
def blank_before_cancel(doc, method=None):
    pass
@frappe.whitelist()
def blank_on_update(doc, method=None):
    pass
