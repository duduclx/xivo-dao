# -*- coding: utf-8 -*-
# Copyright 2007-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from xivo_dao import context_dao
from xivo_dao.tests.test_dao import DAOTestCase


class TestContextDAO(DAOTestCase):

    def test_get(self):
        context_name = 'test_context'
        tenant = self.add_tenant()

        self.add_context(name=context_name, tenant_uuid=tenant.uuid)

        context = context_dao.get(context_name)

        self.assertEqual(context.name, context_name)
