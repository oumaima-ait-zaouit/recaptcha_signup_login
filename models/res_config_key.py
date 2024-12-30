from odoo import fields, models, api, _

class RecaptchaSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    secret_key = fields.Char(string=_("Clé secrète "))
    site_key = fields.Char(string=_("Clé de site"))



    def set_values(self):
        super(RecaptchaSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('recaptcha.secret_key', self.secret_key)
        self.env['ir.config_parameter'].sudo().set_param('recaptcha.site_key', self.site_key)


    @api.model
    def get_values(self):
        res = super(RecaptchaSettings, self).get_values()
        res.update(
            secret_key=self.env['ir.config_parameter'].sudo().get_param('recaptcha.secret_key', default=''),
            site_key=self.env['ir.config_parameter'].sudo().get_param('recaptcha.site_key', default='')
        )

        return res