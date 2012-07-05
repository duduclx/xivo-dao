# -*- coding: utf-8 -*-
# Copyright (C) 2012  Avencall
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# Alternatively, XiVO CTI Server is available under other licenses directly
# contracted with Avencall. See the LICENSE file at top of the source tree
# or delivered in the installable package in which XiVO CTI Server is
# distributed for more details.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from xivo_dao.alchemy.groupfeatures import GroupFeatures
from xivo_dao.alchemy import dbconnection
from xivo_dao import group_dao
from xivo_dao.tests.test_dao import DAOTestCase


class TestGroupDAO(DAOTestCase):

    tables = [GroupFeatures]

    def setUp(self):
        self.empty_tables()

    def test_get_name(self):
        session = dbconnection.get_connection('asterisk').get_session()
        group = GroupFeatures()
        group.name = 'test_name'
        group.number = '1234'
        group.context = 'my_ctx'
        session.add(group)
        session.commit()

        result = group_dao.get_name(group.id)

        self.assertEqual(result, group.name)

    def test_get_name_number(self):
        group = GroupFeatures()
        group.name = 'test_name'
        group.number = '1234'
        group.context = 'my_ctx'

        self.session.add(group)
        self.session.commit()

        name, number = group_dao.get_name_number(group.id)

        self.assertEqual(name, 'test_name')
        self.assertEqual(number, '1234')
