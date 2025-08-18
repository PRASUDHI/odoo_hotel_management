import io

import xlsxwriter

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
        name = self.env['res.partner'].browse(name).name
        # print(name)

        return {
            'docs': records,
            'doc_ids': docids,
            'doc_model': 'hotel.accommodation',
            'data': data,
            'name': name

        }

    def _get_xlsx_report(self, data, response):
        print("dfghjk")
        date_from = data.get('date_from')
        date_to = data.get('date_to')
        guest_id = data.get('guest_id')

        # SQL query
        query = """
            SELECT 
                row_number() OVER () AS sl_no,
                res_partner.name AS guest,
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
        if guest_id:
            query += " AND hotel_accommodation.guest_id = %s"
            params.append(guest_id)

        self.env.cr.execute(query, tuple(params))
        records = self.env.cr.fetchall()


        guest_name = self.env['res.partner'].browse(guest_id).name if guest_id else "All"




        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet("Hotel Report")


        title_format = workbook.add_format({'align': 'center', 'bold': True, 'font_size': 14})
        bold = workbook.add_format({'bold': True})
        date_fmt = workbook.add_format({'num_format': 'yyyy-mm-dd'})


        sheet.merge_range('A1:E1', 'Hotel Management Report', title_format)


        sheet.write('A3', 'Date From', bold)
        sheet.write('B3', str(date_from or ''))
        sheet.write('C3', 'Date To', bold)
        sheet.write('D3', str(date_to or ''))
        sheet.write('E3', f"Guest: {guest_name}", bold)

        # Table headings
        headers = ["SL.No", "Guest", "Check-In", "Check-Out", "State"]
        for col, header in enumerate(headers):
            sheet.write(5, col, header, bold)


        row = 6
        for rec in records:
            sheet.write(row, 0, rec['sl_no'])
            sheet.write(row, 1, rec['guest'])
            sheet.write(row, 2, rec['date_from'], date_fmt)
            sheet.write(row, 3, rec['date_to'], date_fmt)
            sheet.write(row, 4, rec['state'])
            row += 1


        for col_num, header in enumerate(headers):
            sheet.set_column(col_num, col_num, len(header) + 5)

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
