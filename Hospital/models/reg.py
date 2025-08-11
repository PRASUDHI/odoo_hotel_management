from odoo import models, fields, api,_
from odoo.exceptions import UserError, ValidationError


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _description = "Appointment"

    # appointment = fields.Char('Name', required=True)
    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True)
    age = fields.Integer(related='patient_id.age', string="Age", readonly=True)
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor", required=True)
    consulting_fee = fields.Float(related='doctor_id.consulting_fee', string="Consulting Fee", store=True, readonly=True )
    department = fields.Selection(related='doctor_id.department', string='Department', store=True, readonly=True)
    appointment_date = fields.Datetime("Appointment Date", required=True)
    notes = fields.Text("Notes")
    doctor_lines = fields.Many2one('hospital.doctor', string="Doctor")
    appointment_status = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft')

    # def action_done(self):
    #     for record in self:
    #         if record.patient_id.gender == 'male':
    #             record.appointment_status == 'done'
    #         else:
    #             raise ValidationError('An offer has already been approved for this property.')
    #     return True


    def action_done(self):
        if "cancelled" in self.mapped("appointment_status"):
            raise UserError("You have cancelled this appointment.")
        return self.write({"appointment_status":"done"})







    can_show_action_buttons = fields.Boolean(compute="_compute_button_visibility", store=False)

    @api.depends('appointment_status')
    def _compute_button_visibility(self):
        for record in self:
            record.can_show_action_buttons = record.appointment_status not in ['confirmed', 'cancelled']

    def cancelled(self):
        for record in self:
            record.appointment_status = 'cancelled'

    def confirmed(self):
        if "cancelled" in self.mapped("appointment_status"):
            raise UserError("You have cancelled this appointment.")
        return self.write({"appointment_status":"confirmed"})




    name = fields.Char(string="Reference Number", default=lambda self: _('New'), readonly=True, copy=False,
                                   help="Reference Number of the book")


    @api.model
    def create(self, vals):

        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
        return super(HospitalAppointment, self).create(vals)
