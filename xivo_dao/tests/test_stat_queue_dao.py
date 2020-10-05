# -*- coding: utf-8 -*-
# Copyright 2013-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_dao import stat_queue_dao
from xivo_dao.alchemy.stat_queue import StatQueue
from xivo_dao.helpers.db_utils import flush_session
from xivo_dao.tests.test_dao import DAOTestCase


class TestStatQueueDAO(DAOTestCase):

    def test_id_from_name(self):
        queue = self._insert_queue('test_queue')

        result = stat_queue_dao.id_from_name(queue.name)

        self.assertEqual(result, queue.id)

    def test_insert_if_missing(self):
        confd_queues = [
            {
                'name': 'queue1',
                'tenant_uuid': 'tenant1',
            },
            {
                'name': 'queue2',
                'tenant_uuid': 'tenant2',
            },
            {
                'name': 'queue3',
                'tenant_uuid': 'tenant3',
            },
            {
                'name': 'queue4',
                'tenant_uuid': 'tenant4',
            },
        ]
        self._insert_queue('queue1', 'tenant1')
        self._insert_queue('queue2', 'tenant2')

        new_queues = ['queue1', 'queue3', 'queue4']

        with flush_session(self.session):
            stat_queue_dao.insert_if_missing(self.session, new_queues, confd_queues)

        result = [(name, tenant_uuid) for name, tenant_uuid in self.session.query(StatQueue.name, StatQueue.tenant_uuid).all()]

        self.assertTrue(('queue1', 'tenant1') in result)
        self.assertTrue(('queue2', 'tenant2') in result)
        self.assertTrue(('queue3', 'tenant3') in result)
        self.assertTrue(('queue4', 'tenant4') in result)
        self.assertEquals(len(result), 4)

    def test_clean_table(self):
        self._insert_queue('queue1')

        stat_queue_dao.clean_table(self.session)

        self.assertTrue(self.session.query(StatQueue).first() is None)

    def _insert_queue(self, name, tenant_uuid=None):
        queue = StatQueue()
        queue.name = name
        queue.tenant_uuid = tenant_uuid or self.default_tenant.uuid

        self.add_me(queue)

        return queue
