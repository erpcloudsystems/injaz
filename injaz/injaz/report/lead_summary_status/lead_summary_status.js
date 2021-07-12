// Copyright (c) 2019, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Lead Summary Status"] = {
	"filters": [
		{
			fieldname:"from_date",
			reqd: 1,
			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
		},
		{
			fieldname:"to_date",
			reqd: 1,
			default: frappe.datetime.get_today(),
			label: __("To Date"),
			fieldtype: "Date",
		},
	
	],

	
};