import json

from odoo import http
from odoo.http import request

class WebsiteFoodOrder(http.Controller):

    @http.route(['/my/food'], type='http', auth="user", website=True)
    def portal_food_list(self, **kw):
        foods = request.env['hotel.food'].sudo().search([])
        return request.render("hotel_management.portal_food_list_template", {
            'foods': foods
        })

    @http.route(['/my/food/add_to_list'], type='http', auth="user", website=True, csrf=False, methods=["POST"])
    def add_to_list(self, **post):
        print("POST DATA:", post)
        food_id = int(post.get('food_id'))
        qty = int(post.get('quantity', 1))
        food = request.env['hotel.food'].sudo().browse(food_id)

        cart = request.session.get('food_cart', [])
        cart.append({
            'food_id': food.id,
            'name': food.name,
            'quantity': qty,
            'price': food.price,
            'total': food.price * qty,
        })
        request.session['food_cart'] = cart

        return request.redirect('/my/food/cart')

    @http.route(['/my/food/cart'], type='http', auth="user", website=True)
    def view_cart(self, **kw):
        cart = request.session.get('food_cart', [])
        return request.render("hotel_management.portal_food_cart_template", {
            'cart': cart
        })

    @http.route(['/my/food/cart/confirm'], type='http', auth="user", website=True)
    def confirm_cart(self, **kw):
        cart = request.session.get('food_cart', [])
        if not cart:
            return request.redirect('/my/food')
        partner = request.env.user.partner_id


        order = request.env['order.food'].sudo().create({
            'room_id': request.env['hotel.accommodation'].sudo().search([('room_status', '=', 'check_in')], limit=1).id,
            'guest_id':partner,
            'order_status': 'draft'

        })

        for line in cart:
            request.env['order.list'].sudo().create({
                'name': line['name'],
                'quantity': line['quantity'],
                'price': line['price'],
                'total': line['total'],
                'food_list_id': order.id,
            })

        request.session['food_cart'] = []

        return request.redirect('/my/food')

