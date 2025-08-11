from odoo import models, fields, api
from datetime import date, timedelta
from odoo.exceptions import UserError,ValidationError


class PropertyOffers(models.Model):
    _name = "property.offers"
    _order = "price desc"

    price = fields.Integer()
    # offers_id = fields.Many2one('estate.property', string="Offers")
    partner_id= fields.Many2one("res.partner", string="Partner")
    property_id= fields.Many2one('estate.property', string="Property")
    offer_status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')]
    )
    # create_date = fields.Datetime(string="Created Date", readonly=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(default=fields.Datetime.now(), string="Deadline", compute="_compute_date_deadline",
                                inverse="_inverse_date_deadline")
    seller_id = fields.Many2one('res.users', string='Salesperson', index=True, tracking=True,
                              default=lambda self: self.env.user)
    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            today = fields.Datetime.now()
            record.date_deadline = (today + timedelta(days=record.validity)).date()
        # record.date_deadline = fields.Datetime.now() + datetime.timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            today = fields.Date.context_today(record)
            if record.date_deadline:
                record.validity = (record.date_deadline - today).days



    # def sold(self):
    #     if "cancelled" in self.mapped("status"):
    #         raise UserError("Canceled properties cannot be sold.")
    #     return self.write({"status": "sold"})
    #

    # def action_accept(self):
    #     if "accepted" in self.mapped("offer_status"):
    #         raise UserError("Canceled properties cannot be sold.")
    #     return self.write({"offer_status":"accepted"})
    #
    #
    #
    #
    #
    #
    # def action_refuse(self):
    #     return self.write(
    #         {
    #             "offer_status": "refused",
    #         }
    #     )

    def action_accept(self):
        for record in self:
            if record.property_id.selling_price == 0:
                record.offer_status = 'accepted'
                record.property_id.selling_price = record.price
                record.property_id.user_id = record.seller_id
            else:
                raise ValidationError('An offer has already been approved for this property.')
        return True

    def action_refuse(self):
        for record in self:
            record.offer_status = 'refused'
            if record.offer_status == 'refused':
                record.property_id.selling_price = 0
                record.property_id.user_id = ''

    # def action_accept(self):
    #     if "accepted" in self.mapped("offer_status"):
    #         raise UserError("An offer as already been accepted.")
    #     self.write(
    #         {
    #             "offer_status": "accepted",
    #         }
    #     )
    #     return self.mapped("property_id").write(
    #         {
    #             "offer_status": "accepted",
    #             "selling_price": self.price,
    #             "buyer_id": self.partner_id.id,
    #         }
    #     )
    #
    # def action_refuse(self):
    #     return self.write(
    #         {
    #             "offer_status": "refused",
    #         }
    #     )