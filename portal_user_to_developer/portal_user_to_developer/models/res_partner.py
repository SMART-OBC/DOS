from odoo import api, models, fields, _

class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.constrains('name')
    def sync_data_into_employee(self):
        user = self.env['res.users'].search([('partner_id', '=', self.id)])
        employee = self.env['employee.hub'].search([('portal_user_id', '=', user.id)])
        if employee:
            emp = employee.employee_id
            emp.write({
                'name' : self.name,
                'work_email': self.email,
                'work_phone': self.phone,
            })
