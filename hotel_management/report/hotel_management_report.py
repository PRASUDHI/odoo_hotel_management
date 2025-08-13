from odoo import models, fields, api


class AbstractReport(models.AbstractModel):
    _name = 'report.hotel_management.hotel_management_report_template'
    _description = 'Abstract Model for Reporting'

    @api.model
    def _get_report_values(self, docids, data=None):
        date_from = data.get('date_from')
        date_to = data.get('date_to')
        name = data.get('guest_id')

        query = """
            SELECT 
                row_number() OVER () AS sl_no,
                res_partner.name,
                check_in AS date_from,
                check_out AS date_to,
                room_status AS state
            FROM hotel_accommodation
            LEFT JOIN res_partner 
                ON res_partner.id = hotel_accommodation.guest_id
            WHERE TRUE
        """
        params = []

        if date_from:
            query += " AND hotel_accommodation.check_in >= %s"
            params.append(date_from)
        if date_to:
            query += " AND hotel_accommodation.check_in <= %s"
            params.append(date_to)
        if name:
            query += " AND hotel_accommodation.guest_id = %s"
            params.append(name)

        self.env.cr.execute(query, tuple(params))
        records = self.env.cr.dictfetchall()
        print('records', records)
        print('params',params)
        print('query',query)
        name=self.env['res.partner'].browse(name).name
        print('name',name)

        return {
            'docs': records,
            'doc_ids': docids,
            'doc_model': 'hotel.accommodation',
            'data': data,
            'name':name

        }
