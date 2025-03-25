from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re



class TendersPostores(models.Model):
    _name = 'licitaciones.postores'
    _description = 'postores'
    _rec_name = "nombre"
    postores_id = fields.Char(string="ID Postor", required=True)
    supplier_id = fields.Many2one('licitaciones.proveedor', string='supplier')
    nombre = fields.Char(string="Nombre", related='supplier_id.name', store=True)
    ruc = fields.Char(string="RUC", related='supplier_id.ruc')
    licitacion_id = fields.Many2one('licitaciones.licitacion', string="Licitación", ondelete="cascade")
    titulo = fields.Char('titulo', related='licitacion_id.titulo',store=True)
    monto_total = fields.Float('monto_total', related='licitacion_id.monto_total')
    ganador = fields.Boolean(string="Ganador", default=False)  # Campo Booleano
    fecha_publicacion = fields.Datetime(string='Fecha y Hora de Publicación', related='licitacion_id.fecha_publicacion',store=True)
    ganador_estado = fields.Selection([
            ('ganador', '🏆 Ganador')
        ], string="Estado", compute="_compute_ganador", store=True)

    @api.depends('ganador')
    def _compute_ganador(self):
        for record in self:
            record.ganador_estado = 'ganador' if record.ganador else None  # 🔹 Usa `None` en lugar de `False`

            if record.ganador and record.licitacion_id:
                record.licitacion_id.sudo().write({
                    'bidder_winner': record
                })
                if record.licitacion_id.buyer_id and 'bidder_id' in record.licitacion_id.buyer_id._fields:
                    record.licitacion_id.buyer_id.sudo().write({
                        'bidder_id': record
                    })
                    
            if not record.ganador and record.licitacion_id:
                record.licitacion_id.sudo().write({
                    'bidder_winner': False
                })
