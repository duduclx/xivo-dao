# -*- coding: utf-8 -*-
# Copyright 2015-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from hamcrest import (
    all_of,
    assert_that,
    empty,
    equal_to,
    has_item,
    has_items,
    has_length,
    has_properties,
    is_not,
    none,
    not_,
    not_none,
)
from sqlalchemy.inspection import inspect

from xivo_dao.alchemy.usersip import UserSIP as SIPEndpoint
from xivo_dao.helpers.exception import InputError
from xivo_dao.helpers.exception import NotFoundError
from xivo_dao.resources.utils.search import SearchResult
from xivo_dao.tests.test_dao import DAOTestCase

from .. import dao as sip_dao

ALL_OPTIONS = [
    ['buggymwi', 'yes'],
    ['amaflags', 'default'],
    ['sendrpid', 'yes'],
    ['videosupport', 'yes'],
    ['maxcallbitrate', '1024'],
    ['session-minse', '10'],
    ['maxforwards', '1'],
    ['rtpholdtimeout', '15'],
    ['session-expires', '60'],
    ['ignoresdpversion', 'yes'],
    ['textsupport', 'yes'],
    ['unsolicited_mailbox', '1000@default'],
    ['fromuser', 'field-user'],
    ['useclientcode', 'yes'],
    ['call-limit', '1'],
    ['progressinband', 'yes'],
    ['transport', 'udp'],
    ['directmedia', 'update'],
    ['promiscredir', 'yes'],
    ['allowoverlap', 'yes'],
    ['dtmfmode', 'info'],
    ['language', 'fr_FR'],
    ['usereqphone', 'yes'],
    ['qualify', '500'],
    ['trustrpid', 'yes'],
    ['timert1', '1'],
    ['session-refresher', 'uas'],
    ['allowsubscribe', 'yes'],
    ['session-timers', 'originate'],
    ['busylevel', '1'],
    ['callcounter', 'no'],
    ['callerid', '"cûstomcallerid" <1234>'],
    ['encryption', 'yes'],
    ['use_q850_reason', 'yes'],
    ['disallowed_methods', 'disallowsip'],
    ['rfc2833compensate', 'yes'],
    ['g726nonstandard', 'yes'],
    ['contactdeny', '127.0.0.1'],
    ['snom_aoc_enabled', 'yes'],
    ['t38pt_udptl', 'yes'],
    ['subscribemwi', 'no'],
    ['autoframing', 'yes'],
    ['t38pt_usertpsource', 'yes'],
    ['fromdomain', 'field-domain'],
    ['allowtransfer', 'yes'],
    ['nat', 'force_rport,comedia'],
    ['contactpermit', '127.0.0.1'],
    ['rtpkeepalive', '15'],
    ['insecure', 'port'],
    ['permit', '127.0.0.1'],
    ['deny', '127.0.0.1'],
    ['timerb', '1'],
    ['rtptimeout', '15'],
    ['disallow', 'all'],
    ['allow', 'gsm'],
    ['accountcode', 'accountcode'],
    ['md5secret', 'abcdefg'],
    ['mohinterpret', 'mohinterpret'],
    ['vmexten', '1000'],
    ['callingpres', '1'],
    ['parkinglot', '700'],
    ['fullname', 'fullname'],
    ['defaultip', '127.0.0.1'],
    ['qualifyfreq', '5000'],
    ['regexten', 'regexten'],
    ['cid_number', '0123456789'],
    ['callbackextension', '0123456789'],
    ['port', '10000'],
    ['outboundproxy', '127.0.0.1'],
    ['remotesecret', 'remotesecret'],
]


class TestFindBy(DAOTestCase):

    def test_given_column_does_not_exist_then_raises_error(self):
        self.assertRaises(InputError, sip_dao.find_by, column=1)

    def test_given_row_with_value_does_not_exist_then_returns_null(self):
        result = sip_dao.find_by(name='abcd')
        assert_that(result, none())

    def test_find_by(self):
        sip = self.add_usersip(name='myname')
        result = sip_dao.find_by(name='myname')

        assert_that(result.id, equal_to(sip.id))

    def test_find_by_multi_tenant(self):
        tenant = self.add_tenant()

        sip_row = self.add_usersip()
        sip = sip_dao.find_by(name=sip_row.name, tenant_uuids=[tenant.uuid])
        assert_that(sip, none())

        sip_row = self.add_usersip(tenant_uuid=tenant.uuid)
        sip = sip_dao.find_by(name=sip_row.name, tenant_uuids=[tenant.uuid])
        assert_that(sip, equal_to(sip_row))


class TestFindAllBy(DAOTestCase):

    def test_find_all_multi_tenant(self):
        tenant = self.add_tenant()

        sip1 = self.add_usersip(language='en_US', tenant_uuid=tenant.uuid)
        sip2 = self.add_usersip(language='en_US')

        tenants = [tenant.uuid, self.default_tenant.uuid]
        sips = sip_dao.find_all_by(language='en_US', tenant_uuids=tenants)
        assert_that(sips, has_items(sip1, sip2))

        tenants = [tenant.uuid]
        sips = sip_dao.find_all_by(language='en_US', tenant_uuids=tenants)
        assert_that(sips, all_of(has_items(sip1), not_(has_items(sip2))))


class TestGet(DAOTestCase):

    def test_given_no_rows_then_raises_error(self):
        self.assertRaises(NotFoundError, sip_dao.get, 1)

    def test_given_row_with_minimal_parameters_then_returns_model(self):
        row = self.add_usersip(
            name='username',
            secret='secret',
            type='friend',
            host='dynamic',
        )

        sip = sip_dao.get(row.id)
        assert_that(sip, has_properties(
            id=row.id,
            name='username',
            secret='secret',
            type='friend',
            host='dynamic',
        ))

    def test_given_row_with_optional_parameters_then_returns_model(self):
        row = self.add_usersip(language="fr_FR", amaflags="omit", buggymwi=1)

        sip = sip_dao.get(row.id)
        assert_that(sip.options, has_items(
            ["language", "fr_FR"],
            ["amaflags", "omit"],
            ["buggymwi", "yes"]
        ))

    def test_given_row_with_option_set_to_null_then_option_not_returned(self):
        row = self.add_usersip(language=None, allow=None, callerid='')

        sip = sip_dao.get(row.id)
        assert_that(sip.options, all_of(
            is_not(has_item(has_item("language"))),
            is_not(has_item(has_item("allow"))),
            is_not(has_item(has_item("callerid"))),
        ))

    def test_given_row_with_additional_options_then_returns_model(self):
        options = [
            ["foo", "bar"],
            ["foo", "baz"],
            ["spam", "eggs"]
        ]

        row = self.add_usersip(options=options)

        sip = sip_dao.get(row.id)
        assert_that(sip.options, has_items(*options))

    def test_given_row_has_native_and_additional_options_then_all_options_returned(self):
        row = self.add_usersip(language="fr_FR", _options=[["foo", "bar"]])

        sip = sip_dao.get(row.id)
        assert_that(sip.options, has_items(["language", "fr_FR"], ["foo", "bar"]))

    def test_get_multi_tenant(self):
        tenant = self.add_tenant()

        sip_row = self.add_usersip(tenant_uuid=tenant.uuid)
        sip = sip_dao.get(sip_row.id, tenant_uuids=[tenant.uuid])
        assert_that(sip, equal_to(sip_row))

        sip_row = self.add_usersip()
        self.assertRaises(
            NotFoundError,
            sip_dao.get, sip_row.id, tenant_uuids=[tenant.uuid],
        )


class TestSearch(DAOTestCase):

    def assert_search_returns_result(self, search_result, **parameters):
        result = sip_dao.search(**parameters)
        assert_that(result, equal_to(search_result))


class TestSimpleSearch(TestSearch):

    def test_given_no_sip_then_returns_no_empty_result(self):
        expected = SearchResult(0, [])

        self.assert_search_returns_result(expected)

    def test_given_on_sip_then_returns_one_result(self):
        sip = self.add_usersip()
        expected = SearchResult(1, [sip])

        self.assert_search_returns_result(expected)

    def test_search_multi_tenant(self):
        tenant = self.add_tenant()

        sip1 = self.add_usersip(name='sort1')
        sip2 = self.add_usersip(name='sort2', tenant_uuid=tenant.uuid)

        expected = SearchResult(2, [sip1, sip2])
        tenants = [tenant.uuid, self.default_tenant.uuid]
        self.assert_search_returns_result(expected, tenant_uuids=tenants)

        expected = SearchResult(1, [sip2])
        tenants = [tenant.uuid]
        self.assert_search_returns_result(expected, tenant_uuids=tenants)


class TestSearchMultiple(TestSearch):

    def setUp(self):
        super(TestSearch, self).setUp()
        self.sip1 = self.add_usersip(name='Ashton', host='resto')
        self.sip2 = self.add_usersip(name='Beaugarton', host='bar')
        self.sip3 = self.add_usersip(name='Casa', host='resto')
        self.sip4 = self.add_usersip(name='Dunkin', host='resto')

    def test_when_searching_then_returns_one_result(self):
        expected = SearchResult(1, [self.sip2])

        self.assert_search_returns_result(expected, search='eau')

    def test_when_searching_with_an_extra_argument(self):
        expected_resto = SearchResult(1, [self.sip1])
        self.assert_search_returns_result(expected_resto, search='ton', host='resto')

        expected_bar = SearchResult(1, [self.sip2])
        self.assert_search_returns_result(expected_bar, search='ton', host='bar')

        expected_all_resto = SearchResult(3, [self.sip1, self.sip3, self.sip4])
        self.assert_search_returns_result(expected_all_resto, host='resto', order='username')

    def test_when_sorting_then_returns_result_in_ascending_order(self):
        expected = SearchResult(
            4, [self.sip1, self.sip2, self.sip3, self.sip4]
        )

        self.assert_search_returns_result(expected, order='username')

    def test_when_sorting_in_descending_order_then_returns_results_in_descending_order(self):
        expected = SearchResult(
            4, [self.sip4, self.sip3, self.sip2, self.sip1]
        )

        self.assert_search_returns_result(expected, order='username', direction='desc')

    def test_when_limiting_then_returns_right_number_of_items(self):
        expected = SearchResult(4, [self.sip1])

        self.assert_search_returns_result(expected, limit=1)

    def test_when_offset_then_returns_right_number_of_items(self):
        expected = SearchResult(4, [self.sip2, self.sip3, self.sip4])

        self.assert_search_returns_result(expected, offset=1)

    def test_when_doing_a_paginated_search_then_returns_a_paginated_result(self):
        expected = SearchResult(3, [self.sip2])

        self.assert_search_returns_result(
            expected,
            search='a',
            order='username',
            direction='desc',
            offset=1,
            limit=1,
        )


class TestCreate(DAOTestCase):

    def test_create_minimal_parameters(self):
        sip_model = SIPEndpoint(tenant_uuid=self.default_tenant.uuid)

        sip = sip_dao.create(sip_model)

        self.session.expire_all()
        assert_that(inspect(sip).persistent)
        assert_that(sip, has_properties(
            id=not_none(),
            name=has_length(8),
            username=sip.name,
            secret=has_length(8),
            type='friend',
            host='dynamic',
            category='user',
        ))

    def test_create_predefined_parameters(self):
        sip_model = SIPEndpoint(
            tenant_uuid=self.default_tenant.uuid,
            name='myusername',
            secret='mysecret',
            host="127.0.0.1",
            type="peer",
        )

        sip = sip_dao.create(sip_model)

        self.session.expire_all()
        assert_that(inspect(sip).persistent)
        assert_that(sip, has_properties(
            id=not_none(),
            tenant_uuid=self.default_tenant.uuid,
            name='myusername',
            username='myusername',
            secret='mysecret',
            type='peer',
            host='127.0.0.1',
            category='user',
        ))

    def test_create_with_native_options(self):
        sip_model = SIPEndpoint(tenant_uuid=self.default_tenant.uuid, options=ALL_OPTIONS)

        sip = sip_dao.create(sip_model)

        self.session.expire_all()
        assert_that(inspect(sip).persistent)
        assert_that(sip, has_properties({
            'id': not_none(),
            'options': has_items(*ALL_OPTIONS),

            'buggymwi': 1,
            'amaflags': 'default',
            'sendrpid': 'yes',
            'videosupport': 'yes',
            'maxcallbitrate': 1024,
            'session_minse': 10,
            'maxforwards': 1,
            'rtpholdtimeout': 15,
            'session_expires': 60,
            'ignoresdpversion': 1,
            'textsupport': 1,
            'unsolicited_mailbox': '1000@default',
            'fromuser': 'field-user',
            'useclientcode': 1,
            'call_limit': 1,
            'progressinband': 'yes',
            'transport': 'udp',
            'directmedia': 'update',
            'promiscredir': 1,
            'allowoverlap': 1,
            'dtmfmode': 'info',
            'language': 'fr_FR',
            'usereqphone': 1,
            'qualify': '500',
            'trustrpid': 1,
            'timert1': 1,
            'session_refresher': 'uas',
            'allowsubscribe': 1,
            'session_timers': 'originate',
            'busylevel': 1,
            'callcounter': 0,
            'callerid': '"cûstomcallerid" <1234>',
            'encryption': 1,
            'use_q850_reason': 1,
            'disallowed_methods': 'disallowsip',
            'rfc2833compensate': 1,
            'g726nonstandard': 1,
            'contactdeny': '127.0.0.1',
            'snom_aoc_enabled': 1,
            't38pt_udptl': 1,
            'subscribemwi': 0,
            'autoframing': 1,
            't38pt_usertpsource': 1,
            'fromdomain': 'field-domain',
            'allowtransfer': 1,
            'nat': 'force_rport,comedia',
            'contactpermit': '127.0.0.1',
            'rtpkeepalive': 15,
            'insecure': 'port',
            'permit': '127.0.0.1',
            'deny': '127.0.0.1',
            'timerb': 1,
            'rtptimeout': 15,
            'disallow': 'all',
            'allow': 'gsm',
            'accountcode': 'accountcode',
            'md5secret': 'abcdefg',
            'mohinterpret': 'mohinterpret',
            'vmexten': '1000',
            'callingpres': 1,
            'parkinglot': 700,
            'fullname': 'fullname',
            'defaultip': '127.0.0.1',
            'qualifyfreq': 5000,
            'regexten': 'regexten',
            'cid_number': '0123456789',
            'callbackextension': '0123456789',
            'port': 10000,
            'outboundproxy': '127.0.0.1',
            'remotesecret': 'remotesecret',
        }))

    def test_create_with_additional_options(self):
        options = [
            ["language", "fr_FR"],
            ["foo", "bar"],
            ["foo", "baz"],
            ["spam", "eggs"]
        ]

        sip_model = SIPEndpoint(tenant_uuid=self.default_tenant.uuid, options=options)
        sip = sip_dao.create(sip_model)

        self.session.expire_all()
        assert_that(inspect(sip).persistent)
        assert_that(sip, has_properties(
            options=has_items(*options)
        ))


class TestEdit(DAOTestCase):

    def test_edit_basic_parameters(self):
        sip = self.add_usersip()

        self.session.expire_all()
        sip.name = 'username'
        sip.secret = 'secret'
        sip.type = 'peer'
        sip.host = '127.0.0.1'

        sip_dao.edit(sip)

        self.session.expire_all()
        assert_that(sip, has_properties(
            name='username',
            secret='secret',
            type='peer',
            host='127.0.0.1',
        ))

    def test_edit_remove_options(self):
        sip = self.add_usersip(options=ALL_OPTIONS)

        self.session.expire_all()
        sip.options = []

        sip_dao.edit(sip)

        self.session.expire_all()
        assert_that(sip, has_properties({
            'buggymwi': none(),
            'md5secret': '',
            'amaflags': 'default',
            'sendrpid': none(),
            'videosupport': none(),
            'maxcallbitrate': none(),
            'session_minse': none(),
            'maxforwards': none(),
            'rtpholdtimeout': none(),
            'session_expires': none(),
            'ignoresdpversion': none(),
            'textsupport': none(),
            'unsolicited_mailbox': none(),
            'fromuser': none(),
            'useclientcode': none(),
            'call_limit': 10,
            'progressinband': none(),
            'transport': none(),
            'directmedia': none(),
            'promiscredir': none(),
            'allowoverlap': none(),
            'dtmfmode': none(),
            'language': none(),
            'usereqphone': none(),
            'qualify': none(),
            'trustrpid': none(),
            'timert1': none(),
            'session_refresher': none(),
            'allowsubscribe': none(),
            'session_timers': none(),
            'busylevel': none(),
            'callcounter': none(),
            'callerid': none(),
            'encryption': none(),
            'use_q850_reason': none(),
            'disallowed_methods': none(),
            'rfc2833compensate': none(),
            'g726nonstandard': none(),
            'contactdeny': none(),
            'snom_aoc_enabled': none(),
            't38pt_udptl': none(),
            'subscribemwi': 0,
            'autoframing': none(),
            't38pt_usertpsource': none(),
            'fromdomain': none(),
            'allowtransfer': none(),
            'nat': none(),
            'contactpermit': none(),
            'rtpkeepalive': none(),
            'insecure': none(),
            'permit': none(),
            'deny': none(),
            'timerb': none(),
            'rtptimeout': none(),
            'disallow': none(),
            'allow': none(),
            'accountcode': none(),
            'md5secret': '',
            'mohinterpret': none(),
            'vmexten': none(),
            'callingpres': none(),
            'parkinglot': none(),
            'fullname': none(),
            'defaultip': none(),
            'qualifyfreq': none(),
            'regexten': none(),
            'cid_number': none(),
            'callbackextension': none(),
            'port': none(),
            'outboundproxy': none(),
            'remotesecret': none(),
            '_options': empty(),
        }))

    def test_edit_options(self):
        sip = self.add_usersip(
            language="fr_FR",
            amaflags="default",
            subscribemwi=1,
            allow="g729,gsm"
        )

        self.session.expire_all()
        sip.options = [
            ["language", "en_US"],
            ["amaflags", "omit"],
            ["subscribemwi", "no"],
            ["allow", "ulaw,alaw"],
        ]

        sip_dao.edit(sip)

        self.session.expire_all()
        assert_that(sip, has_properties(
            language='en_US',
            amaflags='omit',
            subscribemwi=0,
            allow='ulaw,alaw',
        ))

    def test_edit_additional_options(self):
        sip = self.add_usersip(_options=[
            ["foo", "bar"],
            ["foo", "baz"],
            ["spam", "eggs"],
        ])

        self.session.expire_all()
        sip.options = [
            ["foo", "newbar"],
            ["foo", "newbaz"],
            ["spam", "neweggs"],
        ]

        sip_dao.edit(sip)

        self.session.expire_all()
        assert_that(sip._options, has_items(
            ["foo", "newbar"],
            ["foo", "newbaz"],
            ["spam", "neweggs"],
        ))

    def test_edit_both_native_and_additional_options(self):
        sip = self.add_usersip(
            language="fr_FR",
            amaflags="default",
            subscribemwi=1,
            allow="g729,gsm",
            _options=[
                ["foo", "bar"],
                ["foo", "baz"],
                ["spam", "eggs"],
            ]
        )

        new_options = [
            ["language", "en_US"],
            ["amaflags", "omit"],
            ["subscribemwi", "no"],
            ["allow", "ulaw,alaw"],
            ["foo", "newbar"],
            ["foo", "newbaz"],
            ["spam", "neweggs"],
        ]

        self.session.expire_all()
        sip.options = new_options
        sip_dao.edit(sip)

        self.session.expire_all()
        assert_that(sip, has_properties(
            options=has_items(*new_options),
            language='en_US',
            amaflags='omit',
            subscribemwi=0,
            allow='ulaw,alaw',
            _options=has_items(
                ["foo", "newbar"],
                ["foo", "newbaz"],
                ["spam", "neweggs"],
            )
        ))


class TestDelete(DAOTestCase):

    def test_delete(self):
        sip = self.add_usersip()

        sip_dao.delete(sip)

        assert_that(inspect(sip).deleted)

    def test_given_endpoint_is_associated_to_line_then_line_is_dissociated(self):
        sip = self.add_usersip()
        line = self.add_line(endpoint_sip_id=sip.id)

        sip_dao.delete(sip)

        assert_that(line.endpoint_sip_id, none())


class TestRelations(DAOTestCase):

    def test_trunk_relationship(self):
        sip = self.add_usersip()
        trunk = self.add_trunk()

        trunk.associate_endpoint(sip)
        self.session.flush()

        self.session.expire_all()
        assert_that(sip.trunk, equal_to(trunk))

    def test_line_relationship(self):
        sip = self.add_usersip()
        line = self.add_line()

        line.associate_endpoint(sip)
        self.session.flush()

        self.session.expire_all()
        assert_that(sip.line, equal_to(line))
