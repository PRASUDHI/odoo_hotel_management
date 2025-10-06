# -*- coding: utf-8 -*-
from odoo import models, api
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta


class InventoryDashboard(models.Model):
    _name = "inventory.dashboard"
    _description = "Inventory Dashboard Data"

    def _get_date_domain(self, period, value=None):
        """
        Helper function to generate a date domain.
        It now handles specific week, month, or year values.
        """
        domain = []
        if not period or period == 'all' or not value:
            return []

        try:
            if period == 'week':

                start_date = datetime.strptime(f"{value}-1", "%Y-W%W-%w").date()
                end_date = start_date + timedelta(days=6)
                domain = [('date', '>=', start_date), ('date', '<=', end_date)]
            elif period == 'month':
                year, month = map(int, value.split('-'))
                start_date = date(year, month, 1)
                end_date = (start_date + relativedelta(months=1)) - timedelta(days=1)
                domain = [('date', '>=', start_date), ('date', '<=', end_date)]
        except (ValueError, TypeError):
            return []

        return domain

    @api.model
    def get_dashboard_data(self, filters=None):
        if filters is None:
            filters = {}

        data = {}
        period = filters.get('period')
        value = filters.get('value')
        date_domain = self._get_date_domain(period, value)

        user = self.env.user
        user_domain = []
        if not user.has_group('stock.group_stock_manager'):
            user_domain = [('create_uid', '=', self.env.user.id)]

        incoming_domain = date_domain + [('picking_code', '=', 'incoming')] + user_domain
        outgoing_domain = date_domain + [('picking_code', '=', 'outgoing')] + user_domain
        internal_domain = date_domain + [('picking_code', '=', 'internal')] + user_domain

        data['incoming'] = self.env['stock.move'].read_group(
            incoming_domain, ['product_id', 'product_uom_qty:sum'], ['product_id']
        )
        data['outgoing'] = self.env['stock.move'].read_group(
            outgoing_domain, ['product_id', 'product_uom_qty:sum'], ['product_id']
        )
        data['internal'] = self.env['stock.move'].read_group(
            internal_domain, ['product_id', 'product_uom_qty:sum'], ['product_id']
        )

        picking_date_domain = [(item[0].replace('date', 'date_done'), item[1], item[2]) for item in date_domain]
        picking_date_domain += user_domain
        data['picking_types'] = self.env['stock.picking'].read_group(
            picking_date_domain, ['picking_type_id'], ['picking_type_id']
        )

        warehouses = self.env['stock.warehouse'].search([])
        data['warehouses'] = [{'name': wh.name, 'code': wh.code} for wh in warehouses]

        quants = self.env['stock.quant'].read_group([], ['quantity:sum', 'value:sum'], ['location_id'])
        valuation_data = []
        for q in quants:
            if q['location_id']:
                location_id = q['location_id'][0]
                location = self.env['stock.location'].browse(location_id)
                if location.usage == 'internal':
                    value_number = round(q.get('value', 0), 2)
                    valuation_data.append({
                        'warehouse': location.display_name,
                        'value': value_number
                    })
        data['inventory_valuation'] = valuation_data

        products = self.env['product.product'].search([('purchase_ok', '=', True)])
        avg_expense_data = []

        purchase_date_domain = []
        if date_domain:
            purchase_date_domain = [('order_id.date_order', item[1], item[2]) for item in date_domain]

        for product in products:
            purchase_lines = self.env['purchase.order.line'].search(
                [('product_id', '=', product.id)] + purchase_date_domain
            )
            total_cost = 0
            total_qty = 0

            for line in purchase_lines:
                purchase_cost = line.price_unit or 0
                qty = line.product_qty or 1

                landed_lines = self.sudo().env['stock.landed.cost.lines'].search([('product_id', '=', product.id)])
                landed_cost = sum(lc.price_unit for lc in landed_lines)

                total_cost += (purchase_cost + landed_cost) * qty
                total_qty += qty

            average_expense = total_cost / total_qty if total_qty else 0

            if total_qty > 0:
                avg_expense_data.append({
                    'product': product.name,
                    'average_expense': round(average_expense, 2)
                })

        data['average_expense'] = avg_expense_data

        return data