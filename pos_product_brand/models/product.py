from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    brand_name=fields.Char(string="Brand")

    @api.model
    def _load_pos_data_fields(self, config_id):
        data = super()._load_pos_data_fields(config_id)
        data += ['brand_name']
        return data