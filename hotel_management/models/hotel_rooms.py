from odoo import models, fields


class HotelRooms(models.Model):
    """
        model for adding room for hotel
        added facility, bed types, and availability state of room
    """
    _name = "hotel.rooms"
    _description = "Hotel Rooms"
    _check_company_auto = True

    name = fields.Char(string="Room Number")
    bed = fields.Selection(
        string='Bed',
        selection=[('single', 'Single'), ('double', 'Double'), ('dormitory', 'Dormitory')]
    )
    available_beds = fields.Integer()
    rent = fields.Monetary(string="Price", currency_field="currency_id")
    company_id = fields.Many2one('res.company', store=True, copy=False, string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency", related="company_id.currency_id",
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    facility_ids = fields.Many2many('hotel.facility')
    state = fields.Selection(
        string='State',
        selection=[('available', 'Available'), ('not_available', 'Not Available')]
    )
