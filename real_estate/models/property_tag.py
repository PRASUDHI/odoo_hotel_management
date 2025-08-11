from odoo import models,fields


class PropertyTag(models.Model):
    _name = "property.tag"
    _description = "Property Tag"

    name = fields.Char('Property Tag', required=True)
    color = fields.Integer("Color Index")