from odoo import models,fields


class FoodCategory(models.Model):
    """
        Model for the choosing the food category
    """
    _name ="food.category"
    _description = "Food Category"


    name = fields.Char('Name', required=True)