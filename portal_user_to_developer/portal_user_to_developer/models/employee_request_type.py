# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class TimeOffType(models.Model):
    _name = 'working.time'

    working_id = fields.Integer(string='Working Time', required=True, readonly=True)
    name = fields.Char('Name', required=True)
