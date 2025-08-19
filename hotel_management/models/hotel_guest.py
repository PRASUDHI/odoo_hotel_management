from odoo import models, fields, api


class HotelGuests(models.Model):
    """
        model for creating guests/customers in the hotel
    """
    _name ="hotel.guest"
    _description = "Hotel Guest"

    accommodation_line_id=fields.Many2one('hotel.accommodation', ondelete='cascade')
    guest_id=fields.Many2one('res.partner')
    age = fields.Integer('Age')
    gender = fields.Selection(
        string='Gender',
        selection=[('male', 'Male'), ('female', 'Female')]
    )






class ResPartner(models.Model):
    _inherit = "res.partner"


    sale_order_ids=fields.One2many('sale.order','partner_id','sale order')
    is_hotel_guest = fields.Boolean(string="Is Hotel Guest", default=True)



class AccountMove(models.Model):
    _inherit = 'account.move'


    accommodation_id = fields.Many2one('hotel.accommodation',string="Accommodation",ondelete='cascade')