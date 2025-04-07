from odoo import models, fields

class SupplierFilterWizard(models.TransientModel):
    _name = 'licitaciones.supplier.filter.wizard'
    _description = 'Filtro de Proveedores'

    name = fields.Char(string="Nombre")
    ruc = fields.Char(string="RUC")

    def aplicar_filtro(self):
        domain = []
        if self.name:
            domain.append(('name', 'ilike', self.name))
        if self.ruc:
            domain.append(('ruc', 'ilike', self.ruc))

        return {
            'type': 'ir.actions.act_window',
            'name': 'Proveedores Filtrados',
            'res_model': 'licitaciones.proveedor',
            'view_mode': 'list,form',
            'domain': domain,
            'target': 'current',
        }

    def action_cancelar(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Proveedores',
            'res_model': 'licitaciones.proveedor',
            'view_mode': 'list,form',
            'target': 'main',
        }
