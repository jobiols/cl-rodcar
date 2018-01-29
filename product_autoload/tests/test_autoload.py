# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from __future__ import division

from openerp.tests.common import TransactionCase
from ..models.product_mapper import ProductMapper

#    Forma de correr el test
#    -----------------------
#
#   Definir un subpackage tests que será inspeccionado automáticamente por
#   modulos de test los modulos de test deben empezar con test_ y estar
#   declarados en el __init__.py, como en cualquier package.
#
#   Hay que crear una base de datos no importa el nombre (por ejemplo
#   bulonfer_test) vacia y con el modulo que se va a testear instalado
#   (por ejemplo product_autoload).
#
#   El usuario admin tiene que tener password admin, Language English, Country
#   United States.
#
#   Correr el test con:
#
#    oe -Q cl-bulonfer test_autoload.py -c bulonfer -d bulonfer_test -m product_autoload
#
#    si le pongo -i modulo ejecuta el yml si le pongo -u modulo no lo ejecuta.
#

import os


class TestBusiness(TransactionCase):
    """ Cada metodo de test corre en su propia transacción y se hace rollback
        despues de cada uno.
    """

    def setUp(self):
        """ Este setup corre antes de cada método
        """
        super(TestBusiness, self).setUp()
        # obtener el path al archivo de datos
        self._data_path = os.path.realpath(__file__)
        self._data_path = self._data_path.replace('tests/test_autoload.py',
                                                  'data/')

    def test_01(self):
        """ Chequear creacion de ProductMapper
        """
        line = [
            '123456',
            'nombre-producto',
            'Descripción del producto',
            '7750082001169',
            '1000.52',
            '500.22',
            '200.50',
            '125.85',
            '601.AA.3157.jpg',
            '60',
            '2018-25-01 13:10:55']
        prod = ProductMapper(line, self._data_path)
        self.assertEqual(prod.default_code, '123456')
        self.assertEqual(prod.name, 'nombre-producto')
        self.assertEqual(prod.description_sale, 'Descripción del producto')
        self.assertEqual(prod.barcode, '7750082001169', )
        self.assertEqual(prod.list_price, 1000.52)
        self.assertEqual(prod.standard_price, 500.22)
        self.assertEqual(prod.weight, 200.50)
        self.assertEqual(prod.volume, 125.85)
        self.assertEqual(prod.warranty, 60)
        self.assertEqual(prod.write_date, '2018-25-01 13:10:55')

        val = {
            'warranty': 60.0,
            'barcode': '7750082001169',
            'list_price': 1000.52,
            'name': 'nombre-producto',
            'weight': 200.5,
            'standard_price': 500.22,
            'volume': 125.85,
            'default_code': '123456',
            'write_date': '2018-25-01 13:10:55',
            'description_sale': 'Descripci\xc3\xb3n del producto'}
        val.update(prod.default_values())

        for item in val:
            self.assertEqual(prod.values()[item], val[item])

    def test_02(self):
        """ Chequear creacion de ProductMapper con minimos datos
        """
        line = [
            '123456', '', '', '', '', '', '', '', '', '',
            '2018-25-01 13:10:55']
        prod = ProductMapper(line, self._data_path)
        self.assertEqual(prod.default_code, '123456')
        self.assertEqual(prod.name, False)
        self.assertEqual(prod.description_sale, False)
        self.assertEqual(prod.barcode, False)
        self.assertEqual(prod.list_price, False)
        self.assertEqual(prod.standard_price, False)
        self.assertEqual(prod.weight, False)
        self.assertEqual(prod.volume, False)
        self.assertEqual(prod.image_name, False)
        self.assertEqual(prod.warranty, False)
        self.assertEqual(prod.write_date, '2018-25-01 13:10:55')

        val = {
            'default_code': '123456',
            'write_date': '2018-25-01 13:10:55'
        }
        val.update(prod.default_values())
        self.assertEqual(prod.values(), val)

    def test_03(self):
        """ Cuequear update de producto
        """
        # verificar createm
        product_obj = self.env['product.product']
        product_obj.auto_load(self._data_path)

        prod_obj = self.env['product.product']
        prod = prod_obj.search([('default_code', '=', '601.AA.315/7')])
        self.assertEqual(len(prod), 1, 'NO ENCUENTRO EL PRODUCTO')

        prod = prod_obj.search([('default_code', '=', '601.HV.8800B')])
        self.assertEqual(len(prod), 1, 'NO ENCUENTRO EL PRODUCTO')

        prod = prod_obj.search([('default_code', '=', '601.I.10250')])
        self.assertEqual(len(prod), 1, 'NO ENCUENTRO EL PRODUCTO')

        # verificar update
        product_obj.auto_load(self._data_path)
