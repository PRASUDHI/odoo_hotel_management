from odoo import models, fields, api

class HotelPaymentLine(models.Model):
    _name = 'hotel.payment.line'
    _description = 'Accommodation Charges'

    name = fields.Char()
    description = fields.Html()
    quantity = fields.Integer()
    price = fields.Monetary(string="Price", currency_field="currency_id")
    company_id = fields.Many2one('res.company', store=True, copy=False, string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency", related="company_id.currency_id",
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    total = fields.Float(string="Total", compute="_compute_total", store=True)
    food_list_id = fields.Many2one('order.food')
    accommodation_id = fields.Many2one('hotel.accommodation', string="Accommodation",ondelete='cascade')
    room_id = fields.Many2one('hotel.rooms', string="Room")
    uom_id = fields.Many2one('uom.uom', string="UOM")
    total_rent = fields.Float(string="Total Rent")


    @api.depends('quantity', 'price')
    def _compute_total(self):
        """
            Compute total for the rent of room with no.of days
        """
        for rec in self:
            rec.total = rec.quantity * rec.price

