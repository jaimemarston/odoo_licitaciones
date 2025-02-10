from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class Licitacion(models.Model):
    _name = 'licitaciones.licitacion'
    _description = 'Licitación'

    id_licitacion = fields.Char(string="ID Licitación", required=True)
    comprador_id = fields.Many2one('licitaciones.buyer', string="Comprador")
    fecha_publicacion = fields.Datetime(string='Fecha y Hora de Publicación', required=True)
    nomenclatura = fields.Char(string='Nomenclatura')
    reiniciado_desde = fields.Char(string='Reiniciado Desde')
    objeto_contratacion = fields.Char(string='Objeto de Contratación', required=True)
    descripcion_objeto = fields.Text(string='Descripción de Objeto')
    codigo_snip = fields.Char(string='Código SNIP')
    codigo_unico_inversion = fields.Char(string='Código Único de Inversión')
    metodo_adquisicion = fields.Char(string='Metodo de Adquisición')
    categoria_adquisicion = fields.Char(string='Categoria de Adquisición')
    valor_referencial = fields.Float(string='Valor Referencial')
    moneda = fields.Selection([
        ('PEN', 'Soles'),
        ('USD', 'Dólares')
    ], string='Moneda', required=True)
    version_seace = fields.Char(string='Versión SEACE')
    acciones = fields.Text(string='Acciones')
    monto_total = fields.Float(string="Monto Total")
    documento_ids = fields.One2many('licitaciones.documento', 'licitacion_id', string="Documentos")
    postores_ids = fields.One2many('licitaciones.postores', 'licitacion_id', string="Postores")
    titulo = fields.Char(string="Título")
    categoria_principal = fields.Char(string="Categoría Principal")
    item_ids = fields.One2many('licitaciones.item', 'licitacion_id', string="Ítems")
    cronograma_ids = fields.One2many('licitaciones.cronograma', 'licitacion_id', string="Cronograma")

class Buyer(models.Model):
    _name = 'licitaciones.buyer'
    _description = 'Comprador'

    name = fields.Char(string="Nombre del Comprador", required=True)
    rol = fields.Char(string="Rol")
    direccion = fields.Char(string="Dirección")
    localidad = fields.Char(string="Localidad")
    region = fields.Char(string="Región")
    pais = fields.Char(string="País")

class Cronograma(models.Model):
    _name = 'licitaciones.cronograma'
    _description = 'Cronograma'

    name = fields.Char(string="ID Cronograma", required=True)
    licitacion_id = fields.Many2one('licitaciones.licitacion', string="Licitación")
    tipo_periodo = fields.Selection([
        ('enquiry', 'Periodo de Consultas'),
        ('tender', 'Periodo de Licitación'),
        ('evaluation', 'Periodo de Evaluación'),
        ('award', 'Periodo de Adjudicación')
    ], string="Tipo de Periodo", required=True)
    fecha_inicio = fields.Datetime(string="Fecha de Inicio", required=True)
    fecha_fin = fields.Datetime(string="Fecha de Fin", required=True)
    duracion_dias = fields.Integer(string="Duración en Días", compute='_compute_duracion_dias', store=True)

    @api.depends('fecha_inicio', 'fecha_fin')
    def _compute_duracion_dias(self):
        for record in self:
            if record.fecha_inicio and record.fecha_fin:
                delta = record.fecha_fin - record.fecha_inicio
                record.duracion_dias = delta.days
            else:
                record.duracion_dias = 0

class Documento(models.Model):
    _name = 'licitaciones.documento'
    _description = 'Documento'

    id_documento = fields.Char(string="ID Documento", required=True)
    titulo = fields.Char(string="Título")
    url = fields.Char(string="URL")
    tipo_documento = fields.Char(string="Tipo de Documento")
    formato = fields.Char(string="Formato")
    fecha_publicacion = fields.Datetime(string="Fecha de Publicación")
    licitacion_id = fields.Many2one('licitaciones.licitacion', string="Licitación", ondelete="cascade")

class Postores(models.Model):
    _name = 'licitaciones.postores'
    _description = 'postores'

    postores_id = fields.Char(string="ID Postor", required=True)
    nombre = fields.Char(string="Nombre")
    ruc = fields.Char(string="RUC")
    licitacion_id = fields.Many2one('licitaciones.licitacion', string="Licitación", ondelete="cascade")
    ganador = fields.Boolean(string="Ganador", default=False)  # Campo Booleano
    fecha_publicacion = fields.Datetime(string='Fecha y Hora de Publicación', required=True)

    ganador_estado = fields.Selection([
            ('ganador', '🏆 Ganador')
        ], string="Estado", compute="_compute_ganador", store=True)

    @api.depends('ganador')
    def _compute_ganador(self):
        for record in self:
            record.ganador_estado = 'ganador' if record.ganador else None  # 🔹 Usa `None` en lugar de `False`

class Item(models.Model):
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

class Favorites(models.Model):
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

class TipoServicio(models.Model):
    _name = 'licitaciones.tiposervicio'
    _description = 'Tipo de Servicio'

    name = fields.Char(string="Tipo de Servicio", required=True)


class Proveedor(models.Model):
    _name = 'licitaciones.proveedor'
    _description = 'Proveedor'

    name = fields.Char(string="Nombre del Proveedor", required=True)
    ruc = fields.Char(string="RUC", required=True)
    direccion = fields.Char(string="Dirección")
    localidad = fields.Char(string="Localidad")
    region = fields.Char(string="Región")
    pais = fields.Char(string="País")
    correo = fields.Char(string="Correo Electrónico")
    telefono = fields.Char(string="Teléfono")
    categoria = fields.Selection([
        ('bien', 'Bien'),
        ('servicio', 'Servicio'),
        ('obra', 'Obra'),
        ('consultoria', 'Consultoría')
    ], string="Categoría de Servicio", required=True)