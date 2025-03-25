from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class TendersItem(models.Model):
    _name = 'licitaciones.item'
    _description = 'Ítem'

    
    id_item = fields.Char(string="ID Ítem", required=True)  # Corresponde a item_id
    posicion = fields.Integer(string="Posición")  # Corresponde a position
    descripcion = fields.Text(string="Descripción")  # Corresponde a description
    estado_detalle = fields.Char(string="Detalle del Estado")  # Corresponde a status_details
    estado = fields.Char(string="Estado")  # Corresponde a status
    clasificacion_id = fields.Char(string="ID Clasificación")  # Corresponde a classification_id
    clasificacion_descripcion = fields.Char(string="Descripción Clasificación")  # Corresponde a classification_description
    clasificacion_esquema = fields.Char(string="Esquema Clasificación")  # Corresponde a scheme
    cantidad = fields.Float(string="Cantidad")  # Corresponde a quantity
    unidad_id = fields.Char(string="ID Unidad de Medida")  # Corresponde a unit_id
    unidad_nombre = fields.Char(string="Nombre Unidad de Medida")  # Corresponde a unit_name
    valor_total = fields.Float(string="Valor Total")  # Corresponde a total_value
    moneda = fields.Char(string="Moneda")  # Corresponde a currency
    licitacion_id = fields.Many2one('licitaciones.licitacion', string="Licitación", ondelete="cascade")  # Corresponde a licitacion_id

    # Campos adicionales (si es necesario)
    observaciones = fields.Text(string="Observaciones")  # Puedes agregar cualquier campo adicional que necesites