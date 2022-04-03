# -*- coding: utf-8 -*-

import json
import logging

from odoo import http, fields
from odoo.exceptions import ValidationError
from odoo.http import request, Response

from odoo.addons.license_manager.utils.key_generator import Key

_logger = logging.getLogger(__name__)


class License(http.Controller):
    

    @http.route('/validate_license', type='http',  methods=['POST'],  website=True, auth="public", csrf=False)
    def validate_license(self, **post):

        sub_code = post.get('sub_code')
        if not sub_code:
            return json.dumps({
                'valid': False, 
                "error": "bad_request",
                "message": "Required field 'sub_code' is missing"
            })


        dbuuid = request.httprequest.headers.get("dbuuid")
        if not dbuuid:
            return json.dumps({
                'valid': False, 
                "error": "bad_request",
                "message": "Missing header dbuuid"
            })

        license = (
            request.env["lm.license"]
            .sudo()
            .search([("dbuuid", "=", dbuuid)], order="id DESC", limit=1)
        )
        if not license:
                return json.dumps({
                    'valid': False, 
                    "error": "not_found",
                    "message": "License with DBUID not found"
                })

        if license.state == 'expired' or license.date_to < fields.Datetime.now():
                return json.dumps({
                    'valid': False, 
                    "error": "expired",
                    "message": "License has expired"
                })

        if license.state == 'deactivate':
                return json.dumps({
                    'valid': False, 
                    "error": "deactivated",
                    "message": "License is deactivated"
                })


        if sub_code != license.license_key:
            return json.dumps({
                'valid': False, 
                "error": "bad_request",
                "message": "Invalid subscription code"
            })

            #validate subscription code
        key = Key(sub_code)
        if not key.verify():
            return json.dumps({
                'valid': False, 
                "error": "invalid",
                'message':'Invalid subscription code', 
            })
            
        
        return json.dumps({
            'valid': True, 
            'message':'Valid', 
            'date_from': fields.Datetime.to_string(license.date_from), 
            'date_to': fields.Datetime.to_string(license.date_to)
        })