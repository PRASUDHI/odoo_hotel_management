# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class InventoryDashboardController(http.Controller):

    @http.route('/inventory/dashboard/data', type='json', auth='user')
    def get_data(self, filters=None):
        if filters is None:
            filters = {}
        return request.env['inventory.dashboard'].get_dashboard_data(filters)
