# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from werkzeug.utils import redirect


class PaymentProviderController(http.Controller):
    @http.route('/payment/paytrail/redirect/<int:transaction_id>', type='http', auth='public')
    def paytrail_redirect(self, transaction_id):
        """Sending request to the Paytrail API"""
        transaction = request.env['payment.transaction'].browse(transaction_id)
        redirect_url = transaction.provider_id.paytrail_create_payment(transaction)
        return redirect(redirect_url, code=302)

    @http.route('/payment/paytrail/success', type='http', auth='public')
    def paytrail_success(self):
        """Set the transaction done from the API response if done"""
        # Access URL parameters from the request.params dictionary
        reference = request.params.get('checkout-reference')
        transaction = request.env['payment.transaction'].search([('reference', '=', reference)])

        if transaction:
            transaction.provider_reference = request.params.get('checkout-transaction-id')
            transaction._set_done()

        return request.redirect('/payment/status')

    @http.route('/payment/paytrail/cancel', type='http', auth='public')
    def paytrail_cancel(self):
        """Set the transaction cancelled from the API response if cancel"""
        # Access URL parameters from the request.params dictionary
        reference = request.params.get('checkout-reference')
        transaction = request.env['payment.transaction'].search([('reference', '=', reference)])

        if transaction:
            transaction.provider_reference = request.params.get('checkout-transaction-id')
            transaction._set_canceled()

        return request.redirect('/payment/status?cancel=true')