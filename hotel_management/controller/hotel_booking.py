import json
from datetime import datetime
from odoo import http
from odoo.http import request


class WebsiteHotelGallery(http.Controller):

    @http.route('/get_hotel_gallery', type='json', auth="public", website=True)
    def get_hotel_gallery(self):
        images = request.env['hotel.gallery'].sudo().search([])
        result = []
        for img in images:
            result.append({
                "id": img.id,
                "name": img.name,
                "image": f"/web/image/hotel.gallery/{img.id}/image_1920" if img.image_1920 else "",
            })
        return {"gallery": result}



    @http.route('/get_hotel_rooms', auth="public", type='json', website=True)
    def get_hotel_rooms(self):
        rooms = request.env['hotel.rooms'].sudo().search_read(
            fields=['name', 'bed', 'rent', 'facility_ids', 'state', 'image_1920']
        )
        for room in rooms:
            facilities = request.env['hotel.facility'].sudo().browse(room['facility_ids'])
            room['facilities'] = [f.name for f in facilities]
            if room.get('image_1920'):
                room['image'] = f"/web/image/hotel.rooms/{room['id']}/image_1920"
            else:
                room['image'] = ""
        return {"rooms": rooms}

    @http.route(['/hotel/booking/submit'], type='http', auth="user", methods=['POST'], website=True, csrf=False)
    def hotel_booking_submit(self, **post):
        print("POST DATA:", post)
        days = int(post.get('days', 1))
        bed = post.get('bed')
        booking_time_str = post.get('booking_time')
        booking_time = datetime.strptime(booking_time_str, "%Y-%m-%dT%H:%M") if booking_time_str else False
        partner = request.env.user.partner_id
        number_of_guests = int(post.get('guests', 1))
        guest_lines = post.get('guest_lines')
        guest_vals = []
        if guest_lines:
            for g in json.loads(guest_lines):
                guest_vals.append((0, 0, {
                    'guest_id': int(g.get('guest_id')),
                    'age': g.get('age'),
                    'gender': g.get('gender'),
                }))


        facility_ids = request.httprequest.form.getlist('facility_ids')
        facility_ids = [int(fid) for fid in facility_ids if fid]

        booking = request.env['hotel.accommodation'].sudo().create({
            'guest_id': partner.id,
            'bed': bed,
            'expected_days': days,
            'booking_time': booking_time,
            'facility_ids': [(6, 0, facility_ids)],
            'number_of_guests': number_of_guests,
            'accommodation_ids': guest_vals,
            'booking_method': "Website"
        })

        return request.render("hotel_management.template_hotel_booking_success", {
            'booking': booking,
            'partner': partner,
            # 'rooms': rooms,
        })

