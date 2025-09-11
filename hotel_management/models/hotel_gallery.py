from odoo import models, fields

class HotelGallery(models.Model):
    _name = "hotel.gallery"
    _description = "Hotel Gallery"

    name = fields.Char("Title")
    image_1920 = fields.Image("Image", max_width=1920, max_height=1080)
