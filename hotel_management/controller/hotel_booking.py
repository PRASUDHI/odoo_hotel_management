from odoo import http
from odoo.http import request


class WebsiteHotelBooking(http.Controller):


    @http.route(['/hotel/booking/submit'], type='http', auth="public", methods=['POST'], website=True, csrf=False)
    def hotel_booking_submit(self, **post):
        name = post.get('name')
        days = int(post.get('expected_days', 1))

        """ Save booking when user submits the form """
        guest = request.env['res.partner'].sudo().create({
            'name': name,
            'email': post.get('email'),
            'phone': post.get('phone'),
            'is_hotel_guest': True,
        })

        booking = request.env['hotel.accommodation'].sudo().create({
            'guest_id': guest.id,
            # 'bed':int(post.get('bed')),
            # 'facility_ids':int(post.get('facility')),
            # 'rooms_id': int(post.get('room_id')),
            'expected_days': days,
            'number_of_guests': int(post.get('guests')),
        })
        # return request.redirect('/thank-you-page')
        return request.render("hotel_management.template_hotel_booking_success", {
            'booking': booking,
        })
        