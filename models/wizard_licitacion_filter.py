from odoo import models, fields

class LicitacionFilterWizard(models.TransientModel):
    _name = 'licitaciones.filter.wizard'
    _description = 'Filtro Inicial de Licitaciones'

    fecha_inicio = fields.Date(string="Desde")
    fecha_fin = fields.Date(string="Hasta")
    monto_minimo = fields.Float(string="Monto Mínimo")

    def aplicar_filtro(self):
        domain = []
        if self.fecha_inicio:
            domain.append(('fecha_publicacion', '>=', self.fecha_inicio))
        if self.fecha_fin:
            domain.append(('fecha_publicacion', '<=', self.fecha_fin))
        if self.monto_minimo:
            domain.append(('monto_total', '>=', self.monto_minimo))

        return {
            'type': 'ir.actions.act_window',
            'name': 'Licitaciones Filtradas',
            'res_model': 'licitaciones.licitacion',
            'view_mode': 'list,form',
            'domain': domain,
            'target': 'current',
        }
