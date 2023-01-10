# -*- coding: utf-8 -*-
import logging
from odoo.exceptions import UserError

from odoo import api, fields, models, _

class PortalWizardInherit(models.TransientModel):
    _inherit = "portal.wizard.user"

    def action_grant_access(self):
        self.ensure_one()
        self._assert_user_email_uniqueness()
        partner = self.partner_id
        if self.is_portal or self.is_internal:
            raise UserError(_('The partner "%s" already has the portal access.', self.partner_id.name))

        group_portal = self.env.ref('base.group_portal')
        group_public = self.env.ref('base.group_public')

        self._update_partner_email()
        user_sudo = self.user_id.sudo()

        if not user_sudo:
            # create a user if necessary and make sure it is in the portal group
            company = self.partner_id.company_id or self.env.company
            user_sudo = self.sudo().with_company(company.id)._create_user()
        if not user_sudo.active or not self.is_portal:
            user_sudo.write({'active': True, 'groups_id': [(4, group_portal.id), (3, group_public.id)]})
            # prepare for the signup process
            user_sudo.partner_id.signup_prepare()
        employee = self.env['hr.employee'].search([('work_contact_id', '=', self.partner_id.id)])
        if employee and user_sudo:
            employee_hub = self.env['employee.hub'].create({
                'employee_id': employee.id,
                'portal_user_id': user_sudo.id
            })
        self.with_context(active_test=True)._send_email()
        return self.action_refresh_modal()