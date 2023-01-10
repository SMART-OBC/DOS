# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "Employee Extended",
    'summary': """Employee Dos development""",
    'description': """Employee Dos development""",
    'version': '16.0.0.0.0',
    'depends': ['hr'],
    'data': ['security/ir.model.access.csv',
             'data/schaal_table_data.xml',
             'views/schaal_configuration.xml',
             'views/hr_employee.xml',
             'views/formatiepunten.xml',
             ],
    # 'assets': {
    #     'web.assets_backend': [
    #         'document_extended/static/src/js/documents_inspector.js',
    #         'document_extended/static/src/scss/document_view.scss',
    #         'document_extended/static/src/xml/documentsInspector_extend.xml'
    #     ]
    #     },
    'license': 'LGPL-3',
}
