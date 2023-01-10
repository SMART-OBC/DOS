from odoo import api, models, fields, _
from datetime import datetime
from odoo.exceptions import ValidationError, AccessError


class EmployeeFormatiepunten(models.Model):
    _name = "employee.formatiepunten"

    name = fields.Char('Name')
    ofo = fields.Integer('OFO', help="Onderwijzend personeel, Funderend onderwijs")
    ofso = fields.Integer('OFSO', help="Onderwijzend personeel, Funderend Speciaal Onderwijs")
    ovsbo_vso = fields.Integer('OVSBO/VSO', help="Onderwijzend personeel, VSBO/ VSO")
    osbo = fields.Integer('OSBO', help="Onderwijzend personeel, SBO")
    ohvbo = fields.Integer('OHVBO', help="Onderwijzend personeel, HAVO/ VWO/ HBO")
    ofodir = fields.Integer('OFOdir', help="Directeurs, Onderwijzend personeel, Funderend onderwijs")
    ofsodir = fields.Integer('OFSODir', help="Directeurs, Onderwijzend personeel, Funderend Speciaal Onderwijs")
    ovsbo_vsodir = fields.Integer('OVSBO/VSODir', help="Directeurs,Onderwijzend personeel, VSBO/ VSO")
    osbodir = fields.Integer('OSBODir', help="Directeurs, Onderwijzend personeel, SBO")
    ohvbodir = fields.Integer('OHVBODir', help="Directeurs, Onderwijzend personeel, HAVO/ VWO/ HBO")
    nofso = fields.Integer('NOFSO', help="Niet onderwijzend personeel/ Onderwijs ondersteunend personeel, Funderend Speciaal Onderwijs ")
    nofo_ago = fields.Integer('NOFO/AGO', help="Niet onderwijzend personeel/ Onderwijs ondersteunend personeel, FO/ AGO ")
    novsbo = fields.Integer('NOVSBO', help="Niet onderwijzend personeel/ Onderwijs ondersteunend personeel, VSBO")
    nohvbotoa = fields.Integer('NOHVBOTOA', help="TOA, Niet onderwijzend personeel/ Onderwijs ondersteunend personeel, HAVO/ VWO/ SBO")
    nohvbosa = fields.Integer('NOHVBOSA', help="Studieassistent, Niet onderwijzend personeel/ Onderwijs ondersteunend personeel, HAVO/ VWO/ SBO")
    nosvz = fields.Integer('NOSVZ', help="Schoolverzorger, Niet onderwijzend personeel/ Onderwijs ondersteunend personeel")
    nosa = fields.Integer('NOSA', help="Schooladministratie, Niet onderwijzend personeel/ Onderwijs ondersteunend personeel")
    nosmw = fields.Integer('NOSMW', help="Schoolmaatschappelijk werker, Niet onderwijzend personeel/ Onderwijs ondersteunend personeel")
    nolopd = fields.Integer('NOLOPD', help='Logopedist, Niet onderwijzend personeel/ Onderwijs ondersteunend personeel')

    @api.model
    def create(self, vals):
        form = self.env['employee.formatiepunten'].search([])
        if len(form) >= 1:
            raise ValidationError(_("Cannot create multiple formatiepunten values"))
        res = super(EmployeeFormatiepunten, self).create(vals)
        return res

    def action_plus_trede(self):
        print('jjjjj')
        employe = self.env['hr.employee'].search([])
        print('employe', employe)
        for rec in employe:
            if rec.datum_in_dienst and rec.trede_button != True:
                print('rec', rec.name)
                current_year = str(fields.datetime.now().year)
                date_str = ''+current_year+'-02-01'
                date_object = datetime.strptime(date_str, '%Y-%m-%d').date()
                if rec.datum_in_dienst < date_object and rec.work_location_id.name not in ['Uitdienst', 'BVVD']:
                    trede = rec.trede.trede
                    line = rec.schaal_id.schaal_line_ids
                    value = line.filtered(lambda x : x.trede == (trede + 1))
                    if value:
                        rec.write({
                            'trede': value.id,
                            'bezoldiging': value.bezoldiging
                        })
                        rec.trede_button = True
                        rec.bezoldiging = rec.trede.bezoldiging
                        rec._compute_nieuwe_bezoldiging()
                        rec._compute_total_achterstand_betaling()
                        rec._compute_total_invalskracht_fo_uitbetaling()
                        rec._compute_totaal_invalskracht_vo_betaling()
                        rec._compute_nieuwe_lesuren_bezoldiging()
                        rec._compute_toelage_van_overuren()
