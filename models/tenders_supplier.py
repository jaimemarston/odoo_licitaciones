from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re
import datetime
import logging

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
    title_filter = fields.Char('title_filter', store=False, readonly=False)
    bidders_filter_ids = fields.Many2many('licitaciones.postores', string='bidders_filter', compute="_compute_bidders_filter")
    date_filter = fields.Date('Date filter', store=False, readonly=False)
    end_date_filter = fields.Date('Date filter', store=False, readonly=False)
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

    @api.depends('bidders_ids', 'title_filter', 'date_filter', 'end_date_filter')
    def _compute_bidders_filter(self):
        domain = []
        if not self.bidders_ids:
            return  False
        if self.title_filter:
            domain.append(('titulo', 'ilike', f"%{self.title_filter}%"))
        if self.date_filter:
            # end_datetime = datetime.datetime(
            #         self.date_filter.year,
            #         self.date_filter.month,
            #         self.date_filter.day,
            #         23, 59, 59
            #     )
            domain.append(('fecha_publicacion', '>=', self.date_filter))
        if self.end_date_filter:
            domain.append(('fecha_publicacion', '<=', self.end_date_filter))
        
        # bidders = self.bidders_ids.filtered(lambda bidder: bidder.titulo == self.title_filter)
        if domain:
            domain.append(('id', 'in', self.bidders_ids.ids))
            bidders = self.bidders_ids.search(domain)
            self.bidders_filter_ids = [(6,0,bidders.ids)]
            return True
        if not domain and self.bidders_ids:
            self.bidders_filter_ids = self.bidders_ids.ids