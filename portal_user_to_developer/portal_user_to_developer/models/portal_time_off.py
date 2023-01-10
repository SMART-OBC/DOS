# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class EmployeeHub(models.Model):
    _name = 'portal.time.off'
    _rec_name = 'time_off_type'

    time_off_type = fields.Many2one('time.off.type', 'Time off type', required=True)
    employee_id = fields.Many2one('hr.employee', 'Employee', required=True)
    user_id = fields.Many2one('res.users', 'Responsible User')
    name = fields.Char('Description')
    request_date_from = fields.Date(string='Start Date', required=True)
    request_date_to = fields.Date(string='End Date', required=True)
    number_of_days = fields.Integer('Days', copy=False, readonly=True)
    state = fields.Selection([
        ('draft', 'To Submit'),
        ('confirm', 'To approve'),
        ('refuse', 'Refused'), ('validate1', 'Second Approval'), ('validate', 'Approved'),
    ], string='Status', default='draft'
    )
    hr_leave_id = fields.Integer('Hr Leave id', copy=False)
    hr_bool = fields.Boolean(default=False, copy=False)
    attachment = fields.Many2many('ir.attachment', 'attach_rel', 'doc_id', 'attach_id3', string="Attachment", help='You can attach the copy of your document', copy=False)

    def action_confirm(self):
        print(self.attachment.ids)
        time_off = self.env['hr.leave'].create({
            'name': self.name,
            'user_id': self.user_id.id,
            'employee_id': self.employee_id.id,
            'holiday_status_id': self.time_off_type.time_off_id,
            'request_date_from': self.request_date_from,
            'request_date_to': self.request_date_to,
            'number_of_days': self.number_of_days,
            'supported_attachment_ids': [(6, 0, self.attachment.ids)],
            'date_from': self.request_date_from,
            'date_to': self.request_date_to
        })

        self.hr_bool = True
        self.hr_leave_id = time_off.id

    @api.onchange('request_date_to', 'request_date_from')
    def _onchange_date(self):
        if self.request_date_to and self.request_date_from:
            d1 = datetime.strptime(str(self.request_date_from), '%Y-%m-%d')
            d2 = datetime.strptime(str(self.request_date_to), '%Y-%m-%d')
            d3 = d2 - d1
            self.number_of_days = int(d3.days)

    @api.model
    def create(self, vals):
        res = super(EmployeeHub, self).create(vals)
        return res

    def time_off_cron(self):
        requests = self.env['portal.time.off'].search([('hr_leave_id', '=', False)])
        for rec in requests:
            rec.action_confirm()

