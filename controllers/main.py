import requests
from odoo import http
from odoo.http import request, Response
import json
import logging  


class RecaptchaKeys(http.Controller):
    @http.route('/get_site_key', type='http', auth='public')
    def get_site_key(self):
        site_key = request.env['ir.config_parameter'].sudo().get_param('darb_login_signup_recaptcha.site_key')
        return request.make_response(json.dumps({'site_key': site_key}), [('Content-Type', 'application/json')])



from odoo.addons.web.controllers.main import Home

class RecaptchaValidationControllerLogin(Home):

    @http.route('/web/login', type='http', auth="none")
    def web_login(self, redirect=None, **kw):
        response = super(RecaptchaValidationControllerLogin, self).web_login(**kw)

        if request.httprequest.method == 'POST':
            client_key = kw.get('g-recaptcha-response')
            if not client_key:
                return "error : no client key."
            
            
            secret_key = request.env['ir.config_parameter'].sudo().get_param('darb_login_signup_recaptcha.secret_key')
            if not secret_key:
                return "error: 'Secret key not configured.'"

            captcha_data = {
                'secret': secret_key,
                'response': client_key
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=captcha_data)

            captcha_response = r.json()

            print(r)
            print("client key :", client_key)
            print("captcha response :", captcha_response)
    
        return response
    
    
