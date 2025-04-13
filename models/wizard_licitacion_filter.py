from odoo import models, fields

class LicitacionFilterWizard(models.TransientModel):
    _name = 'licitaciones.filter.wizard'
    _description = 'Filtro Inicial de Licitaciones'

    contratante_id = fields.Many2one('licitaciones.buyer', string="Contratante")
    postor_id = fields.Many2one('licitaciones.proveedor', string="Postor")
    objetivo_contratacion = fields.Char(string="Objetivo de Contratación")
    items = fields.Char(string="Items")
    
    fecha_inicio = fields.Date(string="Desde")
    fecha_fin = fields.Date(string="Hasta")
    monto_minimo = fields.Float(string="Monto Mínimo")
    
    
    # Nuevo campo de selección
    categoria_adquisicion = fields.Selection([
        ('bienes', 'Bienes'),
        ('obras', 'Obras'),
        ('servicios', 'Servicios')
    ], string="Categoría de Adquisición")

    filtro_monto = fields.Selection([
        ('mayor_8uit', 'Monto Mayor a 8 UIT'),
        ('menor_8uit', 'Monto Menor o Igual a 8 UIT')
    ], string="Filtro de Monto")
    rango_fechas = fields.Selection([
        ('day', 'Día'),
        ('month', 'Mes'),
        ('year', 'Año')
    ], string="Rango de Fechas")

    def aplicar_filtro(self):
        domain = []
        uit = 3450

        if self.fecha_inicio:
            domain.append(('fecha_publicacion', '>=', self.fecha_inicio))
        if self.fecha_fin:
            domain.append(('fecha_publicacion', '<=', self.fecha_fin))
        if self.monto_minimo:
            domain.append(('monto_total', '>=', self.monto_minimo))
        if self.contratante_id:
            domain.append(('buyer_id', '=', self.contratante_id.id))
        if self.postor_id:
            domain.append(('postores_ids', 'in', self.postor_id.id))
        if self.objetivo_contratacion:
            domain.append(('objeto_contratacion', 'ilike', self.objetivo_contratacion))
        if self.items:
            domain.append(('item_ids.descripcion', 'ilike', self.items))
        if self.filtro_monto == 'mayor_8uit':
            domain.append(('monto_total', '>', 8 * uit))
        if self.categoria_adquisicion:
            domain.append(('categoria_adquisicion', '=', self.categoria_adquisicion))
        elif self.filtro_monto == 'menor_8uit':
            domain.append(('monto_total', '<=', 8 * uit))
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Licitaciones Filtradas',
            'res_model': 'licitaciones.licitacion',
            'view_mode': 'list,form',
            'domain': domain,
            'target': 'current',
        }
    
    def action_cancelar(self):
        """Redirecciona a la vista de licitaciones al cancelar el wizard"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Licitaciones',
            'res_model': 'licitaciones.licitacion',
            'view_mode': 'list,form',
            'target': 'main',  # Cambiado a 'main' de current para evitar acumulación de pestañas
        }