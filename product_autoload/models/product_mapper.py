# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

_logger = logging.getLogger(__name__)

MAP_DEFAULT_CODE = 0
MAP_NAME = 1
MAP_DESCRIPTION_SALE = 2
MAP_BARCODE = 3
MAP_LIST_PRICE = 4
MAP_STANDARD_PRICE = 5
MAP_WEIGHT = 6
MAP_VOLUME = 7
MAP_IMAGE_NAME = 8
MAP_WARRANTY = 9
MAP_WRITE_DATE = 10


class ProductMapper(object):
    def __init__(self, line, image_path):
        self._image_path = image_path
        self._default_code = False
        self._name = False
        self._description_sale = False
        self._barcode = False
        self._list_price = False
        self._standard_price = False
        self._weight = False
        self._volume = False
        self._image_name = False
        self._image = False
        self._warranty = False
        self._write_date = False

        self.default_code = line[MAP_DEFAULT_CODE]
        self.name = line[MAP_NAME]
        self.description_sale = line[MAP_DESCRIPTION_SALE]
        self.barcode = line[MAP_BARCODE]
        self.list_price = line[MAP_LIST_PRICE]
        self.standard_price = line[MAP_STANDARD_PRICE]
        self.weight = line[MAP_WEIGHT]
        self.volume = line[MAP_VOLUME]
        self.image_name = line[MAP_IMAGE_NAME]
        self.warranty = line[MAP_WARRANTY]
        self.write_date = line[MAP_WRITE_DATE]

    def values(self):
        ret = {'default_code': self.default_code}

        if self.name:
            ret['name'] = self.name

        if self._description_sale:
            ret['description_sale'] = self.description_sale

        if self.barcode:
            ret['barcode'] = self.barcode

        if self.list_price:
            ret['list_price'] = self.list_price

        if self.standard_price:
            ret['standard_price'] = self.standard_price

        if self.weight:
            ret['weight'] = self.weight

        if self.volume:
            ret['volume'] = self.volume

        if self.warranty:
            ret['warranty'] = self.warranty

        if self.write_date:
            ret['write_date'] = self.write_date

        if self._image:
            ret['image'] = self._image

        # agregar valores por defecto
        ret.update(self.default_values())
        return ret

    @staticmethod
    def default_values():
        return {
            'type': 'product',
            'invoice_policy': 'order',
            'purchase_method': 'purchase'
        }

    def execute(self, product_model):
        """
         si encuentra el producto en el modelo lo actualiza si no lo
         encuentra lo crea

        :param product_model: objeto product.product
        :return:
        """
        prod = product_model.search([('default_code', '=', self.default_code)])
        if prod:
            try:
                prod.write(self.values())
                _logger.info('Updating product %s', self.default_code)
            except Exception as ex:
                _logger.error(ex.message)
        else:
            try:
                product_model.create(self.values())
                _logger.info('Creating product %s', self.default_code)
            except Exception as ex:
                _logger.error(ex.message)

    @staticmethod
    def check_string(field, value):
        try:
            value.decode('utf-8')
        except UnicodeError as ex:
            _logger.error('%s Value: "%s": %s', field, value, ex.message)
        return value

    @staticmethod
    def check_numeric(field, value):
        try:
            ret = int(value)
        except ValueError as ex:
            _logger.error('%s Value: "%s": %s', field, value, ex.message)
        return value

    @staticmethod
    def check_currency(field, value):
        try:
            ret = float(value)
            return ret
        except ValueError as ex:
            _logger.error('%s Value: "%s": %s', field, value, ex.message)
        return False

    @staticmethod
    def check_float(field, value):
        try:
            ret = float(value)
            return ret
        except ValueError as ex:
            _logger.error('%s Value "%s": %s', field, value, ex.message)
        return False

    def slugify(self, field, value):
        ret = self.check_string(field, value)
        ret.replace('/', '')
        return ret

    @property
    def default_code(self):
        return self._default_code

    @default_code.setter
    def default_code(self, value):
        self._default_code = self.check_string('default_code', value)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value:
            self._name = self.check_string('name', value)

    @property
    def description_sale(self):
        return self._description_sale

    @description_sale.setter
    def description_sale(self, value):
        if value:
            self._description_sale = self.check_string('description_sale',
                                                       value)

    @property
    def barcode(self):
        return self._barcode

    @barcode.setter
    def barcode(self, value):
        if value:
            self._barcode = self.check_numeric('barcode', value)

    @property
    def list_price(self):
        return self._list_price

    @list_price.setter
    def list_price(self, value):
        if value:
            self._list_price = self.check_currency('list_price', value)

    @property
    def standard_price(self):
        return self._standard_price

    @standard_price.setter
    def standard_price(self, value):
        if value:
            self._standard_price = self.check_currency('standard_price', value)

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        if value:
            self._weight = self.check_float('weight', value)

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value):
        if value:
            self._volume = self.check_float('volume', value)

    @property
    def image_name(self):
        return self._image_name

    @image_name.setter
    def image_name(self, value):
        if value:
            self._image_name = self.slugify('image_name', value)
            # cargar la imagen
            try:
                with open(self._image_path + self._image_name,
                          'rb') as img_file:
                    self._image = img_file.read().encode('base64')
            except IOError as ex:
                logging.error('%s %s', ex.filename, ex.strerror)

    @property
    def warranty(self):
        return self._warranty

    @warranty.setter
    def warranty(self, value):
        if value:
            self._warranty = self.check_float('warranty', value)
