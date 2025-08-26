from odoo import http
from odoo.http import request


class WebsiteHotelBooking(http.Controller):

    @http.route(['/hotel/booking'], type='http', auth="public", website=True)
    def hotel_booking_page(self, **kwargs):
        """ Show available rooms with booking form """
        rooms = request.env['hotel.rooms'].sudo().search([('state', '=', 'available')])
        return request.render("hotel_management.template_hotel_booking_form", {
            'rooms': rooms,

        })

    @http.route(['/hotel/booking/submit'], type='http', auth="public", website=True, csrf=False)
    def hotel_booking_submit(self, **post):
        """ Save booking when user submits the form """
        guest = request.env['res.partner'].sudo().create({
            'name': post.get('name'),
            'email': post.get('email'),
            'phone': post.get('phone'),
            'is_hotel_guest': True,
        })

    # @http.route(['/hotel/booking/submit'], type='http', auth='public', website=True, methods=['POST'])
    # def hotel_booking_submit(self, **post):
    #     request.env['res.partner'].sudo().create({
    #         'name': post.get('name'),
    #         'phone': post.get('phone'),
    #         'email': post.get('email'),
    #     })
    #     return request.redirect('/thank-you-page')

        booking = request.env['hotel.accommodation'].sudo().create({
            'guest_id':guest.id,
            'bed':int(post.get('room_id')),
            # 'facility_ids':int(post.get('facility')),
            'rooms_id': int(post.get('room_id')),
            'expected_days': int(post.get('days')),
            'number_of_guests': int(post.get('guests')),

        })

        return request.render("hotel_management.template_hotel_booking_success", {
            'booking': booking,
        })