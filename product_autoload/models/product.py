# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

_logger = logging.getLogger(__name__)

from openerp import api, models
from .product_mapper import ProductMapper
import csv


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def auto_load(self, file_path):
        try:
            with open(file_path + 'data.csv', 'r') as file_csv:
                reader = csv.reader(file_csv)
                for line in reader:
                    prod = ProductMapper(line, file_path)
                    prod.execute(self)
        except IOError as ex:
            _logger.error('%s %s', ex.filename, ex.strerror)
