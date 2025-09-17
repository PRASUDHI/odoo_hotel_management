import json
import time
from datetime import datetime
from odoo import http
from odoo.http import request


class WebsiteHotelGallery(http.Controller):
    @http.route('/hotel_gallery_data', type='json', auth="public", website=True)
    def get_hotel_gallery(self):
        """
            This defines a URL endpoint. 'type="json"' means it's for RPC calls from JavaScript.
            Use Odoo's ORM to search the 'hotel.gallery' model.
            .search_read() fetches all records and reads the 'name' and 'image_1920' fields.
            Generate a unique ID based on the current time to prevent browser caching issues for the carousel.
        """
        images = request.env['hotel.gallery'].sudo().search_read(
            [], ['name', 'image_1920']
        )
        unique_id = "hg-%d" % int(time.time() * 1000)
        return {
            'images': images,
            'unique_id': unique_id
        }

    # @http.route('/get_hotel_rooms', auth="public", type='json', website=True)
    # def get_hotel_rooms(self):
    #     rooms = request.env['hotel.rooms'].sudo().search_read(
    #         fields=['name', 'bed', 'rent', 'facility_ids', 'state', 'image_1920']
    #     )
    #     for room in rooms:
    #         facilities = request.env['hotel.facility'].sudo().browse(room['facility_ids'])
    #         room['facilities'] = [f.name for f in facilities]
    #
    #         if room.get('bed'):
    #             try:
    #                 bed = request.env['hotel.rooms'].sudo().browse(int(room['bed']))
    #                 room['bed'] = bed.name if bed.exists() else ""
    #             except Exception:
    #                 field = request.env['hotel.rooms']._fields['bed']
    #                 room['bed'] = dict(field.selection).get(room['bed'], room['bed'])
    #
    #         if room.get('state'):
    #             field = request.env['hotel.rooms']._fields['state']
    #             room['state'] = dict(field.selection).get(room['state'], room['state'])
    #
    #         room['image'] = f"/web/image/hotel.rooms/{room['id']}/image_1920" if room.get('image_1920') else ""
    #
    #     return {"rooms": rooms}

    @http.route(['/hotel/booking/submit'], type='http', auth="user", methods=['POST'], website=True, csrf=False)
    def hotel_booking_submit(self, **post):
        """
              Extract all the data from the form fields
        """
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
                guest_id = g.get('guest_id')
                if guest_id:
                    guest_vals.append((0, 0, {
                        'guest_id': int(guest_id),
                        'age': g.get('age') or False,
                        'gender': g.get('gender') or False,
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
        })

