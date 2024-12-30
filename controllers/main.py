import requests
from odoo import http
from odoo.http import request, Response
import json
import logging  


from odoo.addons.web.controllers.main import Home

class RecaptchaValidationController(Home):
    @http.route('/web/login', type='http', auth="none")
    def web_login(self, redirect=None, **kw):
        response = super(RecaptchaValidationController, self).web_login(**kw)
        print("test")
        if request.httprequest.method == 'POST':
            client_key = kw.get('g-recaptcha-response')
            if not client_key:
                return "error': 'reCAPTCHA verification failed. Please try again."
            
            secret_key = '6Lci9qgqAAAAANldIqzXWBavK1B9hn8ja7NTpnEo'

            captcha_data = {
                'secret': secret_key,
                'response': client_key
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=captcha_data)
            
            captcha_response = json.loads(r.text)

            print(r)
            print("client_key :", client_key)
    
        return response
    







    # @http.route('/cap', type='http', auth='public', website=True)
    # def google_recaptcha(self, redirect=None, **kw):
    #     if request.httprequest.method == 'POST':
    #         client_key = kw.get('g-recaptcha-response')
    #         if not client_key:
    #             return "error': 'reCAPTCHA verification failed. Please try again."
            
    #         secret_key = '6Lci9qgqAAAAANldIqzXWBavK1B9hn8ja7NTpnEo'

    #         captcha_data = {
    #             'secret': secret_key,
    #             'response': client_key
    #         }
    #         r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=captcha_data)
    #         response = json.loads(r.text)

    #         print(response)
    #         verify = response.get('success')
            
    #         if verify:
    #             # Logic for successful reCAPTCHA verification
    #             return request.render('module_name.your_form_template', {
    #                 'key_1': 'Test',
    #                 'key_2': kw,
    #             })
    #         else:
    #             # Logic for failed reCAPTCHA verification
    #             return "error': 'reCAPTCHA verification failed. Please try again."
            



        # recaptcha_response = kw.get('g-recaptcha-response')
        # if not recaptcha_response:           
        #     return Response(
        #         json.dumps({'status': 'error', 'message': 'Missing the token'}), 
        #         content_type='application/json', 
        #         status=400
        #     )
        # else:
        #     print(f"reCAPTCHA response received: {recaptcha_response}")

        #     _logger = logging.getLogger(__name__)
        #     _logger.info("reCAPTCHA response received: %s", recaptcha_response)


        # secret_key = '6Lci9qgqAAAAANldIqzXWBavK1B9hn8ja7NTpnEo'  
        # recaptcha_url = 'https://www.google.com/recaptcha/api/siteverify'

        # data = {
        #     'secret': secret_key,
        #     'response': recaptcha_response
        # }

        # response = requests.post(recaptcha_url, data=data)
        # result = response.json()

        # if result.get('success'):
        #     return Response(json.dumps({'status': 'success', 'message': 'reCAPTCHA validation successful'}),
        #                     content_type='application/json', status=200)
        # else:
        #     return Response(json.dumps({'status': 'error', 'message': 'reCAPTCHA validation failed'}),
        #                     content_type='application/json', status=400)

    
