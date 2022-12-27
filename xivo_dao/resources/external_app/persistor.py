# Copyright 2020-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_dao.alchemy.external_app import ExternalApp
from xivo_dao.helpers.persistor import BasePersistor
from xivo_dao.resources.utils.search import CriteriaBuilderMixin


class ExternalAppPersistor(CriteriaBuilderMixin, BasePersistor):

    _search_table = ExternalApp

    def __init__(self, session, external_app_search, tenant_uuids=None):
        self.session = session
        self.search_system = external_app_search
        self.tenant_uuids = tenant_uuids

    def _find_query(self, criteria):
        query = self.session.query(ExternalApp)
        query = self._filter_tenant_uuid(query)
        return self.build_criteria(query, criteria)

    def _search_query(self):
        return self.session.query(self.search_system.config.table)
