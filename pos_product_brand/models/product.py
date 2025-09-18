from odoo import models, fields, api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    brand_name = fields.Char(string="Brand")

    @api.model
    def _load_pos_data_fields(self, config_id):
        fields_list = super()._load_pos_data_fields(config_id)
        fields_list += ['brand_name']
        return fields_list