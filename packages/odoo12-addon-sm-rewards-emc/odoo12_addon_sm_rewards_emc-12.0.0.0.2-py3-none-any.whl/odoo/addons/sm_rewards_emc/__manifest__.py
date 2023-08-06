# -*- coding: utf-8 -*-
{
  'name': "sm_rewards_emc",

  'summary': """""",

  'description': """""",

  'author': "Som Mobilitat",
  'website': "http://www.sommobilitat.coop",

  # Categories can be used to filter modules in modules listing
  # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
  # for the full list
  'category': 'Uncategorized',
  'version': '12.0.0.0.2',

  # any module necessary for this one to work correctly
  'depends': ['base','sm_rewards','easy_my_coop'],

  # always loaded
  'data': [
    'views/views_reward.xml',
    'views/views_subscription_request.xml'
  ],
  # only loaded in demonstration mode
  'demo': [],
}
