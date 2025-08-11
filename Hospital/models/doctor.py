from odoo import models, fields
from odoo.exceptions import ValidationError


class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _description = "Doctor"

    name = fields.Char('Name', required=True)
    department = fields.Selection([
        ('cardiology', 'Cardiology'),('neurology', 'Neurology'),('orthopedics', 'Orthopedics'),('pediatrics', 'Pediatrics'),('dermatology', 'Dermatology'),('gynecology', 'Gynecology'),
        ('general_medicine', 'General Medicine'),
    ], string="Department")
    consulting_type = fields.Selection([
        ('in_person', 'In-person'),
        ('online', 'Online'),
        ('both', 'Both'),
    ], string="Consulting Type")

    consulting_fee = fields.Float("Consulting Fee", required=True)
    specialization = fields.Char("Specialization")
    experience_years = fields.Integer("Years of Experience")
    joining_date = fields.Date("Joining Date")
    phone = fields.Char("Phone")
    email = fields.Char("Email")
    qualification = fields.Selection([
        ('mbbs', 'MBBS'),
        ('md', 'MD'),
        ('ms', 'MS'),
    ], string="Qualification")

    bio = fields.Text("Biography")
    is_active = fields.Boolean("Active", default=True)
    # appointment_id = fields.Many2one("hospital.appointment", string="Appointment")
    patient_id = fields.Many2one('hospital.patient', string="Patient")
    appointment_lines = fields.One2many('hospital.appointment','doctor_lines',string="Appointment")


