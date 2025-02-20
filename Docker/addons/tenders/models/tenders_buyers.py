from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class TendersBuyer(models.Model):
    _name = 'licitaciones.buyer'
    _description = 'Comprador'

    name = fields.Char(string="Nombre del Comprador", required=True)
    rol = fields.Char(string="Rol")
    direccion = fields.Char(string="Dirección")
    localidad = fields.Char(string="Localidad")
    region = fields.Char(string="Región")
    pais = fields.Char(string="País")
    tender_ids = fields.One2many('licitaciones.buyer.pivot', 'buyer_id', string='tender')
