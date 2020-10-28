# -*- coding: utf-8 -*-
# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from sqlalchemy import func

from hamcrest import assert_that, equal_to

from xivo_dao.tests.test_dao import DAOTestCase

from ..stat_agent import StatAgent


class TestStatAgent(DAOTestCase):
    def test_agent_number(self):
        agent = self.add_stat_agent(name='Agent/1004')

        self.session.expire_all()

        assert_that(agent.number, equal_to('1004'))

    def test_agent_number_empty(self):
        agent = self.add_stat_agent(name='')

        self.session.expire_all()

        assert_that(agent.number, equal_to(None))

    def test_number_min(self):
        self.add_stat_agent(name='Agent/1004')

        self.session.expire_all()

        result = self.session.query(
            func.min(StatAgent.number).label('min_number')
        ).first()

        assert_that(result.min_number, equal_to('1004'))

    def test_number_min_number_empty(self):
        self.add_stat_agent(name='not-prefixed')

        self.session.expire_all()

        result = self.session.query(
            func.min(StatAgent.number).label('min_number')
        ).first()

        assert_that(result.min_number, equal_to(None))
