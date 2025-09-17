from odoo import http
from odoo.http import request

class WebsiteFoodOrder(http.Controller):

    @http.route(['/my/food'], type='http', auth="user", website=True)
    def portal_food_list(self, **kw):
        foods = request.env['hotel.food'].sudo().search([])
        partner = request.env.user.partner_id

        cart_order = request.env['order.food'].sudo().search([
            ('guest_id', '=', partner.id),
            ('order_status', '=', 'draft')
        ], limit=1)

        cart_items = []
        if cart_order:
            cart_items = [
                {
                    "food_id": l.id,
                    "name": l.name,
                    "quantity": l.quantity,
                    "price": l.price,
                    "subtotal": l.quantity * l.price,
                }
                for l in cart_order.order_list_ids
            ]

        return request.render("hotel_management.portal_food_list_template", {
            'foods': foods,
            'cart_items': cart_items,
        })

    @http.route('/food/add_to_cart', type='json', auth='user', website=True)
    def add_to_cart(self, food_id, quantity):
        partner = request.env.user.partner_id
        room = request.env['hotel.accommodation'].sudo().search(
            [('room_status', '=', 'check_in'), ('guest_id', '=', partner.id)],
            limit=1
        )
        order = request.env['order.food'].sudo().search([
            ('guest_id', '=', partner.id),
            ('order_status', '=', 'draft')
        ], limit=1)
        if not order:
            order = request.env['order.food'].sudo().create({
                'room_id': room.id,
                'guest_id': partner.id,
                'order_status': 'draft',
            })

        food = request.env['hotel.food'].sudo().browse(food_id)
        line = request.env['order.list'].sudo().search([
            ('food_list_id', '=', order.id),
            ('name', '=', food.name)
        ], limit=1)

        if line:
            line.quantity += int(quantity)
        else:
             request.env['order.list'].sudo().create({
                'name': food.name,
                'quantity': quantity,
                'price': food.price,
                'description': food.description,
                'food_list_id': order.id,
                'accommodation_id': room.id,
            })

        cart_items = [
            {
                "food_id": l.id,
                "name": l.name,
                "quantity": l.quantity,
                "price": l.price,
                "subtotal": l.quantity * l.price,
            }
            for l in order.order_list_ids
        ]

        return {"success": True, "cart": cart_items}

    @http.route('/food/remove_from_cart', type='json', auth='user', website=True)
    def remove_from_cart(self, line_id):
        partner = request.env.user.partner_id
        order = request.env['order.food'].sudo().search([
            ('guest_id', '=', partner.id),
            ('order_status', '=', 'draft')
        ], limit=1)

        if not order:
            return {"success": False, "error": "No active cart"}

        line = request.env['order.list'].sudo().browse(line_id)
        if line and line.food_list_id.id == order.id:
            line.unlink()

        # Rebuild cart
        cart_items = [
            {
                "food_id": l.id,
                "name": l.name,
                "quantity": l.quantity,
                "price": l.price,
                "subtotal": l.quantity * l.price,
            }
            for l in order.order_list_ids
        ]

        return {"success": True, "cart": cart_items}

    @http.route('/food/confirm_order', type='json', auth='user', website=True)
    def confirm_order(self):
        partner = request.env.user.partner_id
        order = request.env['order.food'].sudo().search([
            ('guest_id', '=', partner.id),
            ('order_status', '=', 'draft'),

        ], limit=1)

        if not order or not order.order_list_ids:
            return {"success": False, "error": "Cart is empty"}

        if not order.room_id or order.room_id.room_status != "check_in":
            return {"success": False, "error": "You must be checked in to confirm an order."}


        order.order_status = 'draft'

        return {"success": True, "order_id": order.id}