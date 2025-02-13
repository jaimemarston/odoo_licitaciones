from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


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