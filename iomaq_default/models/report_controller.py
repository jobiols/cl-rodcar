# -*- coding: utf-8 -*-
from openerp.addons.web.http import route
from openerp.addons import report


class ReportControllerDerived(report.controllers.main.ReportController):

    @route(['/report/download'], type='http', auth="user")
    def report_download(self, data, token):

        # le cambiamos el reporte para que salga el de aeroo
        data = data.replace('point_of_sale.report_invoice',
                            'aeroo_report_ar_einvoice')

        ret = super(ReportControllerDerived, self).report_download(data, token)
        return ret
