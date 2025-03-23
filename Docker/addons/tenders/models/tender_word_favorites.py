from odoo import models, fields, api


class TenderWordFavorites(models.Model):
    _name = 'tender.word.favorites'
    

    name = fields.Char('name')

    