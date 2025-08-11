from odoo import models, fields, api
from odoo.exceptions import UserError


class HotelFood(models.Model):
    _name = "hotel.food"
    _description = "Hotel Food"
    _check_company_auto = True

    name = fields.Char('Name', required=True)
    image = fields.Binary()
    item = fields.Char('Food Item')
    food_id = fields.Many2one('food.category', string="Category")
    price = fields.Monetary(string="Price", currency_field="currency_id")
    company_id = fields.Many2one('res.company', store=True, copy=False, string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency", related="company_id.currency_id",
                                  default=lambda self: self.env.user.company_id.currency_id.id)

    quantity = fields.Integer('Quantity')
    description = fields.Html(string='Description')
    order_list_id = fields.Many2one('order.list')



    def order_food_action_form(self):
        """
            Open a form view When clicking Kanban Tile
        """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hotel.food',
            'target': 'new',
            'res_id': self.id,
            'view_id': self.env.ref('hotel_management.food_list_view_form').id,
            'views': [(self.env.ref('hotel_management.food_list_view_form').id, 'form')],
        }

    def action_create_list(self):
        """
            Clicking on add_to_list create a list on order_list and payment tab
        """
        order_list_id = self.env.context.get('order_list_id')
        room_id = self.env.context.get('room_id')
        vals_list = {
            'name': self.name,
            'quantity': self.quantity,
            'price': self.price,
            'description': self.description,
            'food_list_id': order_list_id,
            'accommodation_id': room_id,

        }
        vals_payment = {
            'name': self.name,
            'quantity': self.quantity,
            'price': self.price,
            'description': self.description,
            'food_list_id': order_list_id,
            'accommodation_id': room_id,

        }

        vals = self.env['order.list'].create(vals_list)
        value = self.env['hotel.payment.line'].create(vals_payment)
        return vals, value




    def action_create_product(self):
        """
            create a product in lunch while creating using automation action
        """

        self.env['lunch.product'].sudo().create({
            'name': self.name or "Sample",
            'price': self.price,
            'category_id': 3,
            'supplier_id': 2,
        })
        return True




