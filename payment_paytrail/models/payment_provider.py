# -*- coding: utf-8 -*-
import hmac
import hashlib
import json
import requests
import uuid
from datetime import datetime, timezone
from math import floor

from odoo import fields, models, _
from odoo.exceptions import ValidationError


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('paytrail', "Paytrail")],
        ondelete={'paytrail': 'set default'}
    )
    paytrail_merchant_identifier = fields.Char(
        string="Paytrail Merchant ID",
        help="The key solely used to identify the account with Paytrail.",
        required_if_provider='paytrail',
    )
    paytrail_secret_key = fields.Char(
        string="Paytrail Secret Key",
        required_if_provider='paytrail',
        groups='base.group_system',
    )

    def _paytrail_calculate_signature(self, headers: dict, body: str = '') -> str:
        # print("erty")
        self.ensure_one()

        # 1. Collect all 'checkout-' headers.
        checkout_headers = {k: v for k, v in headers.items() if k.startswith('checkout-')}

        # 2. Sort headers alphabetically by key and format them as "key:value".
        # This is required by Paytrail for a consistent signature.
        data_to_sign_parts = [f"{key}:{value}" for key, value in sorted(checkout_headers.items())]

        # 3. Append the request body.
        data_to_sign_parts.append(body)

        # 4. Join the final list into a single string with newlines.
        message = '\n'.join(data_to_sign_parts)

        # 5. Compute the HMAC-SHA256 hash using the secret key.
        signature = hmac.new(
            self.paytrail_secret_key.encode('utf-8'),
            message.encode('utf-8'),
            digestmod=hashlib.sha256
        ).hexdigest()

        return signature

    def paytrail_create_payment(self, transaction):
        self.ensure_one()

        # Convert amount to EUR cents, as required by Paytrail
        from_currency = transaction.currency_id
        to_currency = self.env['res.currency'].search([('name', '=', 'EUR')], limit=1)

        if not to_currency:
            raise ValidationError(_("The EUR currency is not available in the system."))

        # Convert amount and ensure it's an integer (cents)
        converted_amount = from_currency._convert(
            transaction.amount, to_currency, self.env.company, fields.Date.today()
        )
        amount_in_cents = floor(converted_amount * 100)

        # Build the payload for the API request
        base_url = self.get_base_url()
        payload = {
            "stamp": str(uuid.uuid4()),
            "reference": transaction.reference,
            "amount": amount_in_cents,
            "currency": "EUR",
            "language": "EN",
            "items": [{
                "unitPrice": amount_in_cents,
                "units": 1,
                "vatPercentage": 0,
                "productCode": transaction.reference,
                "description": transaction.reference
            }],
            "customer": {"email": transaction.partner_email},
            "redirectUrls": {
                "success": f"{base_url}/payment/paytrail/success",
                "cancel": f"{base_url}/payment/paytrail/cancel",
            },
        }

        # Build headers for the API request
        headers = {
            "checkout-account": self.paytrail_merchant_identifier,
            "checkout-algorithm": "sha256",
            "checkout-method": "POST",
            "checkout-nonce": str(uuid.uuid4()),
            "checkout-timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            "content-type": "application/json; charset=utf-8",
        }

        # Create the JSON body and calculate the signature
        body = json.dumps(payload, separators=(',', ':'))
        headers["signature"] = self._paytrail_calculate_signature(headers, body)

        # Send the request to Paytrail
        api_url = "https://services.paytrail.com/payments"
        try:
            response = requests.post(api_url, headers=headers, data=body, timeout=20)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        except requests.exceptions.RequestException as e:
            raise ValidationError(_("Paytrail Error: Could not connect to the payment gateway. %s", e))

        response_data = response.json()
        return response_data.get("href")
