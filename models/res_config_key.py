from odoo import fields, models, api, _

class RecaptchaSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    secret_key = fields.Char(string=_("Clé secrète "), config_parameter='darb_login_signup_recaptcha.secret_key')
    site_key = fields.Char(string=_("Clé de site"), config_parameter='darb_login_signup_recaptcha.site_key')



    def set_values(self):
        super(RecaptchaSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('darb_login_signup_recaptcha.secret_key', self.secret_key)
        self.env['ir.config_parameter'].sudo().set_param('darb_login_signup_recaptcha.site_key', self.site_key)


    @api.model
    def get_values(self):
        res = super(RecaptchaSettings, self).get_values()
        res.update(
            secret_key=self.env['ir.config_parameter'].sudo().get_param('darb_login_signup_recaptcha.secret_key'),
            site_key=self.env['ir.config_parameter'].sudo().get_param('darb_login_signup_recaptcha.site_key')
        )

        return res