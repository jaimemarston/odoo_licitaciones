from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class TendersBuyerPivot(models.Model):
    _name = 'licitaciones.buyer.pivot'

    tender_id = fields.Many2one('licitaciones.licitacion', string='Licitacion')
    buyer_id = fields.Many2one('licitaciones.buyer', string='Comprador')
    title = fields.Char('title', related='tender_id.titulo', store=True)
    name = fields.Char('name', related='buyer_id.name')
    tender_name = fields.Char('tender', related='tender_id.id_licitacion')
    tender_date = fields.Datetime('date_public', related='tender_id.fecha_publicacion')
    amount = fields.Float('amount',related='tender_id.monto_total')
    bidder_id = fields.Many2one('licitaciones.postores', string='supplier')