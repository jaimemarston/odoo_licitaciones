from odoo import models, fields, api,_
from odoo.exceptions import ValidationError
import re
from odoo.osv.expression import OR, AND
from datetime import date

import logging
class FeaturedTenders(models.Model):
    _name = 'featured.tenders'
    _description = 'Licitaciones Destacadas'

    tender_id = fields.Many2one('licitaciones.licitacion', string='tender')
    id_licitacion = fields.Char('id licitacion', related='tender_id.id_licitacion')
    fecha_publicacion = fields.Datetime('fecha publicacion', related='tender_id.fecha_publicacion')
    titulo = fields.Char('titulo', related='tender_id.titulo')
    objeto_contratacion = fields.Char('objeto contratacion', related='tender_id.objeto_contratacion')
    monto_total = fields.Float('monto total', related='tender_id.monto_total')
    user_id = fields.Many2one('res.users', string='user')
    favorite_id = fields.Many2one('licitaciones.favorites', string='Favorito')

    @api.constrains('tender_id', 'favorite_id', 'user_id')
    def _constrains_unique_tender_favorite_user(self):
        for record in self:
            existing_record = self.search([
                ('tender_id', '=', record.tender_id.id),
                ('favorite_id', '=', record.favorite_id.id),
                ('user_id', '=', record.user_id.id),
                ('id', '!=', record.id)
            ])
            if existing_record:
                raise ValidationError("Ya existe una licitación destacada con la misma licitación, favorito y usuario.")
            
    def action_remove_featured_tender(self):
        for record in self:
            record.unlink()
        return {'type': 'ir.actions.act_window_close'}