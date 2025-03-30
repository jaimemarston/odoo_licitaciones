from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class TendersCronograma(models.Model):
    _name = 'licitaciones.cronograma'
    _description = 'Cronograma'

    name = fields.Char(string="ID Cronograma", required=True)
    licitacion_id = fields.Many2one('licitaciones.licitacion', string="Licitación")
    title = fields.Char(string="Título")
    url = fields.Char(string="URL")
    tipo_documento = fields.Char(string="Tipo de Documento")
    fecha_inicio = fields.Datetime(string="Fecha de Inicio", required=True)
    fecha_fin = fields.Datetime(string="Fecha de Fin", required=True)
    duracion_dias = fields.Integer(string="Duración en Días", compute='_compute_duracion_dias', store=True)

    
    download_icon = fields.Html(string="Descargar", compute="_compute_download_icon")

    def _compute_download_icon(self):
        for record in self:
            if record.url:
                record.download_icon = (
                    f'<a href="{record.url}" target="_blank">'
                    f'<i class="fa fa-download"></i></a>'
                )
            else:
                record.download_icon = "Sin enlace"