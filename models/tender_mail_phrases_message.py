from odoo import models, fields, api,_
from odoo.exceptions import ValidationError
import re
import random

class TendersMailPhrasesMessage(models.Model):
    _name = 'tenders.mail.phrases.message'
    _description = 'fraces para favoritos fallidos'

    name = fields.Char('name')
    type = fields.Selection([
        ('success', 'Success'),
        ('danger', 'danger')
    ], string='type', default="danger")
    

    def _get_random_phrases(self):
        phrases_ids = self.search([])
        pharse_id = random.choice(phrases_ids) if phrases_ids else False
        return pharse_id.name