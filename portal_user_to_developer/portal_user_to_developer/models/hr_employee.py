from odoo import api, models, fields, _
from datetime import datetime

class HrEmployeeBase(models.AbstractModel):
    _inherit = "hr.employee.base"

    def _inverse_work_contact_details(self):
        for employee in self:
            if not employee.work_contact_id:
                employee.work_contact_id = self.env['res.partner'].sudo().create({
                    'email': employee.work_email,
                    'mobile': employee.mobile_phone,
                    'name': employee.name,
                    'image_1920': employee.image_1920,
                    'company_id': employee.company_id.id
                })
                print(employee.work_contact_id.user_id)
                a = employee.work_contact_id
            else:
                employee.work_contact_id.sudo().write({
                    'email': employee.work_email,
                    'mobile': employee.mobile_phone,
                })