from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class TendersFavorites(models.Model):
    _name = 'licitaciones.favorites'
    _description = 'Favoritos'

    claves = fields.Char(string="Palabras clave", required=True)
    restricciones = fields.Char(string="Restricciones")
    montoinicial = fields.Float(string="Monto Inicial (S/)", required=True)
    montotope = fields.Float(string="Monto Tope (S/)")
    pais = fields.Char(string="País")
    region = fields.Char(string="Región")
    distrito = fields.Char(string="Distrito")
    tiposervicio_ids = fields.Many2many(
        'licitaciones.tiposervicio',
        string="Tipo de Servicio"
    )
    correo = fields.Char(string="Correos Electrónicos", help="Ingrese múltiples correos separados por comas.")

    @api.constrains('correo')
    def _check_correo(self):
        """Valida que los correos estén en formato correcto y separados por comas."""
        email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
        for record in self:
            if record.correo:
                emails = record.correo.split(',')
                for email in emails:
                    email = email.strip()
                    if not email_regex.match(email):
                        raise ValidationError(f"El correo '{email}' no tiene un formato válido.")
