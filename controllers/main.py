import requests
from odoo import http
from odoo.http import request, Response
import json
import logging  

_logger = logging.getLogger(__name__)

class RecaptchaKeys(http.Controller):
    @http.route('/get_site_key', type='http', auth='public')
    def get_site_key(self):
        site_key = request.env['ir.config_parameter'].sudo().get_param('darb_login_signup_recaptcha.site_key')
        return request.make_response(json.dumps({'site_key': site_key}), [('Content-Type', 'application/json')])


from odoo.addons.web.controllers.main import Home

class RecaptchaValidationControllerLogin(Home):

    @http.route('/web/login', type='http', auth="none")
    def web_login_captcha(self, redirect=None, **kw):
        if request.httprequest.method == 'POST':
            client_key = kw.get('g-recaptcha-response')
            if not client_key:
                return "error : Something is wrong."
            
            
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

        response = super(RecaptchaValidationControllerLogin, self).web_login(**kw)
    
        return response
    

# from odoo.addons.auth_signup.controllers.main import AuthSignupHome

# class RecaptchaValidationControllerSignup(AuthSignupHome):

#     @http.route('/web/signup', type='http', auth="none")
#     def web_signup(self, redirect=None, **kw):
#         if request.httprequest.method == 'POST':
#             client_key = kw.get('g-recaptcha-response')
#             if not client_key:
#                 return "error : Something is wrong."

            
#             secret_key = request.env['ir.config_parameter'].sudo().get_param('darb_login_signup_recaptcha.secret_key')
            
#             if not secret_key:
#                 return "error: 'Secret key not configured.'"

#             captcha_data = {
#                 'secret': secret_key,
#                 'response': client_key
#             }
#             r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=captcha_data)
#             captcha_response = json.loads(r.text)

#             print(r)
#             print("client key :", client_key)
#             print("captcha response :", captcha_response)


#             # If reCAPTCHA is valid, proceed with the signup process
#         response = super(RecaptchaValidationControllerSignup, self).web_auth_signup(**kw)
#         return response




from odoo.addons.auth_signup.controllers.main import AuthSignupHome

class RecaptchaValidationControllerSignup(AuthSignupHome):

    @http.route('/web/signup', type='http', auth="public", methods=['POST'], csrf=False)
    def verify_captcha(self, token):
    
        secret_key = request.env['ir.config_parameter'].sudo().get_param('darb_login_signup_recaptcha.secret_key')

        url = "https://www.google.com/recaptcha/api/siteverify"
        data = {
            'secret': secret_key,
            'response': token,
        }

        response = requests.post(url, data=data)

        result = response.json()
        return result.get('success', False) 
    
    def web_signup_captcha(self, **kw):
        client_key = kw.get('g-recaptcha-response')

        if not self.verify_captcha(client_key):
            return "CAPTCHA verification failed. Please try again."
            
        
        response = super(RecaptchaValidationControllerSignup, self).web_auth_signup(**kw)
        return response
    

            


    
    

    
