from odoo import models, fields,api


class Patient(models.Model):
    _name = "hospital.patient"
    _description = "Patient"

    name = fields.Char('Name', required=True)
    age = fields.Integer('Age')
    dob = fields.Date('Date Of Birth')
    gender = fields.Selection(
        string='Gender',
        selection=[('male', 'Male'), ('female', 'Female')]
    )
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    address = fields.Text(string='Address')
    blood_group = fields.Selection([
        ('a+', 'A+'), ('a-', 'A-'),
        ('b+', 'B+'), ('b-', 'B-'),
        ('ab+', 'AB+'), ('ab-', 'AB-'),
        ('o+', 'O+'), ('o-', 'O-')
    ], string='Blood Group')
    emergency_contact = fields.Char(string='Emergency Contact')
    medical_history = fields.Text(string='Medical History')
    active = fields.Boolean(string='Active', default=True)
    prescription_id=fields.One2many("hospital.prescription","patient_lines",string="Prescription Details")
    # prescription=fields.Many2one("hospital.prescription", string="Prescription")



#
# @api.depends('dob')
#
#
# def _compute_age(self):
#     for rec in self:
#         if rec.date_of_birth:
#             today = fields.Date.today()
#             rec.age = today.year - rec.date_of_birth.year - (
#                     (today.month, today.day) < (rec.date_of_birth.month, rec.date_of_birth.day)
#             )
#         else:
#             rec.age = 0
