# Copyright 2021-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import (
    assert_that,
    instance_of,
    calling,
    not_,
    raises,
    equal_to,
    has_items,
)
from sqlalchemy import select, Table, Column, Integer
from sqlalchemy.exc import InvalidRequestError

from xivo_dao.tests.test_dao import DAOTestCase
from xivo_dao.helpers.db_manager import Base
from xivo_dao.helpers.db_views import MaterializedView, create_materialized_view


class TestCreateMaterializedView(DAOTestCase):
    def test_create_materialized_view(self):
        result = create_materialized_view('test', select([1]))
        assert_that(result, instance_of(tuple))
        assert_that(result, has_items(instance_of(Table), instance_of(list)))

    def test_create_materialized_view_with_no_name(self):
        assert_that(
            calling(create_materialized_view).with_args(None, select([1])),
            raises(ValueError)
        )

    def test_create_materialized_view_with_no_selectable(self):
        assert_that(
            calling(create_materialized_view).with_args('testview', None),
            raises(ValueError)
        )

    def test_create_materialized_view_with_invalid_selectable(self):
        assert_that(
            calling(create_materialized_view).with_args('testview', 'invalid'),
            raises(ValueError)
        )

    def test_create_materialized_view_with_invalid_dependencies(self):
        assert_that(
            calling(create_materialized_view).with_args(
                'testview', select([1]), dependencies=[object]
            ),
            raises(ValueError)
        )

    def test_create_materialized_view_with_invalid_indexes(self):
        assert_that(
            calling(create_materialized_view).with_args(
                'testview', select([1]), indexes=[object()]
            ),
            raises(ValueError)
        )


class TestMaterializedView(DAOTestCase):
    def _create_view_class(
        self, func, name=None, selectable=None, dependencies=None, indexes=None
    ):
        class _(MaterializedView):
            __view__ = (
                func(name, selectable, dependencies=dependencies, indexes=indexes)
                if callable(func)
                else func
            )

        return _

    def test_view_init_table(self):
        assert_that(
            calling(self._create_view_class).with_args(
                create_materialized_view, name='test', selectable=select([1])
            ),
            not_(raises(InvalidRequestError)),
        )

    def test_view_class_creation(self):
        view = self._create_view_class(create_materialized_view, "view", select([1]))
        assert_that(issubclass(view, MaterializedView), equal_to(True))

    def test_view_init_with_none(self):
        assert_that(
            calling(self._create_view_class).with_args(None),
            raises(InvalidRequestError),
        )

    def test_view_without_helper_function(self):
        def some_func(name, selectable, dependencies=None, indexes=None):
            return "bad return"

        assert_that(
            calling(self._create_view_class).with_args(some_func, "view", select([1])),
            raises(InvalidRequestError)
        )

    def test_view_init_with_invalid_view(self):
        assert_that(
            calling(self._create_view_class).with_args((None, None)),
            raises(InvalidRequestError),
        )

    def test_view_init_without_view_attribute(self):
        def _create_class():
            class _(MaterializedView):
                pass

            return _

        assert_that(calling(_create_class), raises(InvalidRequestError))

    def test_view_dependencies_event_correctly_bound(self):
        class MockModel(Base):
            __tablename__ = 'mock_model'
            id = Column(Integer, primary_key=True)

        view = self._create_view_class(
            create_materialized_view, "view", select([1]), dependencies=[MockModel]
        )
        assert_that(view.autorefresh, equal_to(True))

    def test_view_dependencies_no_event_bound(self):
        view = self._create_view_class(create_materialized_view, "view", select([1]))
        assert_that(view.autorefresh, equal_to(False))
