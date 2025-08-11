from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = 'name desc'

    name = fields.Char('Name', required=True)
    description = fields.Text()
    postcode = fields.Char()
    data_availability = fields.Date(default=fields.Datetime.now())
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    total = fields.Float(compute="total_area")

    @api.depends("living_area", "garden_area")
    def total_area(self):
        for record in self:
            record.total = record.garden_area + record.living_area

    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )

    status = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')],
        string='Status'
    )

    can_show_action_buttons = fields.Boolean(compute="_compute_button_visibility", store=False)

    @api.depends('status')
    def _compute_button_visibility(self):
        for record in self:
            record.can_show_action_buttons = record.status not in ['sold', 'cancelled']

    property_type = fields.Many2one('property.type', string="Type")
    buyer = fields.Many2one("res.partner", string="Buyer")
    user_id = fields.Many2one('res.users', string='Salesperson', index=True, tracking=True,
                              default=lambda self: self.env.user)
    property_tag = fields.Many2many('property.tag')
    property_p = fields.One2many('property.offers', 'property_id', string="Property")
    best_offer = fields.Float(compute="best_price")

    @api.depends("property_p")
    def best_price(self):
        for record in self:
            record.best_offer = max(record.property_p.mapped('price')) if record.property_p else 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def sold(self):
        if "cancelled" in self.mapped("status"):
            raise UserError("Canceled properties cannot be sold.")
        return self.write({"status": "sold"})

    def cancelled(self):
        if "sold" in self.mapped("status"):
            raise UserError("Sold properties cannot be canceled.")
        return self.write({"status": "cancelled"})

    @api.constrains('expected_price')
    def _check_expected_price(self):
        for record in self:
            if record.expected_price < 0:
                raise ValidationError("The offer price should be a positive number.")
