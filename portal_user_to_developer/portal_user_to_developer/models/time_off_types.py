# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class TimeOffType(models.Model):
    _name = 'time.off.type'

    name = fields.Char('Name', required=True)
    time_off_id = fields.Integer('Time off id', required=True, readonly=True)

    @api.model
    def get_time_of_types(self):
        t_type = self.env['time.off.type'].search([])
        types = []
        for rec in t_type:
            types.append({
                'name': rec.name,
                'id': rec.id
            })
        employee = self.env['employee.hub'].search([('portal_user_id', '=', self.env.uid)])
        portal_time_off = self.env['portal.time.off'].search([('employee_id', '=', employee.employee_id.id)])
        my_time_off = {}
        draft = len(portal_time_off.filtered(lambda r: r.state == 'draft'))
        if draft != 0:
            my_time_off.update({
                'To Submit': draft
            })
        confirm = len(portal_time_off.filtered(lambda r: r.state == 'confirm'))
        if confirm != 0:
            my_time_off.update({
                'To approve': confirm
            })

        refuse = len(portal_time_off.filtered(lambda r: r.state == 'refuse'))
        if refuse != 0:
            my_time_off.update({
                'Refused': refuse
            })

        validate1 = len(portal_time_off.filtered(lambda r: r.state == 'validate1'))
        if validate1 != 0:
            my_time_off.update({
                'Second Approval': validate1
            })
        validate = len(portal_time_off.filtered(lambda r: r.state == 'validate'))
        if validate != 0:
            my_time_off.update({
                'Approved': validate
            })
        return types, my_time_off



