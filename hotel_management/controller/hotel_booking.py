from datetime import datetime
from odoo import http
from odoo.http import request


class WebsiteHotelBooking(http.Controller):
    @http.route(['/hotel/get_rooms'], type='json', auth="public", website=True)
    def get_rooms(self, bed=None, facility_ids=None, **kw):
        domain = [('state', '=', 'available')]
        if bed:
            domain.append(('bed', '=', bed))
        if facility_ids:
            facility_ids = [int(fid) for fid in facility_ids]  # convert to int
            domain.append(('facility_ids', 'in', facility_ids))

        rooms = request.env['hotel.rooms'].sudo().search(domain)
        print("Domain",domain)
        return [{'id': room.id, 'name': room.name} for room in rooms]

    @http.route(['/hotel/booking/submit'], type='http', auth="user", methods=['POST'], website=True, csrf=False)
    def hotel_booking_submit(self, **post):
        print("POST DATA:", post)
        days = int(post.get('days', 1))
        bed = post.get('bed')
        booking_time_str = post.get('booking_time')
        booking_time = datetime.strptime(booking_time_str, "%Y-%m-%dT%H:%M") if booking_time_str else False
        partner = request.env.user.partner_id


        facility_ids = request.httprequest.form.getlist('facility_ids')
        facility_ids = [int(fid) for fid in facility_ids if fid]

        domain = [('state', '=', 'available')]
        if bed:
            domain.append(('bed', '=', bed))
        if facility_ids:
            domain.append(('facility_ids', 'in', facility_ids))

        rooms = request.env['hotel.rooms'].sudo().search(domain)
        print("plolp", rooms, domain)

        room_id = int(post.get('room_id')) if post.get('room_id') else False

        booking = request.env['hotel.accommodation'].sudo().create({
            'guest_id': partner.id,
            'bed': bed,
            'expected_days': days,
            'booking_time': booking_time,
            'facility_ids': [(6, 0, facility_ids)],
            'rooms_id': room_id
        })
        print(booking)
        return request.render("hotel_management.template_hotel_booking_success", {
            'booking': booking,
            'partner': partner,
            'rooms': rooms,
        })

