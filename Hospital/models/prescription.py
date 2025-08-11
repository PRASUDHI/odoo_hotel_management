from odoo import models, fields, api, _


class HospitalPrescription(models.Model):
    _name = "hospital.prescription"
    _description = "Prescription"

    # name = fields.Char("Prescription ID", default="PR00")
    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True)
    pharmacy_name = fields.Char("Pharmacy Name")
    prescription_date = fields.Date("Prescription Date", default=fields.Date.today)
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor", required=True)

    medicine_details = fields.One2many('hospital.medicine', 'prescription_id', string="Medicine Details")

    reference_number = fields.Char(string="Reference Number", default=lambda self: _('New'), readonly=True, copy=False,
                                   help="Reference Number of the book")

    patient_lines=fields.Many2one('hospital.patient', string="Patients")





    @api.model
    def create(self, vals):

        if vals.get('reference_number', _('New')) == _('New'):
            vals['reference_number'] = self.env['ir.sequence'].next_by_code('hospital.prescription')
        return super(HospitalPrescription, self).create(vals)
