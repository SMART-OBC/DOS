# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class EmployeeHub(models.Model):
    _name = 'employee.request'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', 'Employee', required=True)
    state = fields.Selection([
        ('draft', 'To Approve'),
        ('confirm', 'Approved'),
        ('reject', 'Rejected'),
    ], string='Status', default='draft'
    )
    employee_requests = fields.Selection(
        [('family_status', 'Burgelijke staat'),
         ('address', 'Adres'), ('children', 'Kinderen'), ('working_hours', 'Lesuren')], string='Request Type',
        required=True)
    description = fields.Char('Description')
    marital_status = fields.Selection([
         ('single', 'Single'), ('married', 'Married'), ('cohabitant', 'Legal Cohabitant'), ('widower', 'Widower'), 
                                       ('divorced', 'Divorced')], string='Marital Status',)
    spouse_complete_name = fields.Char('Spouse Complete Name')
    spouse_birthdate = fields.Date(string='Spouse Birthdate')
    no_of_children = fields.Integer('Number of Dependent Children')
    working_hours = fields.Many2one('working.time', string='Working Hours')
    attachment_ids = fields.Many2many('ir.attachment', relation='employee_request_ir_attachment_rel',string="Attachment", help='You can attach the copy of your document', copy=False)

    def action_confirm(self):
        print('jjjjjjjjjjjj')
        if self.employee_requests == 'family_status':
            if self.marital_status:
                self.employee_id.marital = self.marital_status
            if self.spouse_birthdate:
                self.employee_id.spouse_birthdate = self.spouse_birthdate
            if self.spouse_complete_name:
                self.employee_id.spouse_complete_name = self.spouse_complete_name
        if self.employee_requests == 'children':
            if self.no_of_children:
                self.employee_id.children = self.no_of_children
        if self.employee_requests == 'working_hours':
            if self.working_hours:
                self.employee_id.resource_calendar_id = self.working_hours.id
        self.state = 'confirm'


    def action_reject(self):
        print('jjjjjjjjjjjj')
        self.state = 'reject'

    @api.model
    def get_working_hour(self):
        t_type = self.env['working.time'].search([])
        types = []
        for rec in t_type:
            types.append({
                'name': rec.name,
                'id': rec.working_id
            })
        return types

