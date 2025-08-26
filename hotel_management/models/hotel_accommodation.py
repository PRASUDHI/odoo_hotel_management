from email.policy import default

from odoo import models, fields, _, api, Command
from odoo.exceptions import ValidationError
from datetime import timedelta, date, datetime


class HotelAccommodation(models.Model):
    """
        Accommodation model for the choosing the rooms for guests and enter the number of guests
        in payment tab having the total rent and overall food cost
    """
    _name = "hotel.accommodation"
    _description = "Hotel Accommodation"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "reference_number"
    _order = 'check_in desc'
    _check_company_auto = True

    reference_number = fields.Char(default=lambda self: _('New'), readonly=True, copy=False,help="Reference Number of the book")
    guest_id = fields.Many2one('res.partner', string="Guest Name",required=True, domain="[('is_hotel_guest', '=', True)]")
    guest_ids = fields.Many2many('res.partner', string='Guests')
    number_of_guests = fields.Integer(string="Number of Guests", default=1)
    check_in = fields.Datetime("Check In")
    check_out = fields.Datetime("Check Out")
    cancel = fields.Datetime("Cancel")
    address_attach = fields.Binary(attachment=True, string="Address Proof",copy=False)
    bed = fields.Selection(string='Bed',selection=[('single', 'Single'), ('double', 'Double'), ('dormitory', 'Dormitory')])
    facility_ids = fields.Many2many('hotel.facility', string="Facility")
    rooms_id = fields.Many2one('hotel.rooms',string="Room",required=True)
    filtered_room_ids = fields.Many2many('hotel.rooms', compute='_compute_filtered_rooms', string="Filtered Rooms")
    room_status = fields.Selection([('draft', 'Draft'),('check_in', 'Check In'),('check_out', 'Check Out'),('cancel', 'Cancel')], string='Room Status', default='draft')
    expected_days = fields.Integer(string='Expected Days')
    expected_date = fields.Date(string='Expected CheckOut', compute='_compute_expected_date', store=True, readonly=True)
    age = fields.Integer('Age')
    gender = fields.Selection(string='Gender',selection=[('male', 'Male'), ('female', 'Female')])
    invoice_id = fields.Many2one('account.move', string="Invoice")
    payment_state = fields.Selection(related="invoice_id.payment_state", store=True, string="Payment State")
    move_type = fields.Selection(related="invoice_id.move_type", store=True, string="Move Type")
    accommodation_ids = fields.One2many('hotel.guest', 'accommodation_line_id')
    total_rent = fields.Float(string="Total Rent", compute="_compute_total_rent", store=True)
    total_amount = fields.Float(string="Total Amount", compute="_compute_total_amount", store=True, currency_field="currency_id")
    company_id = fields.Many2one('res.company', store=True, copy=False, string="Company",default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency", related="company_id.currency_id", default=lambda self: self.env.user.company_id.currency_id.id)
    order_list_ids = fields.One2many('order.list', 'accommodation_id', string="Food Orders")
    payment_line_ids = fields.One2many('hotel.payment.line', 'accommodation_id', string='Payment Lines')
    payment_id =fields.Many2one('hotel.payment.line')
    expected_date_color = fields.Char(compute='_compute_expected_date_color', store=False)
    active = fields.Boolean(default=True)
    invoice_count = fields.Integer(string="Invoices", compute="_compute_invoice_count", default=0)
    food_order_count = fields.Integer(string="Food Orders", compute="_compute_food_order_count", default=0)


    def _compute_invoice_count(self):
        """
            To compute the number of invoice
        """
        for record in self:
            record.invoice_count = self.env['account.move'].search_count([('accommodation_id', '=', record.id)])

    def action_view_invoices(self):
        """
            Return the action for the views of the invoices linked to the transaction
        """
        self.ensure_one()
        return  {
            'type': 'ir.actions.act_window',
            'name': 'Invoices',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [
                ('move_type', '=', 'out_invoice'),
                ('accommodation_id', '=', self.id)
            ],
            'context': {'default_accommodation_id': self.id},
        }
    def _compute_food_order_count(self):
        """
                compute the ordered food count with search_count
        """
        for record in self:
            record.food_order_count = self.env['order.food'].search_count([('room_id', '=', record.id)])


    def action_view_food_orders(self):
        """
            Return the action for the views of the ordered food linked to the accommodation
        """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Food Orders',
            'res_model': 'order.food',
            'view_mode': 'list,form',
            'domain': [('room_id', '=', self.id)],
            'context': {
                'default_room_id': self.id
            },
        }
    def action_archive_accommodation(self):
        """
            archive the cancelled accommodation if it is cancelled two days ago
        """
        two_days_ago = datetime.today() - timedelta(days=2)
        records = self.search([
            ('room_status', '=', 'cancel'),
            ('cancel', '<', two_days_ago)
        ])
        records.write({'active': False})

    @api.model
    def action_send_checkout_email(self):
        """
            send mail to the guest whose check out date is today
        """
        today = date.today()
        records = self.search([
            ('check_in', '!=', False),
            ('expected_date', '=', today),
            ('room_status', '!=', 'cancel')
        ])

        template = self.env.ref('hotel_management.mail_template_checkout')
        for rec in records:
            if rec.guest_id and rec.guest_id.email:
                template.send_mail(rec.id, force_send=True)

    @api.depends('check_out', 'expected_date','room_status')
    def _compute_expected_date_color(self):
        """
            Yellow: Expected date = current day
            Red: Expected date = current day but not Check-out
        """
        today = date.today()
        for rec in self:
            if rec.room_status != 'check_in' or not rec.expected_date:
                rec.expected_date_color = ''
                continue
            if rec.expected_date == today:
                rec.expected_date_color = 'yellow'
            elif rec.expected_date < today:
                rec.expected_date_color = 'red'
            else:
                rec.expected_date_color = ''

    @api.depends('order_list_ids.total')
    def _compute_food_total(self):
        """
        Calculate total food by each order line
        """
        for rec in self:
            rec.food_total = sum(line.total for line in rec.order_list_ids)

    @api.depends('check_in', 'check_out', 'rooms_id.rent','payment_id.total')
    def _compute_total_rent(self):
        """
                compute the total rent based on check_in ,check_out and rent of that particular room.
        """
        for rec in self:
            if rec.check_in and rec.check_out and rec.rooms_id:
                delta = rec.check_out.date() - rec.check_in.date()
                num_days = delta.days
                if num_days == 0:
                    num_days = 1
                rec.total_rent = num_days * rec.rooms_id.rent

            else:
                rec.total_rent = rec.rooms_id.rent or rec.payment_id.total


    @api.depends( 'payment_line_ids.total')
    def _compute_total_amount(self):
        """
            Compute the total amount of food, rent, and other payment lines
        """
        for rec in self:
            rec.total_amount= sum(line.total for line in rec.payment_line_ids)

    @api.depends('facility_ids', 'bed')
    def _compute_filtered_rooms(self):
        """
                Filter the rooms based on bed type,facility,state, otherwise show all rooms
        """
        for rec in self:
            domain = []
            if rec.facility_ids:
                domain.append(('facility', 'in', rec.facility_ids.ids))
            if rec.bed:
                domain.append(('bed', '=', rec.bed))
            domain.append(('state', '=', 'available'))

            rec.filtered_room_ids = self.env['hotel.rooms'].search(domain)

    @api.depends('expected_days', 'check_in','room_status')
    def _compute_expected_date(self):
        """
               Calculate the expected date based on check_in and expected date
        """
        for record in self:
            if record.room_status == 'check_in' and record.check_in:
                if record.expected_days == 0:
                    record.expected_date = record.check_in.date()
                else:
                    record.expected_date = (record.check_in + timedelta(days=record.expected_days)).date()
            else:
                record.expected_date = False


    @api.constrains('number_of_guests')
    def guest_numbers(self):
        """
                Check the number of guests equal to the enter guest
        """
        for record in self:
            if record.number_of_guests != len(record.guest_id) + len(record.accommodation_ids):
                raise ValidationError("Enter guest must be equal to number of Guest")

    def write(self, vals):
        """
            Update the record after the validation error in guest number
        """
        result = super(HotelAccommodation, self).write(vals)
        self.guest_numbers()
        return result


    def create(self, vals):
        """
            For creating Reference number
        """
        if vals.get('reference_number', _('New')) == _('New'):
            vals['reference_number'] = self.env['ir.sequence'].next_by_code('hotel.accommodation')
        return super(HotelAccommodation, self).create(vals)

    def action_check_in(self):
        """
            Action for check_in, if the address proof attachment is not added in chatter raise a validation error,
            Change the room_status to Check in and room state to unavailable
            Record the Datetime in field CheckIn

            Update the room_rent automatically in payment tab
        """
        for record in self:
            # if record.message_attachment_count == 0:
            #     raise ValidationError("Please add attachment")
            record.room_status = 'check_in'
            record.rooms_id.state = 'not_available'
            record.check_in = fields.Datetime.now()
            product = self.env.ref("hotel_management.product_product_room_rent")

            self.env['hotel.payment.line'].create({
                'name': product.name,
                'description': 'Room Rent',
                'quantity': 1,
                'price':  record.rooms_id.rent or product.list_price,
                'total': record.rooms_id.rent or product.list_price,
                'uom_id': product.uom_id.id,
                'accommodation_id': record.id,
            })

    def action_check_out(self):
        """
            Action for check_out,Record the Datetime in field Checkout
            Calculate the rent based on checkout date,Room state change to available
            Opens the invoice with the room rent and food order list
        """
        for record in self:
            record.room_status = 'check_out'
            record.check_out = fields.Datetime.now()
            if record.check_in and record.check_out and record.rooms_id:
                delta = record.check_out.date() - record.check_in.date()
                num_days = delta.days
                if num_days == 0:
                    num_days = 1
                record.total_rent = num_days * record.rooms_id.rent
            if record.rooms_id:
                record.rooms_id.state = 'available'

        invoice = self.env['account.move'].create({
            'partner_id': self.guest_id.id,
            'move_type': 'out_invoice',
            'accommodation_id': self.id,
            'invoice_line_ids': [
                (0, 0, {
                    'name': line.name,
                    'quantity': line.quantity,
                    'price_unit': line.price,
                    'price_subtotal':line.total,
                    'product_uom_id': line.uom_id.id,
                }) for line in self.payment_line_ids],
        })
        record.invoice_id = invoice.id
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'view_mode': 'form',
        }

    def action_cancel(self):
        """
            Action to cancel the Accommodation
        """
        for record in self:
            record.room_status = 'cancel'
            record.cancel = fields.Datetime.now()
