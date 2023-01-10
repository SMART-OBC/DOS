# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ResUserInherit(models.Model):
    _inherit = 'res.users'

    employee_responsible = fields.Boolean(
        'Employee responsible',
        domain="[('sel_groups_1_9_10', '=', '1')]",
        )

    @api.onchange('employee_responsible')
    def _onchange_employee_responsible(self):
        employee_responsible = self.env['res.users'].search([('employee_responsible', '=', True)])
        employee_ = self.env['res.users'].search([])
        if employee_responsible:
            raise ValidationError(_('Already a user have assigned employee responsible'))



