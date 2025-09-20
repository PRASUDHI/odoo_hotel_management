from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'


    due_limit = fields.Float(string="Due Limit")


    @api.model
    def _load_pos_data_fields(self, config_id):
        fields_list = super()._load_pos_data_fields(config_id)
        fields_list += ['due_limit']
        return fields_list