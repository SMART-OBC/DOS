from odoo import api, models, fields, _
from datetime import datetime

class SchaalCnfiguration(models.Model):
    _name = "schaal.configuration"

    name = fields.Char('Schaal Name')
    schaal_line_ids = fields.One2many('schaal.values.line', 'schaal_line_id', string='Schaal_lines')


class SchaalValues(models.Model):
    _name = "schaal.values.line"
    _rec_name = 'trede'

    schaal_line_id = fields.Many2one('schaal.configuration')
    trede = fields.Integer('Trede')
    bezoldiging = fields.Integer('Bezoldiging')



