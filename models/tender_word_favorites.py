from odoo import models, fields, api


class TenderWordFavorites(models.Model):
    _name = 'tender.word.favorites'
    

    name = fields.Char('name', required=True)
    

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'La palabra clave debe ser única.'),
    ]