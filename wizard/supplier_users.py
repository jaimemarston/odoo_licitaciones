from odoo import fields, models, api, _, tools
from odoo.exceptions import ValidationError

import logging
import re

class tendersSupplierUsers(models.TransientModel):
    _name = 'tenders.supplier.users'
    _description = 'mdoelo para crear de forma manual los usuarios de proveedores'
    
    login = fields.Char('login')

    password = fields.Char('password')

    supplier_id = fields.Many2one('licitaciones.proveedor', string='supplier')

    email = fields.Char('email')

    
    @api.onchange('email')
    def _onchenge_validated_email_partner(self):
        if self.email:
            email_normalized = tools.email_normalize(self.email)
            if not email_normalized:
                raise ValidationError('La dirección de correo no cumple con el formato estándar "ejemplo@ejemplo.com"')

                    
    def create_supplier_user(self):
        lang = self.env['res.lang'].sudo().search([('active', '=', True), ('code', '=', 'es_PE')], limit=1)
        user = self.env['res.users'].sudo().create({
            'name': self.supplier_id.name,
            'login': self.login,
            'password': self.password,
            'lang': lang.code if lang else 'es_US',
            'groups_id': [(6, 0, [self.env.ref('base.group_user').id])]
        })
        user.partner_id.vat = self.supplier_id.ruc
        user.partner_id.email = self.email