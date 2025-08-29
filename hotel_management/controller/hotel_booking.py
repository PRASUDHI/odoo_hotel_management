from datetime import datetime

from odoo import http
from odoo.http import request


class WebsiteHotelBooking(http.Controller):

    @http.route(['/hotel/booking/submit'], type='http', auth="user", methods=['POST'], website=True, csrf=False)
    def hotel_booking_submit(self, **post):
        print(post)
        days = int(post.get('expected_days', 1))
        bed = post.get('bed')
        # room_id =post.get('room_id')


        user = request.env.user
        partner = user.partner_id
        booking_time_str = post.get('booking_time')
        booking_time = datetime.strptime(booking_time_str, "%Y-%m-%dT%H:%M") if booking_time_str else False
        # facility_ids = request.httprequest.form.getlist('facility_ids')




        booking = request.env['hotel.accommodation'].sudo().create({
            'guest_id': partner.id,
            'bed': bed,
            'expected_days': days,
            'booking_time': booking_time,
            # 'facility_ids': facility_ids,
            # 'rooms_id':room_id
        })


        return request.render("hotel_management.template_hotel_booking_success", {
            'booking': booking,
            'partner': partner,
        })
