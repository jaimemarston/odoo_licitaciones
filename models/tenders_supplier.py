from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class TendersProveedor(models.Model):
    _name = 'licitaciones.proveedor'
    _description = 'Proveedor'

    name = fields.Char(string="Nombre del Proveedor", required=True)
    ruc = fields.Char(string="RUC", required=True)
    direccion = fields.Char(string="Dirección")
    localidad = fields.Char(string="Localidad")
    region = fields.Char(string="Región")
    pais = fields.Char(string="País")
    correo = fields.Char(string="Correo Electrónico")
    telefono = fields.Char(string="Teléfono")
    categoria = fields.Selection([
        ('bien', 'Bien'),
        ('servicio', 'Servicio'),
        ('obra', 'Obra'),
        ('consultoria', 'Consultoría')
    ], string="Categoría de Servicio", required=True)

    bidders_ids = fields.One2many('licitaciones.postores', 'supplier_id', string='bidders')

    def action_open_wizard_supplier_users(self):
        return {
            'name': 'Crear Usuario',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'tenders.supplier.users',
            'view_id': self.env.ref('tenders.tenders_supplier_users_view_form').id,
            'target': 'new',
            'context': {
                'default_supplier_id': self.id
            }
        }
    
    def accion_mostrar_registros_filtrados(self):
        user = self.env.user
        supplier_id = self.search([('ruc', '=', user.partner_id.vat)])
        bidder = self.env['licitaciones.postores'].search([('supplier_id', '=', supplier_id.id)])
        domain = [('postores_ids', 'in', bidder.ids)]
        competence = self.env['licitaciones.licitacion'].search(domain).mapped('postores_ids')
        return {
            'name': 'Registros Filtrados',
            'type': 'ir.actions.act_window',
            'res_model': 'licitaciones.proveedor',
            'view_id': self.env.ref('tenders.view_proveedor_tree').id,
            'view_mode': 'list',
            'domain': [('id', 'in', competence.ids)],
        }