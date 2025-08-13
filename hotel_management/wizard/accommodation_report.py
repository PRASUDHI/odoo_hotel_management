from odoo import fields, models


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
        pass
    #     self.ensure_one()

    #     data = {
    #         'date_from': self.date_from,
    #         'date_to': self.date_to,
    #         'guest_id': self.guest_id.id if self.guest_id else False,
    #     }
    #     return self.env.ref('hotel_management.hotel_management_report_xlsx').report_action(None, data=data)
