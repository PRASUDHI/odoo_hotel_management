from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    partner_id = fields.Many2one('res.partner', string='Customer', required=True)

    @api.onchange('partner_id')
    def _onchange_partner_id(self):

        partner = self.partner_id
        self.pricelist_id = partner.property_product_pricelist.id
        self.partner_invoice_id = partner.address_get(['invoice']).get('invoice')
        self.partner_shipping_id = partner.address_get(['delivery']).get('delivery')
