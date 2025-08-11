from odoo import models,fields


class HotelFacility(models.Model):
    """
        model for displaying the facility available in hotel
    """
    _name ="hotel.facility"
    _description = "Hotel Facility"

    name = fields.Char('Name', required=True)


