from odoo import models, fields, api
from odoo.fields import Many2one, Many2many


class OrderFood(models.Model):
    """
        model for ordering the food for the guests
    """
    _name = "order.food"
    _description = "Order Food"
    _rec_name = "room_id"

    room_id = fields.Many2one('hotel.accommodation', string="Room", domain="[('room_status', '=', 'check_in')]",
                              ondelete='cascade')
    guest_id = fields.Many2one('res.partner', string="Guest", compute="_compute_guest", store=True)
    order_time = fields.Datetime(string="Order Time", default=fields.Datetime.now())
    food_category_ids = fields.Many2many('food.category', string="Category")
    description = fields.Html()
    quantity = fields.Float(readonly=False)
    food_item_ids = Many2many('hotel.food', string="Food Item", compute="_compute_food_item_ids", store=True,
                              readonly=False)
    food_order_ids = fields.One2many('order.list', 'food_list_id')
    food_total = fields.Float(string="Food Total",compute="_compute_food_total",store=True)
    order_list_ids = fields.One2many('order.list', 'food_list_id', string="Food Orders")
    order_status = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('cancel', 'Cancel')
    ], string='Order Status', default='draft')

    @api.depends('food_category_ids')
    def _compute_food_item_ids(self):
        """
            Show the food_items based on the choose category of food
        """
        for record in self:
            if record.food_category_ids:
                food_items = self.env['hotel.food'].search([
                    ('food_id', 'in', record.food_category_ids.ids)
                ])
                record.food_item_ids = food_items
            else:
                record.food_item_ids = []

    @api.depends('room_id')
    def _compute_guest(self):
        """
            Show the guest name of that room.
        """
        for record in self:
            record.guest_id = record.room_id.guest_id

    @api.depends('order_list_ids.total')
    def _compute_food_total(self):
        """
        Calculate total food by each order line
        """
        for rec in self:
            rec.food_total = sum(line.total for line in rec.order_list_ids)

    def action_confirm(self):
        for record in self:
            record.order_status = 'confirm'
            print("rerert", record.room_id, record.room_id.id)
            print("rerert", record.food_total)
            self.env['hotel.payment.line'].create({
                'name': "Food Items for Room",
                'total': record.food_total,
                'accommodation_id': record.room_id.id,
            })

    def action_cancel(self):
        for record in self:
            record.order_status = 'cancel'




class OrderFoodList(models.Model):
    """
        model for adding ordered food in list
    """
    _name = "order.list"
    _description = "Order List"

    name = fields.Char()
    description = fields.Html()
    quantity = fields.Integer()
    price = fields.Monetary(string=" Unit Price")
    total = fields.Float(string="Total", compute="_compute_total", store=True)
    food_list_id = fields.Many2one('order.food')
    accommodation_id = fields.Many2one('hotel.accommodation', string="Accommodation", ondelete='cascade')
    room_id = fields.Many2one('hotel.rooms', string="Room")
    uom_id = fields.Many2one('uom.uom', string="UOM")
    company_id = fields.Many2one(
        'res.company', store=True, copy=False, string="Company",
        default=lambda self: self.env.user.company_id.id
    )
    currency_id = fields.Many2one(
        'res.currency', string="Currency", related="company_id.currency_id",
        default=lambda self: self.env.user.company_id.currency_id.id
    )

    # subtotal =fields.Float(string="Total", compute="_compute_subtotal", store=True)

    @api.depends('quantity', 'price')
    def _compute_total(self):
        """
            Calculate the food total by unit price and quantity
        """
        for rec in self:
            rec.total = rec.quantity * rec.price
