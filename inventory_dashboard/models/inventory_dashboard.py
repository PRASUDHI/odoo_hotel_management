# -*- coding: utf-8 -*-
from odoo import models, api
from datetime import datetime, timedelta

class InventoryDashboard(models.Model):
    _name = "inventory.dashboard"
    _description = "Inventory Dashboard Data"

    @api.model
    def get_dashboard_data(self, filters=None):
        """Fetch inventory dashboard data with filters (month, week, year)."""

        move_domain = []      # for stock.move
        pol_domain = []       # for purchase.order.line
        landed_domain = []    # for stock.landed.cost.lines

        # Build date ranges
        start_date, end_date = None, None
        if filters and filters.get('year'):
            year = int(filters['year'])
            start_date = datetime(year, 1, 1)
            end_date = datetime(year, 12, 31, 23, 59, 59)

            if filters.get('month'):
                month = int(filters['month'])
                start_date = datetime(year, month, 1)
                if month == 12:
                    end_date = datetime(year, 12, 31, 23, 59, 59)
                else:
                    end_date = datetime(year, month + 1, 1) - timedelta(seconds=1)

            if filters.get('week'):
                week = int(filters['week'])
                start_date = datetime.strptime(f'{year}-W{week}-1', "%Y-W%W-%w")
                end_date = start_date + timedelta(days=6, hours=23, minutes=59, seconds=59)

            # Apply domains with correct date fields
            move_domain += [('date', '>=', start_date), ('date', '<=', end_date)]
            pol_domain += [('order_id.date_order', '>=', start_date), ('order_id.date_order', '<=', end_date)]
            landed_domain += [('cost_id.date', '>=', start_date), ('cost_id.date', '<=', end_date)]

        data = {}

        # --- Incoming ---
        data['incoming'] = self.env['stock.move'].read_group(
            [('picking_code', '=', 'incoming')] + move_domain,
            ['product_id', 'product_uom_qty:sum'],
            ['product_id']
        )

        # --- Outgoing ---
        data['outgoing'] = self.env['stock.move'].read_group(
            [('picking_code', '=', 'outgoing')] + move_domain,
            ['product_id', 'product_uom_qty:sum'],
            ['product_id']
        )

        # --- Internal ---
        data['internal'] = self.env['stock.move'].read_group(
            [('picking_code', '=', 'internal')] + move_domain,
            ['product_id', 'product_uom_qty:sum'],
            ['product_id']
        )

        # --- Inventory valuation (not date-dependent) ---
        quants = self.env['stock.quant'].read_group([], ['quantity:sum', 'value:sum'], ['location_id'])
        valuation_data = []
        for q in quants:
            if q['location_id']:
                location = self.env['stock.location'].browse(q['location_id'][0])
                if location.usage == 'internal':
                    valuation_data.append({
                        'warehouse': location.display_name,
                        'value': round(q.get('value', 0), 2)
                    })
        data['inventory_valuation'] = valuation_data

        # --- Average expense per product ---
        products = self.env['product.product'].search([('purchase_ok', '=', True)])
        avg_expense_data = []

        for product in products:
            purchase_lines = self.env['purchase.order.line'].search([('product_id', '=', product.id)] + pol_domain)
            total_cost, total_qty = 0, 0

            for line in purchase_lines:
                purchase_cost = line.price_unit or 0
                qty = line.product_qty or 1

                # Landed cost lines for the same product
                landed_lines = self.env['stock.landed.cost.lines'].search(
                    [('product_id', '=', product.id)] + landed_domain
                )
                landed_cost = sum(lc.price_unit for lc in landed_lines)

                total_cost += (purchase_cost + landed_cost) * qty
                total_qty += qty

            avg_expense_data.append({
                'product': product.name,
                'average_expense': round(total_cost / total_qty, 2) if total_qty else 0
            })

        data['average_expense'] = avg_expense_data

        return data