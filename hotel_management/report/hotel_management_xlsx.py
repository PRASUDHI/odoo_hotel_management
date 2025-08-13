# import io
# import json
# import xlsxwriter
# from odoo import models
# from odoo.tools import json_default
#
#
# class SalesOrder(models.Model):
#    _inherit = 'sale.order'
#    def sale_report_excel(self):
#        products = self.mapped('order_line.product_id.name')
#        data = {
#            'model_id': self.id,
#            'date': self.date_order,
#            'customer': self.partner_id.name,
#            'products': products
#        }
#        return {
#            'type': 'ir.actions.report',
#            'data': {'model': 'sale.order',
#                     'options': json.dumps(data,
#                                           default=json_default),
#                     'output_format': 'xlsx',
#                     'report_name': 'Sales Excel Report',
#                     },
#            'report_type': 'xlsx',
#        }
#    def get_xlsx_report(self, data, response):
#        output = io.BytesIO()
#        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
#        sheet = workbook.add_worksheet()
#        cell_format = workbook.add_format(
#            {'font_size': '12px', 'align': 'center'})
#        head = workbook.add_format(
#            {'align': 'center', 'bold': True, 'font_size': '20px'})
#        txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
#        sheet.merge_range('B2:I3', 'EXCEL REPORT', head)
#        sheet.merge_range('A4:B4', 'Customer:', cell_format)
#        sheet.merge_range('C4:D4', data['customer'],txt)
#        sheet.merge_range('A5:B5', 'Products', cell_format)
#        for i, product in enumerate(data['products'],
#                                    start=5):  # Start at row 6 for products
#            sheet.merge_range(f'C{i}:D{i}', product, txt)
#        workbook.close()
#        output.seek(0)
#        response.stream.write(output.read())
#        output.close()