# -*- coding: utf-8 -*-
from openerp import api, fields, models

from openerp import SUPERUSER_ID
from openerp.osv import osv
from openerp.tools.translate import _
from openerp.exceptions import UserError


class PosInvoiceReport(models.TransientModel):
    _inherit = 'report.point_of_sale.report_invoice'

    @api.model
    def render_html(self, data=None):
        import wdb; wdb.set_trace()
        res = super(PosInvoiceReport, self).render_html(data)
        return res
