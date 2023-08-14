# Copyright 2018-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import (
    assert_that,
    none,
    not_none,
)

from xivo_dao.resources.func_key.tests.test_helpers import FuncKeyHelper
from xivo_dao.tests.test_dao import DAOTestCase

from ..func_key_dest_agent import FuncKey


class TestDelete(DAOTestCase, FuncKeyHelper):

    def setUp(self):
        super().setUp()
        self.setup_funckeys()

    def test_func_key_deleted(self):
        agent = self.add_agent()
        feature_extension = self.add_feature_extension()
        func_key_dest_agent = self.add_agent_destination(agent.id, feature_extension.uuid)

        row = self.session.query(FuncKey).first()
        assert_that(row, not_none())

        self.session.delete(func_key_dest_agent)
        self.session.flush()

        row = self.session.query(FuncKey).first()
        assert_that(row, none())
