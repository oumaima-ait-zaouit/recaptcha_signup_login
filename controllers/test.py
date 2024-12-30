from odoo import http
from odoo.http import request

class MyCustomController(http.Controller):
    @http.route('/my_custom_route', auth='public', website=True)
    def my_custom_route(self, **kwargs):
        return "Hello, this is my custom controller!"
