from odoo import http
from odoo.http import request


class WebsiteHotelBooking(http.Controller):

    @http.route(['/hotel/booking/submit'], type='http', auth="user", methods=['POST'], website=True, csrf=False)
    def hotel_booking_submit(self, **post):
        print(post)
        days = int(post.get('expected_days', 1))
        bed = post.get('bed')


        user = request.env.user
        partner = user.partner_id


        booking = request.env['hotel.accommodation'].sudo().create({
            'guest_id': partner.id,
            'bed': bed,
            'expected_days': days,
            'number_of_guests': int(post.get('guests')),
        })


        return request.render("hotel_management.template_hotel_booking_success", {
            'booking': booking,
            'partner': partner,
        })
