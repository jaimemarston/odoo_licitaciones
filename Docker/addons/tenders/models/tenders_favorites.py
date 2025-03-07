from odoo import models, fields, api,_
from odoo.exceptions import ValidationError
import re

import logging
class TendersFavorites(models.Model):
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

    emails_ids = fields.Many2many('licitaciones.emails.favorites', string='Emails')
    tenders_ids = fields.Many2many('licitaciones.licitacion', string='tenders')

    def send_massive_mails_favorites(self):
        favorites = self.search([('claves', '!=', False), ('emails_ids', '!=', False)])
        if favorites:
            for favorite in favorites:
                favorite.action_send_email()

    @api.onchange('claves')
    def _onchange_claves(self):
        if self.claves or self.montoinicial or self.montotope:
            domain = self.get_domain_tenders()
            if not domain:
                raise ValidationError(_("Debe agregar al menos una de los siguentes campos: Palabras claves, Monto inicial, Monto tope"))
                
            tenders_ids = self.env['licitaciones.licitacion'].search(domain)
            if not tenders_ids:
                self.tenders_ids = [(6, 0, [])]
                return
            self.tenders_ids = [(6, 0, tenders_ids.ids)]



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
    
    def get_domain_tenders(self):
        domain = []
        valid_fields = [self.claves, self.montoinicial, self.montotope]
        for field in valid_fields:
            if type(field) == str and field:
                domain.extend([("titulo", "ilike", "%" + field + "%")])
            if type(field) == float and field:
                domain.append(('monto_total','>=' if field == self.montoinicial else '<=', field))
        return domain

    def action_send_email(self):
        for record in self:
            if not record.emails_ids:
                raise ValidationError(_("Debe agregar correos electronicos para enviar las licitaciones"))
            
            domain = record.get_domain_tenders()
            if not domain:
                raise ValidationError(_("Debe agregar al menos una de los siguentes campos: Palabras claves, Monto inicial, Monto tope"))
            
            tenders_ids = self.env['licitaciones.licitacion'].search(domain)
            if tenders_ids:
                for favorite in record.emails_ids:

                    values_mail = self.generate_mail_template(tenders=tenders_ids,email_from=self.env.company.email or "noreply@company.com",email_to=favorite.email)
                    mail = self.env['mail.mail'].sudo().create(values_mail)
                    mail.send()


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
                            Te presentamos las licitaciones que coinciden con tus criterios de búsqueda.
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