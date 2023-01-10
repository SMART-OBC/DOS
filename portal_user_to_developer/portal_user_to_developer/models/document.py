from odoo import api, models, fields, _
from datetime import datetime

class DocumentDocumentNew(models.Model):
    _inherit = "documents.document"

    payslip_date = fields.Date("DateM/Y")
    employee_id = fields.Many2one('hr.employee', 'Employee')
    id_nr = fields.Integer('ID nr')


