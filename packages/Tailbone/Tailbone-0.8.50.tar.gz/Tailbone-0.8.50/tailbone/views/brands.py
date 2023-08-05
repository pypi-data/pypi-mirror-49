# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2018 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Brand Views
"""

from __future__ import unicode_literals, absolute_import

from rattail.db import model

from tailbone.views import MasterView, AutocompleteView


class BrandsView(MasterView):
    """
    Master view for the Brand class.
    """
    model_class = model.Brand
    has_versions = True

    grid_columns = [
        'name',
        'confirmed',
    ]

    form_fields = [
        'name',
        'confirmed',
    ]

    def configure_grid(self, g):
        super(BrandsView, self).configure_grid(g)

        # name
        g.filters['name'].default_active = True
        g.filters['name'].default_verb = 'contains'
        g.set_sort_defaults('name')
        g.set_link('name')

        # confirmed
        g.set_type('confirmed', 'boolean')


class BrandsAutocomplete(AutocompleteView):

    mapped_class = model.Brand
    fieldname = 'name'


def includeme(config):

    # autocomplete
    config.add_route('brands.autocomplete', '/brands/autocomplete')
    config.add_view(BrandsAutocomplete, route_name='brands.autocomplete',
                    renderer='json', permission='brands.list')

    BrandsView.defaults(config)
