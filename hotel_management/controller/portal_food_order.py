from odoo import http
from odoo.http import request

class WebsiteFoodOrder(http.Controller):
    """
        Controller for managing hotel food ordering through the website portal.
    """

    @http.route(['/my/food'], type='http', auth="user", website=True)
    def portal_food_list(self, **kw):
        """
                Render the food menu page with available foods and current cart items.

                - Fetches all available food records (`hotel.food`).
                - Identifies the logged-in user's draft order (`order.food`).
                - Builds a list of cart items (food, quantity, price, subtotal).
                - Renders the `portal_food_list_template` with foods and cart data.
        """
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
        """
                Add a food item to the logged-in user's cart.

                - Finds the guest's active accommodation (room with status 'check_in').
                - Locates or creates a draft order (`order.food`) for the guest.
                - If the food already exists in the cart (`order.list`), increment quantity.
                - Otherwise, create a new order line with the food details.
                - Returns the updated cart items list as JSON.
        """
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
        """
               Confirm the guest's current draft food order.

               - Ensures the user has a draft order with items.
               - Validates that the guest is checked into a room.
               - Updates order status (currently keeps it 'draft' — may need 'confirmed').
               - Returns success response with order ID.
        """
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