# -*- coding: utf-8 -*-
# Copyright 2013-2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from xivo_dao import callfilter_dao
from xivo_dao.alchemy.callfilter import Callfilter
from xivo_dao.alchemy.callfiltermember import Callfiltermember
from xivo_dao.tests.test_dao import DAOTestCase


class BaseTestCallFilterDAO(DAOTestCase):

    def _insert_call_filter(self, name):
        callfilter = Callfilter()
        callfilter.callfrom = 'internal'
        callfilter.type = 'bosssecretary'
        callfilter.bosssecretary = 'bossfirst-serial'
        callfilter.name = name
        callfilter.description = ''
        self.add_me(callfilter)
        return callfilter.id

    def _add_user_to_filter(self, userid, filterid, role='boss'):
        member = Callfiltermember()
        member.type = 'user'
        member.typeval = str(userid)
        member.callfilterid = filterid
        member.bstype = role
        self.add_me(member)
        return member


class TestGetSecretariesIdByContext(BaseTestCallFilterDAO):

    def _create_user_and_add_to_filter(self, filter_id, role, context='mycontext'):
        user_line_row = self.add_user_line_with_exten(context=context)
        filter_member_row = self._add_user_to_filter(user_line_row.user_id, filter_id, role)
        return filter_member_row

    def test_given_no_secretaries_then_returns_empty_list(self):
        result = callfilter_dao.get_secretaries_id_by_context('default')

        self.assertEqual(result, [])

    def test_given_boss_then_returns_empty_list(self):
        context = 'mycontext'
        filter_id = self._insert_call_filter('testfilter')
        self._create_user_and_add_to_filter(filter_id, 'boss', context)

        result = callfilter_dao.get_secretaries_id_by_context(context)

        self.assertEqual(result, [])

    def test_given_one_secretary_then_returns_list_with_id(self):
        context = 'mycontext'
        filter_id = self._insert_call_filter('testfilter')
        member = self._create_user_and_add_to_filter(filter_id, 'secretary', context)

        result = callfilter_dao.get_secretaries_id_by_context(context)

        self.assertEqual(len(result), 1)
        self.assertIn((member.id,), result)

    def test_given_two_secretaries_then_returns_list_with_both_ids(self):
        context = 'mycontext'
        filter_id = self._insert_call_filter('testfilter')
        first_member = self._create_user_and_add_to_filter(filter_id, 'secretary', context)
        second_member = self._create_user_and_add_to_filter(filter_id, 'secretary', context)

        result = callfilter_dao.get_secretaries_id_by_context(context)

        self.assertEqual(len(result), 2)
        self.assertIn((first_member.id,), result)
        self.assertIn((second_member.id,), result)

    def test_given_line_with_multiple_users_then_returns_list_with_one_id(self):
        context = 'mycontext'
        filter_id = self._insert_call_filter('testfilter')
        extension = self.add_extension(context=context)

        line = self.add_line(context=context)
        main_user = self.add_user()
        secondary_user = self.add_user()

        self.add_user_line(user_id=main_user.id,
                           line_id=line.id,
                           main_user=True,
                           main_line=True)
        self.add_user_line(user_id=secondary_user.id,
                           line_id=line.id,
                           main_user=False,
                           main_line=True)
        self.add_line_extension(line_id=line.id,
                                extension_id=extension.id)

        member = self._add_user_to_filter(main_user.id, filter_id, 'secretary')

        result = callfilter_dao.get_secretaries_id_by_context(context)

        self.assertEqual(len(result), 1)
        self.assertIn((member.id,), result)

    def test_given_user_with_multiple_line_then_returns_list_with_one_id(self):
        context = 'mycontext'
        filter_id = self._insert_call_filter('testfilter')
        extension = self.add_extension(context=context)

        main_line = self.add_line(context=context)
        secondary_line = self.add_line(context=context)
        user = self.add_user()

        self.add_user_line(user_id=user.id,
                           line_id=main_line.id,
                           main_user=True,
                           main_line=True)
        self.add_user_line(user_id=user.id,
                           line_id=secondary_line.id,
                           main_user=True,
                           main_line=False)
        self.add_line_extension(line_id=main_line.id,
                                extension_id=extension.id)
        self.add_line_extension(line_id=secondary_line.id,
                                extension_id=extension.id)

        member = self._add_user_to_filter(user.id, filter_id, 'secretary')

        result = callfilter_dao.get_secretaries_id_by_context(context)

        self.assertEqual(len(result), 1)
        self.assertIn((member.id,), result)


class TestCallFilterDAO(BaseTestCallFilterDAO):

    def test_get_with_no_filter(self):
        filter_id = 1

        result = callfilter_dao.get(filter_id)

        self.assertEqual(result, [])

    def test_get_with_filter_but_no_members(self):
        filter_id = self._insert_call_filter('testfilter')

        result = callfilter_dao.get(filter_id)

        self.assertEqual(result, [])

    def test_get_with_filter_having_members(self):
        boss_id = 1
        filter_id = self._insert_call_filter('testfilter')
        self._add_user_to_filter(boss_id, filter_id, 'boss')

        result = callfilter_dao.get(filter_id)

        self.assertEqual(1, len(result))
        callfilter = result[0][0]
        member = result[0][1]
        self.assertEqual(callfilter.id, filter_id)
        self.assertEqual(member.typeval, str(boss_id))

    def test_get_with_filter_having_2_members(self):
        boss_id = 1
        secretary_id = 2
        filter_id = self._insert_call_filter('testfilter')
        self._add_user_to_filter(boss_id, filter_id, 'boss')
        self._add_user_to_filter(secretary_id, filter_id, 'secretary')

        result = callfilter_dao.get(filter_id)

        self.assertEqual(2, len(result))
        member_ids = [int(c[1].typeval) for c in result]
        self.assertIn(boss_id, member_ids)
        self.assertIn(secretary_id, member_ids)

    def test_does_secretary_filter_boss_with_no_filters(self):
        boss_id = 1
        secretary_id = 2

        result = callfilter_dao.does_secretary_filter_boss(boss_id, secretary_id)

        self.assertFalse(result)

    def test_does_secretary_filter_boss_with_no_boss_or_secretary(self):
        boss_id = 1
        secretary_id = 2
        self._insert_call_filter('test1')

        result = callfilter_dao.does_secretary_filter_boss(boss_id, secretary_id)

        self.assertFalse(result)

    def test_does_secretary_filter_boss_with_no_secretary(self):
        boss_id = 1
        secretary_id = 2
        filter_id = self._insert_call_filter('test1')
        self._add_user_to_filter(boss_id, filter_id, 'boss')

        result = callfilter_dao.does_secretary_filter_boss(boss_id, secretary_id)

        self.assertFalse(result)

    def test_does_secretary_filter_boss_with_no_boss(self):
        boss_id = 1
        secretary_id = 2
        filter_id = self._insert_call_filter('test1')
        self._add_user_to_filter(secretary_id, filter_id, 'secretary')

        result = callfilter_dao.does_secretary_filter_boss(boss_id, secretary_id)

        self.assertFalse(result)

    def test_does_secretary_filter_boss_with_boss_and_secretary_in_different_filters(self):
        boss_id = 1
        secretary_id = 2
        boss_filter_id = self._insert_call_filter('bossfilter')
        secretatry_filter_id = self._insert_call_filter('secretaryfilter')
        self._add_user_to_filter(boss_id, boss_filter_id, 'boss')
        self._add_user_to_filter(secretary_id, secretatry_filter_id, 'secretary')

        result = callfilter_dao.does_secretary_filter_boss(boss_id, secretary_id)

        self.assertFalse(result)

    def test_does_secretary_filter_boss_with_boss_and_secretary_in_same_filter(self):
        boss_id = 1
        secretary_id = 2
        filter_id = self._insert_call_filter('testfilter')
        self._add_user_to_filter(boss_id, filter_id, 'boss')
        self._add_user_to_filter(secretary_id, filter_id, 'secretary')

        result = callfilter_dao.does_secretary_filter_boss(boss_id, secretary_id)

        self.assertTrue(result)

    def test_does_secretary_filter_boss_with_2_secretaries(self):
        boss_id = 1
        first_secretary_id = 20
        second_secretary_id = 21
        filter_id = self._insert_call_filter('testfilter')
        self._add_user_to_filter(boss_id, filter_id, 'boss')
        self._add_user_to_filter(first_secretary_id, filter_id, 'secretary')
        self._add_user_to_filter(second_secretary_id, filter_id, 'secretary')

        first_result = callfilter_dao.does_secretary_filter_boss(boss_id, first_secretary_id)
        second_result = callfilter_dao.does_secretary_filter_boss(boss_id, second_secretary_id)

        self.assertTrue(first_result)
        self.assertTrue(second_result)

    def test_does_secretary_filter_boss_with_2_bosses(self):
        first_boss_id = 1
        second_boss_id = 2
        secretary_id = 20
        filter_id = self._insert_call_filter('testfilter')
        self._add_user_to_filter(secretary_id, filter_id, 'secretary')
        self._add_user_to_filter(first_boss_id, filter_id, 'boss')
        self._add_user_to_filter(second_boss_id, filter_id, 'boss')

        first_result = callfilter_dao.does_secretary_filter_boss(first_boss_id, secretary_id)
        second_result = callfilter_dao.does_secretary_filter_boss(second_boss_id, secretary_id)

        self.assertTrue(first_result)
        self.assertTrue(second_result)
