import json
import time
from datetime import datetime
from odoo import http
from odoo.http import request


class WebsiteHotelGallery(http.Controller):
    """
          1. Serving hotel gallery images to the website (via JSON for frontend carousels).
          2. Processing hotel booking submissions made by users from the website.
    """
    @http.route('/hotel_gallery_data', type='json', auth="public", website=True)
    def get_hotel_gallery(self):
        """
             `type="json"`: Can be called via JavaScript (RPC) to fetch data.
             Uses Odoo ORM (`hotel.gallery`) with `.search_read()` to get all images.
             Retrieves only `name` and `image_1920` fields to avoid unnecessary data.
             Generates a unique ID (`hg-<timestamp>`) to prevent caching issues when reloading carousels on the frontend.
        """
        images = request.env['hotel.gallery'].sudo().search_read(
            [], ['name', 'image_1920']
        )
        unique_id = "hg-%d" % int(time.time() * 1000)
        return {
            'images': images,
            'unique_id': unique_id
        }



    @http.route(['/hotel/booking/submit'], type='http', auth="user", methods=['POST'], website=True, csrf=False)
    def hotel_booking_submit(self, **post):
        """
        - `auth="user"`: Only logged-in users can book.
        - Accepts `POST` form data containing:
            * days (int): number of days booked
            * bed (str): bed type
            * booking_time (datetime): selected booking date/time
            * guests (int): number of guests
            * guest_lines (json): additional guest info (id, age, gender)
            * facility_ids (list[int]): facilities selected by user
        - Parses form data into proper types.
        - Builds `guest_vals` list of guests to create linked accommodation records.
        - Creates a new `hotel.accommodation` record with:
            guest, bed, days, booking time, facilities, guests, booking method.
        - Renders success template with booking details.

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
        print("sfc", facility_ids)
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

