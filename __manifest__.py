{
    'name': 'Licitaciones',
    'version': '2.1',
    'category': 'Tools',
    'summary': 'Gestión de Licitaciones',
    'description': """Modulo para gestionar licitaciones.
    Incluye un formulario con campos básicos para registrar detalles de licitaciones.""",
    'author': 'Marston Software',
    'depends': ['base', 'board', 'mail', 'web'],  # Agregar 'board' como dependencia
    'data': [
        'data/licitaciones_tiposervicio_data.xml',
        'data/mail_discuss_channel.xml',
        'security/ir.model.access.csv',
        'views/licitaciones_dashboard_views.xml',
        'views/licitacion_views.xml',
        'views/favorites_views.xml',
        'views/buyer_views.xml',
        'views/proveedor_views.xml',
        'views/wizard_licitacion_filter.xml',
        'views/wizard_buyer_filter.xml',
        'views/wizard_proveedor_filter.xml',
        'views/tenders_competence_views.xml',
        'views/menus.xml',
        'wizard/supplier_users_views.xml',
        'data/ir_cron_data.xml',
        # TEMPLATES
        'views/templates/tenders_template.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_backend': [
            'tenders/static/src/js/**/*.*',
        ],
    },
}

