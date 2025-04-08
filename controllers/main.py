from collections import OrderedDict

from odoo import fields, http, _
from odoo.osv import expression
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.addons.account.controllers.download_docs import _get_headers, _build_zip_from_data
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
import logging
class TendersController(http.Controller):
    
    @http.route('/favoritos/<int:favorite_id>',type='http', auth='public', website=True)
    def tenders_public(self, favorite_id, **kw):
        tenders = request.env['licitaciones.favorites'].sudo().browse(favorite_id)
        values = {}
        if tenders and tenders.featured_tenders_ids:
            values['tenders'] = tenders.featured_tenders_ids
        return request.render("tenders.tenders_tenders_template_views", values)
    
    @http.route('/tenders/<int:tender_id>',type='http', auth='public', website=True)
    def tenders_form_public(self, tender_id, **kw):
        tender = request.env['licitaciones.licitacion'].sudo().browse(tender_id)
        values = {}
        if tender:
            values['tender'] = tender
        return request.render("tenders.tenders_tender_template_form", values)