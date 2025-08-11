from odoo import models, fields


class HospitalMedicine(models.Model):
    _name = "hospital.medicine"
    _description = "Medicine"

    name = fields.Selection([
        ('aspirin', 'Aspirin'),('ibuprofen', 'Ibuprofen'),('amoxicillin', 'Amoxicillin'),('cetirizine', 'Cetirizine')
    ], string="Medicine")
    dosage = fields.Text(string="Dosage Instructions")
    duration = fields.Char(string="Duration[In days]")
    prescription_id = fields.Many2one('hospital.prescription', string="Prescription")




