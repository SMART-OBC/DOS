# -*- coding: utf-8 -*-

from odoo import fields, models, api, _



class Attachment(models.Model):

    _inherit = 'ir.attachment'

    attach_rel = fields.Many2many('portal.time.off', 'attachment', 'attachment_id3', 'document_id', string="Attachment", invisible=1 )

