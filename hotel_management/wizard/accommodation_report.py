from odoo import fields, models
import json
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
        print("kwertyui")
        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'guest_id': self.guest_id.id if self.guest_id else False,
        }

        return {
            'type': 'ir.actions.report',
            'data': {'model': 'hotel.accommodation',
                     'options': json.dumps(data,
                                           default=json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Sales Excel Report',
                     },
            'report_type': 'xlsx',
        }
