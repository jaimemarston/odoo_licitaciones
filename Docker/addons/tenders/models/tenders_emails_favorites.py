from odoo import models, fields, api, tools, _
from odoo.exceptions import ValidationError
import re


class TendersEmailsFavorites(models.Model):
    _name = 'licitaciones.emails.favorites'
    _description = 'Favoritos'

    name = fields.Char('name')
    email = fields.Char('email')


    @api.onchange('email')
    def _onchange_email(self):
        if self.email:
            email_normalized = tools.email_normalize(self.email)
            if not email_normalized:
                raise ValidationError(_("La dirección de correo no cumple con el formato estándar 'ejemplo@ejemplo.com' "))
            
