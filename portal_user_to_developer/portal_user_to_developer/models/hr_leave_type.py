# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class HrLeaveType(models.Model):
    _inherit = 'hr.leave.type'

    @api.model
    def create(self, vals):
        res = super(HrLeaveType, self).create(vals)
        self.env['time.off.type'].create({
            'name': vals.get('name'),
            'time_off_id': res.id
        })
        return res

