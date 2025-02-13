from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class TendersCronograma(models.Model):
    _name = 'licitaciones.cronograma'
    _description = 'Cronograma'

    name = fields.Char(string="ID Cronograma", required=True)
    licitacion_id = fields.Many2one('licitaciones.licitacion', string="Licitación")
    tipo_periodo = fields.Selection([
        ('enquiry', 'Periodo de Consultas'),
        ('tender', 'Periodo de Licitación'),
        ('evaluation', 'Periodo de Evaluación'),
        ('award', 'Periodo de Adjudicación')
    ], string="Tipo de Periodo", required=True)
    fecha_inicio = fields.Datetime(string="Fecha de Inicio", required=True)
    fecha_fin = fields.Datetime(string="Fecha de Fin", required=True)
    duracion_dias = fields.Integer(string="Duración en Días", compute='_compute_duracion_dias', store=True)