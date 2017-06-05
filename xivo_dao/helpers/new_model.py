# -*- coding: utf-8 -*-

# Copyright 2013-2017 The Wazo Authors  (see the AUTHORS file)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from __future__ import unicode_literals

import six

from xivo_dao.helpers import errors


class NewModel(object):

    def __init__(self, **kwargs):
        self._check_invalid_parameters(kwargs.keys())

        for model_field in self.FIELDS + list(self._RELATION.values()):
            model_field_value = kwargs.get(model_field, None)
            setattr(self, model_field, model_field_value)

    def _check_invalid_parameters(self, parameters):
        invalid = self.invalid_parameters(parameters)

        if len(invalid) > 0:
            raise errors.missing(*invalid)

    def __eq__(self, other):
        class_name = self.__class__.__name__
        if not isinstance(other, self.__class__):
            raise TypeError('Must compare a %s with another %s' % (class_name, class_name))

        current = {key: value for key, value in six.iteritems(self.__dict__)
                   if key not in self._RELATION.values()}
        other = {key: value for key, value in six.iteritems(other.__dict__)
                 if key not in self._RELATION.values()}
        return current == other

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        properties = ['%s: %s' % (field, getattr(self, field))
                      for field in self.FIELDS + list(self._RELATION.values())]
        text = '<%s %s>' % (self.__class__.__name__, ', '.join(properties))
        return text.encode('utf8')

    def update_from_data(self, data):
        self._check_invalid_parameters(data.keys())

        for parameter, value in six.iteritems(data):
            setattr(self, parameter, value)

    @classmethod
    def from_user_data(cls, properties):
        return cls(**properties)

    def to_user_data(self):
        data_dict = {}
        for model_field in self.FIELDS:
            if hasattr(self, model_field):
                field_value = getattr(self, model_field)
                data_dict[model_field] = field_value

        return data_dict

    def invalid_parameters(self, parameters):
        allowed = self.FIELDS + list(self._RELATION.values())
        return set(parameters).difference(set(allowed))

    def missing_parameters(self):
        missing = []

        for parameter in self.MANDATORY:
            try:
                attribute = getattr(self, parameter)
                if attribute is None:
                    missing.append(parameter)
            except AttributeError:
                missing.append(parameter)

        return missing
