from odoo import fields, models
import logging
class tendersSupplierUsers(models.TransientModel):
    _name = 'tenders.supplier.users'
    _description = 'mdoelo para crear de forma manual los usuarios de proveedores'
    
    login = fields.Char('login')

    password = fields.Char('password')

    supplier_id = fields.Many2one('licitaciones.proveedor', string='supplier')

    def create_supplier_user(self):
        lang = self.env['res.lang'].sudo().search([('active', '=', True), ('code', '=', 'es_PE')], limit=1)
        self.env['res.users'].sudo().create({
            'name': self.supplier_id.name,
            'login': self.login,
            'password': self.password,
            'lang': lang.code if lang else 'es_US',
            'groups_id': [(6, 0, [self.env.ref('base.group_user').id])]
        })