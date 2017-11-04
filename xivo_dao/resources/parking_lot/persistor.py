# -*- coding: UTF-8 -*-

# Copyright 2016 The Wazo Authors  (see the AUTHORS file)
#
# SPDX-License-Identifier: GPL-3.0+

from xivo_dao.alchemy.parking_lot import ParkingLot

from xivo_dao.helpers import errors
from xivo_dao.resources.utils.search import SearchResult, CriteriaBuilderMixin


class ParkingLotPersistor(CriteriaBuilderMixin):

    _search_table = ParkingLot

    def __init__(self, session, parking_lot_search):
        self.session = session
        self.parking_lot_search = parking_lot_search

    def find_by(self, criteria):
        query = self._find_query(criteria)
        return query.first()

    def _find_query(self, criteria):
        query = self.session.query(ParkingLot)
        return self.build_criteria(query, criteria)

    def get_by(self, criteria):
        parking_lot = self.find_by(criteria)
        if not parking_lot:
            raise errors.not_found('ParkingLot', **criteria)
        return parking_lot

    def find_all_by(self, criteria):
        query = self._find_query(criteria)
        return query.all()

    def search(self, parameters):
        rows, total = self.parking_lot_search.search(self.session, parameters)
        return SearchResult(total, rows)

    def create(self, parking_lot):
        self.session.add(parking_lot)
        self.session.flush()
        return parking_lot

    def edit(self, parking_lot):
        self.session.add(parking_lot)
        self.session.flush()

    def delete(self, parking_lot):
        self.session.delete(parking_lot)
        self.session.flush()
