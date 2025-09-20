from odoo import models,fields

class AccountMove(models.Model):
    """
        Inherit account.move object to add field
    """
    _inherit = 'account.move'


    accommodation_id = fields.Many2one('hotel.accommodation',string="Accommodation",ondelete='cascade')