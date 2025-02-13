from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class TendersLicitacion(models.Model):
    _name = 'licitaciones.licitacion'
    _description = 'Licitación'

    id_licitacion = fields.Char(string="ID Licitación", required=True)
    comprador_id = fields.Many2one('licitaciones.buyer', string="Comprador")
    fecha_publicacion = fields.Datetime(string='Fecha y Hora de Publicación', required=True)
    nomenclatura = fields.Char(string='Nomenclatura')
    reiniciado_desde = fields.Char(string='Reiniciado Desde')
    objeto_contratacion = fields.Char(string='Objeto de Contratación', required=True)
    descripcion_objeto = fields.Text(string='Descripción de Objeto')
    codigo_snip = fields.Char(string='Código SNIP')
    codigo_unico_inversion = fields.Char(string='Código Único de Inversión')
    metodo_adquisicion = fields.Char(string='Metodo de Adquisición')
    categoria_adquisicion = fields.Char(string='Categoria de Adquisición')
    valor_referencial = fields.Float(string='Valor Referencial')
    moneda = fields.Selection([
        ('PEN', 'Soles'),
        ('USD', 'Dólares')
    ], string='Moneda', required=True)
    version_seace = fields.Char(string='Versión SEACE')
    acciones = fields.Text(string='Acciones')
    monto_total = fields.Float(string="Monto Total")
    documento_ids = fields.One2many('licitaciones.documento', 'licitacion_id', string="Documentos")
    postores_ids = fields.One2many('licitaciones.postores', 'licitacion_id', string="Postores")
    titulo = fields.Char(string="Título")
    categoria_principal = fields.Char(string="Categoría Principal")
    item_ids = fields.One2many('licitaciones.item', 'licitacion_id', string="Ítems")
    cronograma_ids = fields.One2many('licitaciones.cronograma', 'licitacion_id', string="Cronograma")

    @api.depends('fecha_inicio', 'fecha_fin')
    def _compute_duracion_dias(self):
        for record in self:
            if record.fecha_inicio and record.fecha_fin:
                delta = record.fecha_fin - record.fecha_inicio
                record.duracion_dias = delta.days
            else:
                record.duracion_dias = 0
