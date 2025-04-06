from odoo import models, fields, api,_
from odoo.exceptions import ValidationError
import re

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
    tenders_ids = fields.Many2many('licitaciones.licitacion', string='tenders')
    words_ids = fields.Many2many('tender.word.favorites', string='words')
    date_start = fields.Datetime('date start')
    date_end = fields.Datetime('date end')
    user_id = fields.Many2one('res.users', string='user', default=lambda self: self.env.uid)
    email = fields.Char('email', related='user_id.email')

    def send_massive_mails_favorites(self):
        favorites = self.search([('claves', '!=', False), ('emails_ids', '!=', False)])
        if favorites:
            for favorite in favorites:
                favorite.action_send_email()

    @api.onchange('words_ids', 'montoinicial', 'montotope', 'date_start', 'date_end')
    def _onchange_words_ids(self):
        logging.info('\n' * 2)
        logging.info('in ochange')
        if self.words_ids or self.montoinicial or self.montotope:
            domain = self.get_domain_tenders()
            if not domain:
                raise ValidationError(_("Debe agregar al menos una de los siguentes campos: Palabras claves, Monto inicial, Monto tope"))
                
            tenders_ids = self.env['licitaciones.licitacion'].search(domain)
            if not tenders_ids:
                self.tenders_ids = [(6, 0, [])]
                return
            self.tenders_ids = [(6, 0, tenders_ids.ids)]



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
        logging.info('\n' * 3 + 'en domain')
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
        logging.info(f"Domain construido: {domain}")
        return domain

    def action_send_email(self):
        for record in self:
            if not record.email:
                raise ValidationError(_("Debe agregar correos electronicos para enviar las licitaciones"))
            
            domain = record.get_domain_tenders()
            if not domain:
                raise ValidationError(_("Debe agregar al menos una de los siguentes campos: Palabras claves, Monto inicial, Monto tope"))
            
            tenders_ids = self.env['licitaciones.licitacion'].search(domain)
            # for favorite in record.emails_ids:
            if record.email:
                if not tenders_ids:
                    phrases_ids = self.env['tenders.mail.phrases.message'].search([])
                    phrase = phrases_ids[0]._get_random_phrases() if phrases_ids else ""
                    values_mail = self.generate_for_website_mail_danger_template(message=phrase,email_from=self.env.company.email or "alertas@e-vali.com",email_to=record.email) 
                    mail = self.env['mail.mail'].sudo().create(values_mail)   
                    mail.send()
                    return

                # values_mail = self.generate_mail_template(tenders=tenders_ids,email_from=self.env.company.email or "noreply@company.com",email_to=favorite.email)
                base_url = self.obtener_url_base()
                url =  base_url + f'/favoritos/{record.id}' if base_url else ""
                values_mail = self.generate_for_website_mail_template(url=url,email_from=self.env.company.email or "alertas@e-vali.com",email_to=record.email)
                mail = self.env['mail.mail'].sudo().create(values_mail)
                mail.send()
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
                    <div style="margin: 0px; padding: 0px; background-color: #de99cc; color: #fff; padding: 8px; border-top-left-radius: 3px; border-top-right-radius: 3px;">
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
    
    def generate_for_website_mail_template(self, url, email_from, email_to):
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
                    <div style="margin: 0px; padding: 0px; background-color: #14212e; color: #fff; padding: 8px; border-top-left-radius: 3px; border-top-right-radius: 3px;">
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
                                                    <td style="padding: 10px; text-align: center;">{tender.objeto_contratacion}</td>
                                                </tr>
                                            ''' for tender in self.tenders_ids)}
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
                    <div style="margin: 0px; padding: 0px; background-color: #de99cc; color: #fff; padding: 8px; border-top-left-radius: 3px; border-top-right-radius: 3px;">
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