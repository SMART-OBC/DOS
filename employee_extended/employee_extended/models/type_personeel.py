from odoo import api, models, fields, _
from datetime import datetime


class TypePersoneel(models.Model):
    _name = "type.personeel"

    name = fields.Char('Name')