from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class TendersDocumento(models.Model):
    _name = 'licitaciones.documento'
    _description = 'Documento'

    id_documento = fields.Char(string="ID Documento", required=True)
    titulo = fields.Char(string="Título")
    url = fields.Char(string="URL")
    tipo_documento = fields.Char(string="Tipo de Documento")
    formato = fields.Char(string="Formato")
    fecha_publicacion = fields.Datetime(string="Fecha de Publicación")
    licitacion_id = fields.Many2one('licitaciones.licitacion', string="Licitación", ondelete="cascade")