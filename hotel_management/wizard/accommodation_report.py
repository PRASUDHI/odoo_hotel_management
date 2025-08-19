from odoo import fields, models, api, _
import json
from odoo import models
from odoo.tools import json_default


class AccommodationReportWizard(models.TransientModel):
    """
    This wizard is shown for filtering the Report.
    """

    _name = "accommodation.report.wizard"
    _description = "hotel management report"

    date_from = fields.Date("Date From")
    date_to = fields.Date("Date To")
    guest_id = fields.Many2one("res.partner", string="Guest")

    def action_print_report(self):
        self.ensure_one()
        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'guest_id': self.guest_id.id if self.guest_id else False,
        }
        # return self.env.ref('hotel_management.hotel_management_report_pdf').report_action(None, data=data)

        report_reference = self.env.ref('hotel_management.hotel_management_report_pdf').report_action(None, data=data)
        report_reference.update({'close_on_report_download': True})
        return report_reference



    def print_xls_report(self):
        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'guest_id': self.guest_id.id if self.guest_id else False,
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'report.hotel_management.hotel_management_report_template',
                     'options': json.dumps(data,
                                           default=json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Sales Excel Report',
                     },
            'report_type': 'xlsx',

        }
        # action_window = {
        #     'type': 'ir.actions.report',
        #     'model':'report.hotel_management.hotel_management_report_template',
        #     'options':json.dumps(data,default=json_default),
        #     'output_format': 'xlsx',
        #     'report_name': 'Excel Report',
        #
        # }
        #
        # action_close = {'type': 'ir.actions.act_window_close'}
        #
        # return {
        #     'type': 'ir.actions.act_multi',
        #     'actions': [action_window, action_close]
        # }




