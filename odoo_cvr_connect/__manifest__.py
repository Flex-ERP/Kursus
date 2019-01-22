# -*- coding: utf-8 -*-
{
    'name': "Odoo and CVR Connection API",
    'version': '1.1.6',
    'category': 'Sales',
    'license': 'Other proprietary',
    'summary': """This module provide feature to connect to CVR and fetch CVR number and other details.""",
    'description':  """
Odoo and CVR Connection API                    
                    """,
    'author': "FlexERP",
    'website': "http://www.flexerp.dk/",
    'depends':  [
        'sale',
                ],
    'data': [
                'wizard/cvr_connect_wizard_view.xml',
#                'views/cvr_connection.xml',
                'views/res_partner_views.xml',
            ],
   'installable' : True,
   'application' : False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
