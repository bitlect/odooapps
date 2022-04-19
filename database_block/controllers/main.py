# -*- coding: utf-8 -*-

import json
import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class Main(http.Controller):
    
    @http.route('/get_dbconfig', type='json', website=True, auth="public", csrf=False)
    def get_dbconfig(self):        
        return json.dumps({
            'dbuuid': request.env['ir.config_parameter'].sudo().get_param('database.uuid'),
            'license_server': request.env['ir.config_parameter'].sudo().get_param('license.url'),
        })

    @http.route('/update_db_expiry', type='json',  methods=['POST'],  website=True, auth="public", csrf=False)
    def update_expiry_date(self, **kw):        
        db_expiry = request.env['ir.config_parameter'].sudo().search([('key','=','database_expiration_date')],limit=1)
        db_expiry and db_expiry.write({'value': kw.get('expiry_date')})   
        return json.dumps({
            'status': True
        })



        