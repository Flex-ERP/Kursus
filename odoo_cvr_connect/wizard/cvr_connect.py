# -*- coding: utf-8 -*-
from odoo import models, api,fields, _
from odoo.exceptions import UserError
import urllib.request
import json
import contextlib
import requests
from odoo.exceptions import UserError

class CvrConnect(models.TransientModel):

    _name = "cvr.connect"
    
    company_name = fields.Char('Company Name',
        required = True
    )
	
    @api.multi
    def _cvrapi(self):
        try:
            context = dict(self._context or {})
            active_ids = context.get('active_ids', []) or []
            res_partner_id = self.env['res.partner'].browse(active_ids)
            company_name = self.company_name
            country = 'dk'
            x = 'http://cvrapi.dk/api?search=%s&country=%s' % (company_name,country)
            request = urllib.request.Request(
                url=x,
                headers={
                'User-Agent': 'Odoo'})
            with contextlib.closing(urllib.request.urlopen(request)) as response:
                if response:
                    str_response = response.read().decode('utf-8')
                    if str_response:
                        obj = json.loads(str_response)
                else:
                    raise UserError(('Record is not exist for connecting to CVR.'))
                    
                
            obj_owners_vals = ''
            if 'owners' in obj and obj:
                if obj['owners']:
                    for obj_owners_list in obj['owners']:
                        for keys in obj_owners_list.keys():
                            obj_owners_vals += str(obj_owners_list[keys])

                res_partner_comment = {
                    'companycode' :  obj['companycode'],
                    'version' :  obj['version'],
                    'employees' :  obj['employees'],
                    'owners' :  obj_owners_vals,
                }
                                
                comment_cvr = ""
            
                for key in res_partner_comment.keys():
                    comment_cvr += key +":"+str(res_partner_comment[key]) + "  "
                
                res_country_id = self.env['res.country'].search([('code','=','DK')])
                
                res_partner_id.update({
                    'vat' : obj['vat'],
                    'city' : obj['city'],
                    'name' : self.company_name,
                    'phone' : obj['phone'],
                    'zip' : obj['zipcode'],
                    'email' : obj['email'],
                    'street': obj['address'],
                    'ref': obj['companycode'],
                    'comment' : comment_cvr,
                    'country_id' : res_country_id,
                })
		
                message_cvr = ""
                del obj['productionunits']
                for key in obj.keys():
                    message_cvr += key + ":"+ str(obj[key]) + "<br/>"

                message = (message_cvr)
#                res_partner_vals_id = self.env['res.partner'].create(res_partner_vals)
                res_partner_id.message_post(body=message)
            else:
                raise UserError(('Record not found in CVR.'))
            
#            if res_partner_vals_id:                          
#                action = self.env.ref('base.action_partner_form').read()[0]
#                action['domain'] = [('id', '=', res_partner_vals_id.id)]
#                return action
                
        except urllib.error.HTTPError as error:
            raise UserError(('Record not found in CVR.'))
            
    @api.multi
    def cvrapi(self):
        return self._cvrapi()
