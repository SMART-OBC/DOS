from odoo import api, models, fields, _
from datetime import datetime
import math

class HrEmployee(models.Model):
    _inherit = "hr.employee"

    schaal_id = fields.Many2one("schaal.configuration",string="Schaal")
    schaal_line = fields.Many2many('schaal.values.line')
    trede = fields.Many2one('schaal.values.line', 'Trede', domain="[('id', 'in', schaal_line)]")
    trede_button = fields.Boolean(default=False)
    bezoldiging = fields.Integer('Bezoldiging')
    five_percent_bezoldiging = fields.Boolean('5%Bezoldiging')
    formatiepunten = fields.Integer('Formatiepunten')
    vb_lesuren = fields.Integer('VB lesuren')
    type_personeel = fields.Selection([
        ('onderwijzend_personeel', 'Onderwijzend personeel'),
        ('onderwijs_ondersteunend_personeel', 'Onderwijs ondersteunend personeel'),
        ('niet_onderwijzend_personeel', 'Niet onderwijzend personeel'), ], string='Type personeel')
    wijziging_lesuren_vsbo = fields.Integer('Wijziging lesuren VSBO')
    wijziging_lesuren_havo_vwo = fields.Integer('Wijziging lesuren HAVO/VWO')
    total_degan_achterstand = fields.Integer('Totale dagen achterstand')
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True, default=lambda self: self.env.company.currency_id)
    total_achterstand_betaling = fields.Float('Totaal achterstand betaling', readonly=True, store=True, compute="_compute_total_achterstand_betaling")
    nieuwe_bezoldiging = fields.Integer('Nieuwe Bezoldiging', compute="_compute_nieuwe_bezoldiging", store=True)
    wijziging = fields.Boolean('wijziging', default=False)
    invaldagen_fo = fields.Integer('Invaldagen FO')
    total_invalskracht_fo_uitbetaling = fields.Float('Totaal invalskracht FO uitbetaling', readonly=True, store=True, compute="_compute_total_invalskracht_fo_uitbetaling")
    total_lesuren = fields.Integer('Totaal lesuren')
    totaal_invalskracht_vo_betaling = fields.Float('Totaal invalskracht VO betaling', readonly=True, store=True, compute="_compute_totaal_invalskracht_vo_betaling")
    nieuwe_opvoering_uren = fields.Integer('Nieuwe opvoering uren')
    nieuwe_lesuren_bezoldiging = fields.Float('Nieuwe lesuren bezoldiging', readonly=True, store=True, compute="_compute_nieuwe_lesuren_bezoldiging")
    verschil_lesuren = fields.Float('Verschil lesuren')
    toelage_van_overuren = fields.Float('Toelage van overuren', readonly=True, store=True, compute="_compute_toelage_van_overuren")
    vsbo1 = fields.Float(store=True)
    hvwo1 = fields.Float(store=True)
    datum_in_dienst = fields.Date('Datum in dienst')
    datum_uit_dienst = fields.Date('Datum uit dienst')


    @api.onchange('schaal_id')
    def _onchange_schaal_id(self):
        line = self.schaal_id.schaal_line_ids
        self.schaal_line = line
        self.trede = False
        self.five_percent_bezoldiging = False
        # return {'domain': {'trede': [('id', 'in', line.ids),
        #                                    ]}}

    @api.onchange('trede')
    def _onchange_trede(self):
        self.five_percent_bezoldiging = False
        self.bezoldiging = self.trede.bezoldiging
        self._compute_nieuwe_bezoldiging()
        self._compute_total_achterstand_betaling()
        self._compute_total_invalskracht_fo_uitbetaling()
        self._compute_totaal_invalskracht_vo_betaling()
        self._compute_nieuwe_lesuren_bezoldiging()
        self._compute_toelage_van_overuren()

    @api.depends('wijziging_lesuren_vsbo', 'wijziging_lesuren_havo_vwo')
    def _compute_nieuwe_bezoldiging(self):
        for rec in self:
            if rec.wijziging_lesuren_vsbo and rec.wijziging_lesuren_havo_vwo:
                vsbo1 = (rec.wijziging_lesuren_vsbo/32) * (rec.bezoldiging)
                rec.vsbo1 = vsbo1
                hvwo1 = (rec.wijziging_lesuren_havo_vwo / 27) * (rec.bezoldiging)
                rec.hvwo1 = hvwo1
                val = rec.vsbo1 + rec.hvwo1
                rec.write({
                    'nieuwe_bezoldiging' : math.ceil(val)
                })

    @api.depends('total_degan_achterstand')
    def _compute_total_achterstand_betaling(self):
        for rec in self:
            if rec.total_degan_achterstand:
                val = rec.total_degan_achterstand * 104
                rec.write({
                    'total_achterstand_betaling': math.ceil(val)
                })

    @api.depends('invaldagen_fo')
    def _compute_total_invalskracht_fo_uitbetaling(self):
        for rec in self:
            if rec.invaldagen_fo:
                val = (rec.invaldagen_fo/30) * (rec.bezoldiging)
                rec.write({
                    'total_invalskracht_fo_uitbetaling': math.ceil(val)
                })

    @api.depends('total_lesuren', 'department_id')
    def _compute_totaal_invalskracht_vo_betaling(self):
        for rec in self:
            if rec.total_lesuren:
                val = (rec.bezoldiging / 4.3) / 5
                vo1 = 0
                if self.department_id.name == 'HAVO':
                    vo1 = val/5.4
                if self.department_id.name == 'VSBO':
                    vo1 = val / 6.4
                result = vo1 * rec.total_lesuren
                rec.write({
                    'totaal_invalskracht_vo_betaling': math.ceil(result)
                })

    @api.depends('nieuwe_opvoering_uren')
    def _compute_nieuwe_lesuren_bezoldiging(self):
        for rec in self:
            if rec.nieuwe_opvoering_uren:
                val = (rec.nieuwe_opvoering_uren/rec.vb_lesuren) * rec.bezoldiging
                rec.write({
                    'nieuwe_lesuren_bezoldiging': math.ceil(val)
                })

    @api.depends('verschil_lesuren')
    def _compute_toelage_van_overuren(self):
        for rec in self:
            if rec.verschil_lesuren:
                val = (rec.verschil_lesuren/rec.vb_lesuren) * rec.bezoldiging
                rec.write({
                    'toelage_van_overuren': math.ceil(val)
                })

    @api.onchange('five_percent_bezoldiging')
    def _onchange_five_percent_bezoldiging(self):
        if self.five_percent_bezoldiging:
            benzo = self.bezoldiging
            cal = benzo/100 * 5
            value = benzo - cal
            self.bezoldiging = math.ceil(value)
            self._compute_nieuwe_bezoldiging()
            self._compute_total_achterstand_betaling()
            self._compute_total_invalskracht_fo_uitbetaling()
            self._compute_totaal_invalskracht_vo_betaling()
            self._compute_nieuwe_lesuren_bezoldiging()
            self._compute_toelage_van_overuren()
        else:
            self.bezoldiging = self.trede.bezoldiging
            self._compute_nieuwe_bezoldiging()
            self._compute_total_achterstand_betaling()
            self._compute_total_invalskracht_fo_uitbetaling()
            self._compute_totaal_invalskracht_vo_betaling()
            self._compute_nieuwe_lesuren_bezoldiging()
            self._compute_toelage_van_overuren()

    def plus_trede(self):
        if self.datum_in_dienst:
            current_year = str(fields.datetime.now().year)
            date_str = ''+current_year+'-02-01'
            date_object = datetime.strptime(date_str, '%Y-%m-%d').date()
            if self.datum_in_dienst < date_object and self.work_location_id.name not in ['Uitdienst', 'BVVD']:
                trede = self.trede.trede
                line = self.schaal_id.schaal_line_ids
                value = line.filtered(lambda x : x.trede == (trede + 1))
                if value:
                    self.write({
                        'trede': value.id,
                        'bezoldiging': value.bezoldiging
                    })
                    self.trede_button = True
                    self.bezoldiging = self.trede.bezoldiging
                    self._compute_nieuwe_bezoldiging()
                    self._compute_total_achterstand_betaling()
                    self._compute_total_invalskracht_fo_uitbetaling()
                    self._compute_totaal_invalskracht_vo_betaling()
                    self._compute_nieuwe_lesuren_bezoldiging()
                    self._compute_toelage_van_overuren()

    @api.onchange('department_id', 'type_personeel', 'job_id', 'vb_lesuren', 'resource_calendar_id')
    def _calculate_formatipentun(self):
        if self.department_id:
            if self.department_id.name in ['HAVO', 'VWO + VSBO']:
                self.wijziging = True
            else:
                self.wijziging = False
        hour = self.resource_calendar_id.attendance_ids
        value_time = []
        for rec in hour:
            value_time.append(rec.hour_to - rec.hour_from)
        working_hour = sum(value_time)
        if self.department_id and self.type_personeel and self.job_id and self.vb_lesuren and self.resource_calendar_id:
            if self.type_personeel == 'onderwijzend_personeel':
                if self.job_id.name not in ['Directeur 1', 'Directeur 2', 'Directeur 3','Directeur 1 a.i.', 'Directeur 2 a.i.', 'Directeur 3 a.i.']:
                    if self.department_id.name == 'Funderend onderwijs':
                        max_for = self.env['employee.formatiepunten'].search([])
                        ofo = max_for.ofo
                        formati = (working_hour/self.vb_lesuren) * ofo
                        self.formatiepunten = math.ceil(formati)
                    if self.department_id.name == 'Funderend Speciaal Onderwijs':
                        max_for = self.env['employee.formatiepunten'].search([])
                        ofso = max_for.ofso
                        formati = (working_hour / self.vb_lesuren) * ofso
                        self.formatiepunten = math.ceil(formati)
                    if self.department_id.name in ['VSBO', 'VSO']:
                        max_for = self.env['employee.formatiepunten'].search([])
                        ovsbo_vso = max_for.ovsbo_vso
                        formati = (working_hour / self.vb_lesuren) * ovsbo_vso
                        self.formatiepunten = math.ceil(formati)
                    if self.department_id.name == 'SBO':
                        max_for = self.env['employee.formatiepunten'].search([])
                        osbo = max_for.osbo
                        formati = (working_hour / self.vb_lesuren) * osbo
                        self.formatiepunten = math.ceil(formati)
                    if self.department_id.name in ['HAVO', 'VWO', 'HBO']:
                        max_for = self.env['employee.formatiepunten'].search([])
                        ohvbo = max_for.ohvbo
                        formati = (working_hour / self.vb_lesuren) * ohvbo
                        self.formatiepunten = math.ceil(formati)
                if self.job_id.name in ['Directeur 1', 'Directeur 2', 'Directeur 3','Directeur 1 a.i.', 'Directeur 2 a.i.', 'Directeur 3 a.i.']:
                    if self.department_id.name == 'Funderend onderwijs':
                        max_for = self.env['employee.formatiepunten'].search([])
                        ofodir = max_for.ofodir
                        formati = (working_hour/self.vb_lesuren) * ofodir
                        self.formatiepunten = math.ceil(formati)
                    if self.department_id.name == 'Funderend Speciaal Onderwijs':
                        max_for = self.env['employee.formatiepunten'].search([])
                        ofsodir = max_for.ofso
                        formati = (working_hour / self.vb_lesuren) * ofsodir
                        self.formatiepunten = math.ceil(formati)
                    if self.department_id.name in ['VSBO', 'VSO']:
                        max_for = self.env['employee.formatiepunten'].search([])
                        ovsbo_vsodir = max_for.ovsbo_vsodir
                        formati = (working_hour / self.vb_lesuren) * ovsbo_vsodir
                        self.formatiepunten = math.ceil(formati)
                    if self.department_id.name == 'SBO':
                        max_for = self.env['employee.formatiepunten'].search([])
                        osbodir = max_for.osbodir
                        formati = (working_hour / self.vb_lesuren) * osbodir
                        self.formatiepunten = math.ceil(formati)
                    if self.department_id.name in ['HAVO', 'VWO', 'HBO']:
                        max_for = self.env['employee.formatiepunten'].search([])
                        ohvbodir = max_for.ohvbodir
                        formati = (working_hour / self.vb_lesuren) * ohvbodir
                        self.formatiepunten = math.ceil(formati)

        if self.type_personeel and self.vb_lesuren and self.resource_calendar_id:
            if self.type_personeel in ['niet_onderwijzend_personeel', 'onderwijs_ondersteunend_personeel']:
                if self.department_id.name == 'Funderend Speciaal Onderwijs':
                    max_for = self.env['employee.formatiepunten'].search([])
                    nofso = max_for.nofso
                    formati = (working_hour / self.vb_lesuren) * nofso
                    self.formatiepunten = math.ceil(formati)
                if self.department_id.name in ['FO', 'AGO']:
                    max_for = self.env['employee.formatiepunten'].search([])
                    nofo_ago = max_for.nofo_ago
                    formati = (working_hour / self.vb_lesuren) * nofo_ago
                    self.formatiepunten = math.ceil(formati)
                if self.department_id.name == 'VSBO':
                    max_for = self.env['employee.formatiepunten'].search([])
                    novsbo = max_for.novsbo
                    formati = (working_hour / self.vb_lesuren) * novsbo
                    self.formatiepunten = math.ceil(formati)
                if self.department_id.name in ['HAVO', 'VWO', 'SBO'] and self.job_id.name == 'TOA':
                    max_for = self.env['employee.formatiepunten'].search([])
                    nohvbotoa = max_for.nohvbotoa
                    formati = (working_hour / self.vb_lesuren) * nohvbotoa
                    self.formatiepunten = math.ceil(formati)
                if self.department_id.name in ['HAVO', 'VWO', 'SBO'] and self.job_id.name == 'Studieassistent':
                    max_for = self.env['employee.formatiepunten'].search([])
                    nohvbosa = max_for.nohvbosa
                    formati = (working_hour / self.vb_lesuren) * nohvbosa
                    self.formatiepunten = math.ceil(formati)
                if self.job_id.name == 'Schoolverzorger':
                    max_for = self.env['employee.formatiepunten'].search([])
                    nosvz = max_for.nosvz
                    formati = (working_hour / self.vb_lesuren) * nosvz
                    self.formatiepunten = math.ceil(formati)
                if self.job_id.name == 'Schooladministratie':
                    max_for = self.env['employee.formatiepunten'].search([])
                    nosa = max_for.nosvz
                    formati = (working_hour / self.vb_lesuren) * nosa
                    self.formatiepunten = math.ceil(formati)
                if self.job_id.name == 'Schoolmaatschappelijk werker':
                    max_for = self.env['employee.formatiepunten'].search([])
                    nosmw = max_for.nosmw
                    formati = (working_hour / self.vb_lesuren) * nosmw
                    self.formatiepunten = math.ceil(formati)
                if self.job_id.name == 'Logopedist':
                    max_for = self.env['employee.formatiepunten'].search([])
                    nolopd = max_for.nolopd
                    formati = (working_hour / self.vb_lesuren) * nolopd
                    self.formatiepunten = math.ceil(formati)
