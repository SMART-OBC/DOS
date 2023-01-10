# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class EmployeeHub(models.Model):
    _name = 'employee.hub'
    _rec_name = 'employee_id'

    portal_user_id = fields.Many2one('res.users', 'Portal user', required=True, domain=[('partner_share', '=', True)])
    employee_id = fields.Many2one('hr.employee', 'employee', required=True)

    @api.onchange('portal_user_id', 'employee_id')
    def _onchange_portal_user_id(self):
        portal_user_id = self.portal_user_id
        if self.env['employee.hub'].search([('portal_user_id', '=', portal_user_id.id)]):
            raise ValidationError(_('Portal user is already linked to another employee'))
        employee_id = self.employee_id
        if self.env['employee.hub'].search([('employee_id', '=', employee_id.id)]):
            raise ValidationError(_('Employee is already linked to user'))

    @api.model
    def create(self, vals):
        types = self.env['hr.leave.type'].search([])
        time_off = self.env['time.off.type'].search([])
        if not time_off:
            for rec in types:
                self.env['time.off.type'].create({
                    'name': rec.name,
                    'time_off_id': rec.id
                })
        t_type = self.env['resource.calendar'].search([])
        for rec in t_type:
            self.env['working.time'].create({
                'name': rec.name,
                'working_id': rec.id
            })
        res = super(EmployeeHub, self).create(vals)
        return res