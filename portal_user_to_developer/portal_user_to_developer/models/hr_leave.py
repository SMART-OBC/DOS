# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    @api.constrains('state')
    def _onchange_state(self):
        for rec in self:
            portal_time_off = self.env['portal.time.off'].search([('hr_leave_id', '=', rec.id)])
            if portal_time_off:
                portal_time_off.state = rec.state
