from odoo import models, api, _


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.model
    def action_create_sale_order_popup(self):
        active_ids = self.env.context.get('active_ids', [])
        lines = self.browse(active_ids)

        order_line_vals = [(0, 0, {
            'product_id': l.product_id.id,
            'name': l.name,
            'product_uom_qty': l.product_uom_qty,
            'price_unit': l.price_unit,
        }) for l in lines]



        return {
            'type': 'ir.actions.act_window',
            'name': _('Create Sale Order'),
            'res_model': 'sale.order',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_order_line': order_line_vals
            },
        }
