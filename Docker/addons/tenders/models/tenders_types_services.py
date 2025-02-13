from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class TendersTipoServicio(models.Model):
    _name = 'licitaciones.tiposervicio'
    _description = 'Tipo de Servicio'

    name = fields.Char(string="Tipo de Servicio", required=True)
