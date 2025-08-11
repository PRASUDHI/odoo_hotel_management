from odoo import models, fields, api


class AbstractReport(models.AbstractModel):
    _name = 'report.hotel_management.report_hotel_management'
    _description = 'Abstract Model for Reporting'





    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['hotel.accommodation'].browse(docids)
        print("tyuio",docs)

        return {
            'doc_ids': docids,
            'doc_model': 'hotel.accommodation',
            'docs': docs,
            'data': data,
        }
