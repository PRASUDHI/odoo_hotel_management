from odoo import models,fields


class HotelManagement(models.Model):

    _name ="hotel.management"
    _description = "Hotel Management"

    name = fields.Char()