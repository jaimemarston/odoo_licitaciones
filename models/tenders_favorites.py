from odoo import models, fields, api,_
from odoo.exceptions import ValidationError
import re
from odoo.osv.expression import OR, AND
from datetime import date

import logging
class TendersFavorites(models.Model):
    _name = 'licitaciones.favorites'
    _description = 'Favoritos'

    claves = fields.Char(string="Palabras clave")
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

    emails_ids = fields.Many2many('licitaciones.emails.favorites', string='Emails')
    tenders_ids = fields.Many2many('licitaciones.licitacion', string='tenders',readonly=True)
    words_ids = fields.Many2many('tender.word.favorites', string='words')
    date_start = fields.Date('date start', default=lambda self: date.today().replace(year=date.today().year - 1))
    date_end = fields.Date('date end')
    user_id = fields.Many2one('res.users', string='user', default=lambda self: self.env.uid)
    email = fields.Char('email', related='user_id.email')
    is_featured = fields.Boolean(string="Destacado", default=False)  # Campo nuevo
    # Relación con licitaciones
    # tenders_ids = fields.One2many('licitaciones.licitacion', 'favorites_id', string="Licitaciones", on_delete="set null")
    
    # Relación directa para los destacados con dominio
    featured_tenders_ids = fields.One2many(
        'featured.tenders', 'favorite_id', 
        string="Destacados",
    )
    def action_filter_tenders_favorites(self):
        allow_fields = [self.words_ids, self.montoinicial, self.montotope, self.date_start, self.date_end, self.tiposervicio_ids]
        if not any(allow_fields):
            raise  ValidationError(_("Debe rellenar al menos una de los siguentes campos: Palabras claves, Monto inicial, Monto tope, Fecha de inicio, Fecha final"))
        domain = self.get_domain_tenders()
        # domain.append(('estado_item', '=', 'active'))
        tenders_ids = self.env['licitaciones.licitacion'].search(domain)
        if not tenders_ids:
            self.tenders_ids = [(6, 0, [])]
            return
        self.tenders_ids = [(6,0, tenders_ids.ids)]
        self.split_tenders_favorites()
        return
    
    def action_clear_tenders_favorites(self):
        self.tenders_ids = [(6, 0, [])]
        return

    def split_tenders_favorites(self):
        for record in self:
            if not record.featured_tenders_ids or not record.tenders_ids:
                return
            featured = record.featured_tenders_ids.mapped('tender_id')
            tenders_remove = record.tenders_ids.filtered(lambda rec: rec in featured)
            if not tenders_remove:
                return
            record.write({'tenders_ids': [(3, rec.id) for rec in tenders_remove]})

    def send_massive_mails_favorites(self):
        favorites = self.search([('words_ids', '!=', False), ('email', '!=', False), ('tenders_ids', '!=', False)])
        if favorites:
            for favorite in favorites:
                today = fields.Date.today()
                tenders_ids = favorite.tenders_ids.filtered(lambda tender: tender.write_date and tender.write_date.date() >= today and tender.estado_item == 'activo')
                favorite.send_mail_favorite(tenders_ids=tenders_ids)

    # @api.onchange('words_ids', 'montoinicial', 'montotope', 'date_start', 'date_end', 'tiposervicio_ids')
    # def _onchange_words_ids(self):
    #     logging.info('\n' * 2)
    #     logging.info('in ochange')
    #     if self.words_ids or self.montoinicial or self.montotope:
    #         domain = self.get_domain_tenders()
    #         if not domain:
    #             raise ValidationError(_("Debe agregar al menos una de los siguentes campos: Palabras claves, Monto inicial, Monto tope"))
    #         # domain.append(('estado_item', '=', 'active'))
    #         tenders_ids = self.env['licitaciones.licitacion'].search(domain)
    #         logging.info(f"Dominio aplicado: {domain}")
    #         logging.info(f"IDs encontrados: {tenders_ids.ids}")
    #         if not tenders_ids:
    #             self.tenders_ids = [(6, 0, [])]
    #             return
    #             # raise ValidationError(f"No se encontraron licitaciones que coincidan con los criterios seleccionados.")
    #         self.tenders_ids = [(6, 0, tenders_ids.ids)]



    @api.constrains('email')
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
    
    # def get_domain_tenders(self):
    #     logging.info('\n' * 3)
    #     logging.info('en domaiiiiin')
    #     domain = []
    #     valid_fields = [self.words_ids, self.montoinicial, self.montotope, self.date_start, self.date_end]
    #     for field in valid_fields:
    #         logging.info(field)
    #         if not field:
    #             logging.info('fiel no rellenado %s' % str(field))
    #             continue
    #         if field == self.words_ids:
    #             keys = field.mapped('name')
    #             logging.info(keys)
    #             domain = ['|'] * (len(keys) - 1) if keys else []
    #             for key in keys:
    #                 domain.extend([("objeto_contratacion", "ilike", "%" + key + "%")])
    #                 continue
                
    #         if type(field) == float:
    #             domain.append(('monto_total','>=' if field == self.montoinicial else '<=', field))
    #         logging.info(type(field))
    #     return domain
        
    def get_domain_tenders(self):
        logging.info('\n' * 3 + '💡 Ejecutando get_domain_tenders')

        word_conditions = []
        extra_conditions = []
        domain = []
        if self.words_ids:
            keys = self.words_ids.mapped('name')
            domain.extend([('objeto_contratacion', 'ilike', f"%{key}%") for key in keys])
            if len(keys) > 1:
                domain = ['|'] * (len(keys) - 1) + domain
        if self.montoinicial:
            domain.append(('monto_total', '>=', self.montoinicial))
        if self.montotope:
            logging.info(self.montotope)
            domain.append(('monto_total', '<=', self.montotope))

        if self.date_start:
            domain.append(('fecha_publicacion', '>=', self.date_start))

        if self.date_end:
            domain.append(('fecha_publicacion', '<=', self.date_end))

        if self.tiposervicio_ids:
            services = self.tiposervicio_ids.mapped('name')
            domain.extend([('categoria_adquisicion', 'ilike', f"%{service}%") for service in services])
        logging.info(f"Domain construido: {domain}")
        return domain


        logging.info(f"✅ Dominio final construido: {domain}")
        return domain

    def action_send_email(self):
        for record in self:
            if not record.email:
                raise ValidationError(_("Debe agregar correos electronicos para enviar las licitaciones"))
            record.send_mail_favorite(tenders_ids= record.featured_tenders_ids.mapped('tender_id') if record.featured_tenders_ids else record.tenders_ids)
            
            # domain = record.get_domain_tenders()
            # if not domain:
                # raise ValidationError(_("Debe agregar al menos una de los siguentes campos: Palabras claves, Monto inicial, Monto tope"))
    def send_mail_favorite(self, tenders_ids=None):
        if not tenders_ids:
            raise ValidationError(_("Debe agregar licitaciones"))
        # for favorite in record.emails_ids:
        if self.email:
            if not tenders_ids:
                phrases_ids = self.env['tenders.mail.phrases.message'].search([])
                phrase = phrases_ids[0]._get_random_phrases() if phrases_ids else ""
                values_mail = self.generate_for_website_mail_danger_template(message=phrase,email_from=self.env.company.email or "alertas@e-vali.com",email_to=self.email) 
                mail = self.env['mail.mail'].sudo().create(values_mail)   
                mail.send()
                return

            # values_mail = self.generate_mail_template(tenders=tenders_ids,email_from=self.env.company.email or "noreply@company.com",email_to=favorite.email)
            base_url = self.obtener_url_base()
            url =  base_url + f'/favoritos/{self.id}' if base_url else ""
            values_mail = self.generate_for_website_mail_template(url=url,email_from=self.env.company.email or "alertas@e-vali.com",email_to=self.email, tenders=tenders_ids)
            mail = self.env['mail.mail'].sudo().create(values_mail)
            #mail.send()

            try:
                mail.send()
                logging.info(f"Correo enviado a {self.email}")
            except Exception as e:
                logging.error(f"Error al enviar el correo: {e}")


    def obtener_url_base(self):
        website = self.env['website'].get_current_website()
        if website:
            base_url = website.get_base_url()
            return base_url
        else:
            return False

    def generate_mail_template(self, tenders, email_from, email_to):
        user_lang = self.env.lang or 'en_US'
        mail_values = {
            'subject': self.with_context(lang=user_lang).env._('Tus licitaciones'),
            'body_html': f"""
                <!DOCTYPE html>
                <html>
                <head>
                <style>
                    /* ... (Estilos CSS existentes) ... */
                    table {{
                        width: 100%;
                        border-collapse: collapse;
                        margin-top: 20px;
                    }}
                    th, td {{
                        border: 1px solid #ddd;
                        padding: 8px;
                        text-align: left;
                    }}
                    th {{
                        background-color: #f2f2f2;
                        font-weight: bold;
                    }}
                </style>
                </head>
                <body>
                <div class="email-container">
                    <div style="margin: 0px; padding: 0px; background-color: #24a2ee; color: #fff; padding: 8px; border-top-left-radius: 3px; border-top-right-radius: 3px;">
                        <h2 style="margin: 0px; padding: 0px; font-size: 16px; text-align: center; color: #ffffff;">
                            Licitaciones de tus favoritos
                        </h2>
                    </div>
                    <div style="margin: 10px; padding: 10px; background-color: #FFFFFF; border-radius: 3px;">
                        <p>
                            Estimado(a) Usuario,
                        </p>
                        <p>
                            Hemos detectado las siguientes licitaciones según tus palabras claves.
                        </p>
                        <table>
                            <thead>
                                <tr>
                                    <th style="text-align: center; padding: 10px; border: 1px solid #ddd; background-color: #f2f2f2;">ID de la Licitación</th>
                                    <th style="text-align: center; padding: 10px; border: 1px solid #ddd; background-color: #f2f2f2;">Contratante</th>
                                    <th style="text-align: center; padding: 10px; border: 1px solid #ddd; background-color: #f2f2f2;">Monto Total</th>
                                    <th style="text-align: center; padding: 10px; border: 1px solid #ddd; background-color: #f2f2f2;">URL de los Documentos</th>
                                </tr>
                            </thead>
                            <tbody>
                                {''.join(f'''
                                    <tr>
                                        <td style="padding: 10px; text-align: center;">{tender.id_licitacion}</td>
                                        <td style="padding: 10px; text-align: center;">{tender.buyer_id.name}</td>
                                        <td style="padding: 10px; text-align: center;">{tender.monto_total}</td>
                                        <td style="padding: 10px; text-align: center;">
                                            {''.join(f'''
                                                <a href="{url}">click aqui</a><br/>
                                            ''' for url in tender.cronograma_ids.mapped("url"))}
                                        </td>
                                    </tr>
                                ''' for tender in tenders)}
                            </tbody>
                        </table>
                        <p>
                            Esperamos que esta información te sea útil. Si tienes alguna pregunta, no dudes en contactarnos.
                        </p>
                        <p>
                            Atentamente,
                        </p>
                        <p>
                            El equipo de {self.env.company.name}
                        </p>
                    </div>
                </div>
                </body>
                </html>
            """,
            'email_to': email_to,
            'email_from': email_from,
        }
        return mail_values
    
    def generate_for_website_mail_template(self, url, email_from, email_to, tenders):
        user_lang = self.env.lang or 'en_US'
        mail_values = {
            'subject': self.with_context(lang=user_lang).env._('Tus licitaciones'),
            'body_html': f"""
                <!DOCTYPE html>
                <html>
                <head>
                <style>
                    /* ... (Estilos CSS existentes) ... */
                    table {{
                        width: 100%;
                        border-collapse: collapse;
                        margin-top: 20px;
                    }}
                    th, td {{
                        border: 1px solid #ddd;
                        padding: 8px;
                        text-align: left;
                    }}
                    th {{
                        background-color: #f2f2f2;
                        font-weight: bold;
                    }}
                </style>
                </head>
                <body>
                <div class="email-container container">
                    <div style="margin: 0px; padding: 0px; background-color: #24a2ee; color: #fff; padding: 8px; border-top-left-radius: 3px; border-top-right-radius: 3px;">
                        <h2 style="margin: 0px; padding: 0px; font-size: 16px; text-align: center; color: #ffffff;">
                            Licitaciones de tus favoritos
                        </h2>
                    </div>
                    <div style="background-color: #FFFFFF; border-radius: 3px;">
                        <p>
                            Estimado(a) Usuario,
                        </p>
                        <p>
                            Hemos detectado las sigueintes licitaciones según tus palabras claves.
                        </p>
                        <p>
                            Enlace: <a href="{url}">click aqui!</a>
                        </p> 
                        <div class="row">
                            <div class="panel panel-primary filterable">
                                <div id="wrap" class="table-responsive">
                                    <table class="table table-sm">
                                        <thead>
                                            <tr>
                                                <th style="text-align: center; padding: 10px; border: 1px solid #ddd; background-color: #f2f2f2;">Objeto contratación</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {''.join(f'''
                                                <tr>
                                                    <td style="padding: 10px;"><span style="background-color: #f2f2f2; text-align: center;">{tender.objeto_contratacion}</span>
                                                            {''.join(f'''
                                                                <div style="padding: 10px; text-align: left;"> * Titulo: {crono.title} - Fecha inicio: {crono.fecha_inicio} - Fecha fin: {crono.fecha_fin}</div>
                                                            ''' for crono in tender.cronograma_ids)}
                                                    </td>
                                                </tr>
                                            ''' for tender in tenders)}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                        <p>
                            Recuerda: Revisa los documentos con anticipación y asegúrate de cumplir con los requisitos antes de la fecha límite.
                        </p>
                        <p>
                            Esperamos que esta información te sea útil. Si tienes alguna pregunta, no dudes en contactarnos.
                        </p>
                        <p>
                            Atentamente,
                        </p>
                        <p>
                            El equipo de {self.env.company.name}
                        </p>
                    </div>
                </div>
                </body>
                </html>
            """,
            'email_to': email_to,
            'email_from': email_from,
        }
        return mail_values
    

    def generate_for_website_mail_danger_template(self, message, email_from, email_to):
        user_lang = self.env.lang or 'en_US'
        mail_values = {
            'subject': self.with_context(lang=user_lang).env._('Tus licitaciones'),
            'body_html': f"""
                <!DOCTYPE html>
                <html>
                <head>
                <style>
                    /* ... (Estilos CSS existentes) ... */
                    table {{
                        width: 100%;
                        border-collapse: collapse;
                        margin-top: 20px;
                    }}
                    th, td {{
                        border: 1px solid #ddd;
                        padding: 8px;
                        text-align: left;
                    }}
                    th {{
                        background-color: #f2f2f2;
                        font-weight: bold;
                    }}
                </style>
                </head>
                <body>
                <div class="email-container">
                    <div style="margin: 0px; padding: 0px; background-color: #24a2ee; color: #fff; padding: 8px; border-top-left-radius: 3px; border-top-right-radius: 3px;">
                        <h2 style="margin: 0px; padding: 0px; font-size: 16px; text-align: center; color: #ffffff;">
                            Licitaciones de tus favoritos
                        </h2>
                    </div>
                    <div style="margin: 10px; padding: 10px; background-color: #FFFFFF; border-radius: 3px;">
                        <p>
                            Estimado(a) Usuario,
                        </p>
                        <p>
                            {message}
                        </p>
                        <p>
                            Atentamente,
                        </p>
                        <p>
                            El equipo de {self.env.company.name}
                        </p>
                    </div>
                </div>
                </body>
                </html>
            """,
            'email_to': email_to,
            'email_from': email_from,
        }
        return mail_values
    
    # @api.model
    # def create(self, vals):
    #     record = super().create(vals)
    #     record.action_send_email()
    #     return record

    def refres_favorites(self):
        favorites = self.search([])
        for favorite in favorites:
            favorite._onchange_words_ids()

    # @api.constrains('words_ids')
    # def _check_unique_words_optimized(self):
    #     for record in self:
    #         if not record.words_ids:
    #             continue
    #         existing_favorites = self.search([('words_ids', 'in', record.words_ids.ids),('id', '!=', record.id)])
    #         if existing_favorites:
    #             duplicated_words = record.words_ids & existing_favorites.mapped('words_ids')
    #             if duplicated_words:
    #                 word_names = ", ".join(duplicated_words.mapped('name'))
    #                 raise ValidationError(f"Las siguientes palabras clave ya están asignadas a otro favorito: {word_names}")