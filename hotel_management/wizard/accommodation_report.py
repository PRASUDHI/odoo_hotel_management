from odoo import fields, models


class AccommodationReportWizard(models.TransientModel):
    """
    This wizard is shown for filtering the Report.
    """

    _name = "accommodation.report.wizard"
    _description = "hotel management report"

    guest_id = fields.Many2one('res.partner')
    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date To")
    accommodation_id=fields.Many2one('hotel.accommodation')





    def action_print_report(self):


        self.ensure_one()
        query = """
                    select row_number() OVER () AS sl_no, guest_id as  guest,check_in as date_from,check_in as  date_to 
                    from hotel_accommodation as tb"""
        if self.date_from:
            query += """ where tb.check_in >= '%s' and tb.check_in <= '%s' and tb.guest_id = '%s'""" % (self.date_from,self.date_to,self.guest_id.id)

        self.env.cr.execute(query)
        result=self.env.cr.dictfetchall()
        data = {'result': result,}
        print("accommodation", result)
        return self.env.ref('hotel_management.action_report_hotel_management').report_action(None, data=data)

