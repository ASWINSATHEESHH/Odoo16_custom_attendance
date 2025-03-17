# -*- coding: utf-8 -*-
{
    'name': "attendance_dgz",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'hr_attendance'],
    'data': [
        'security/ir.model.access.csv',
        'data/cron.xml',
        'wizard/wizard.xml',
        'views/attendance.xml',
        # 'views/hr_attendance_template.xml',
    ],
    "assets": {
        "web.assets_backend": [
            'attendance_dgz/static/src/js/my_attendance_extension.js',
        ],
    },

}
