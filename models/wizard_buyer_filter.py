from odoo import models, fields

class BuyerFilterWizard(models.TransientModel):
    _name = 'licitaciones.buyer.filter.wizard'
    _description = 'Filtro de Contratantes'

    name = fields.Char(string="Nombre de Empresa")

    



    def aplicar_filtro(self):
        domain = []
        if self.name:
            domain.append(('name', 'ilike', self.name))

        return {
            'type': 'ir.actions.act_window',
            'name': 'Contratantes Filtrados',
            'res_model': 'licitaciones.buyer',
            'view_mode': 'list,form',
            'domain': domain,
            'target': 'current',
        }

    def action_cancelar(self):
        """Redirecciona a la vista de licitaciones al cancelar el wizard"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Contratantes',
            'res_model': 'licitaciones.buyer',
            'view_mode': 'list,form',
            'target': 'main',  # Cambiado a 'main' para evitar acumulación de pestañas
        }