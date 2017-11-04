# -*- coding: UTF-8 -*-

# Copyright 2016 The Wazo Authors  (see the AUTHORS file)
#
# SPDX-License-Identifier: GPL-3.0+

from xivo_dao.alchemy.conference import Conference
from xivo_dao.alchemy.dialaction import Dialaction

from xivo_dao.helpers import errors
from xivo_dao.resources.utils.search import SearchResult, CriteriaBuilderMixin


class ConferencePersistor(CriteriaBuilderMixin):

    _search_table = Conference

    def __init__(self, session, conference_search):
        self.session = session
        self.conference_search = conference_search

    def find_by(self, criteria):
        query = self._find_query(criteria)
        return query.first()

    def _find_query(self, criteria):
        query = self.session.query(Conference)
        return self.build_criteria(query, criteria)

    def get_by(self, criteria):
        conference = self.find_by(criteria)
        if not conference:
            raise errors.not_found('Conference', **criteria)
        return conference

    def find_all_by(self, criteria):
        query = self._find_query(criteria)
        return query.all()

    def search(self, parameters):
        rows, total = self.conference_search.search(self.session, parameters)
        return SearchResult(total, rows)

    def create(self, conference):
        self.session.add(conference)
        self.session.flush()
        return conference

    def edit(self, conference):
        self.session.add(conference)
        self.session.flush()

    def delete(self, conference):
        self._delete_associations(conference)
        self.session.delete(conference)
        self.session.flush()

    def _delete_associations(self, conference):
        # "unlink" dialactions that points on this Conference
        (self.session.query(Dialaction)
         .filter(Dialaction.action == 'conference')
         .filter(Dialaction.actionarg1 == str(conference.id))
         .update({'linked': 0}))
