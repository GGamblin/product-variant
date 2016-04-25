# -*- coding: utf-8 -*-
# © 2016 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.multi
    @api.depends('lst_price')
    def _product_lst_price(self):
        for product in self:
            price = product.lst_price or product.list_price
            if 'uom' in self.env.context:
                uom = product.uos_id or product.uom_id
                price = uom.with_context(uom='uom')._compute_price(price)
            product.lst_price = price

    @api.multi
    def _set_product_lst_price(self):
        if 'uom' in self.env.context:
            for product in self:
                uom = product.uos_id or product.uom_id
                product.lst_price = uom.with_context(uom='uom')._compute_price(
                    product.lst_price)

    lst_price = fields.Float(
        compute='_product_lst_price',
        inverse='_set_product_lst_price',
        store=True,
    )
