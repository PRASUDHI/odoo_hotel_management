from odoo import models, fields

class PropertyType(models.Model):
    _name = "property.type"
    _description = "Property Type"
    _order = 'sequence desc'

    name = fields.Char('Property types', required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better")
    type = fields.One2many("estate.property", "property_type", string="Properties")
