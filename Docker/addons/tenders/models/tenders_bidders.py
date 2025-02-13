from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class TendersPostores(models.Model):
    _name = 'licitaciones.postores'
    _description = 'postores'

    postores_id = fields.Char(string="ID Postor", required=True)
    nombre = fields.Char(string="Nombre")
    ruc = fields.Char(string="RUC")
    licitacion_id = fields.Many2one('licitaciones.licitacion', string="Licitación", ondelete="cascade")
    ganador = fields.Boolean(string="Ganador", default=False)  # Campo Booleano
    fecha_publicacion = fields.Datetime(string='Fecha y Hora de Publicación', required=True)

    ganador_estado = fields.Selection([
            ('ganador', '🏆 Ganador')
        ], string="Estado", compute="_compute_ganador", store=True)

    @api.depends('ganador')
    def _compute_ganador(self):
        for record in self:
            record.ganador_estado = 'ganador' if record.ganador else None  # 🔹 Usa `None` en lugar de `False`