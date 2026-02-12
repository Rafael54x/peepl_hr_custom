# -*- coding: utf-8 -*-
{
    'name': 'Peepl HR - HR Recruitment',
    'version': '19.0.1.0.3',
    'category': 'HR/Projects',
    'summary': 'HR Recruitment policy for assessment services',
    'description': """
HR Recruitment System
==================================

This module extends Odoo's HR and project management to support HR Recruitment,
building on the existing participant management system.

    """,
    'author': 'Peepl',
    'website': 'https://peepl.com',
    'license': 'LGPL-3',
    'depends': ['base', 'hr_recruitment', 'hr_recruitment_reports'],
    'data': [
        'security/ir.model.access.csv',
        'data/recruitment_test_config_data.xml',
        'views/hr_applicant_views.xml',
        'views/recruitment_custom_field_views.xml',
        'views/recruitment_config_views.xml',
        'views/recruitment_dashboard_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'peepl_hr_custom/static/src/css/recruitment_dashboard.css',
            'peepl_hr_custom/static/src/css/list_view.css',
            'peepl_hr_custom/static/src/js/recruitment_dashboard.js',
            'peepl_hr_custom/static/src/xml/recruitment_dashboard.xml',
        ],
    },
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,

    'uninstall_hook': None,
    'external_dependencies': {
        'python': [],
    },
}