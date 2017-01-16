# -*- coding: utf-8 -*-

# Copyright 2007-2017 The Wazo Authors  (see the AUTHORS file)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, PrimaryKeyConstraint
from sqlalchemy.sql import cast, not_
from sqlalchemy.sql.schema import ForeignKeyConstraint
from sqlalchemy.types import Integer, String, Text, Boolean

from xivo_dao.alchemy import enum
from xivo_dao.alchemy.entity import Entity
from xivo_dao.helpers.db_manager import Base, IntAsString


class Schedule(Base):

    __tablename__ = 'schedule'
    __table_args__ = (
        PrimaryKeyConstraint('id'),
        ForeignKeyConstraint(('entity_id',),
                             ('entity.id',),
                             ondelete='RESTRICT'),
    )

    id = Column(Integer, nullable=False)
    entity_id = Column(Integer)
    name = Column(String(255))
    timezone = Column(String(128))
    fallback_action = Column(enum.dialaction_action, nullable=False, server_default='none')
    fallback_actionid = Column(IntAsString(255))
    fallback_actionargs = Column(String(255))
    description = Column(Text)
    commented = Column(Integer, nullable=False, server_default='0')

    entity = relationship(Entity)

    periods = relationship('ScheduleTime',
                           primaryjoin='ScheduleTime.schedule_id == Schedule.id',
                           foreign_keys='ScheduleTime.schedule_id',
                           cascade='all, delete-orphan')

    @property
    def open_periods(self):
        return self._get_periods('opened')

    @open_periods.setter
    def open_periods(self, value):
        self._set_periods('opened', value)

    @property
    def exceptional_periods(self):
        return self._get_periods('closed')

    @exceptional_periods.setter
    def exceptional_periods(self, value):
        self._set_periods('closed', value)

    def _get_periods(self, mode):
        return [period for period in self.periods if period.mode == mode]

    def _set_periods(self, mode, periods):
        self.periods = [period for period in self.periods if period.mode != mode]
        for period in periods:
            period.mode = mode
            self.periods.append(period)

    @property
    def closed_destination(self):
        return self

    @property
    def type(self):
        return self.fallback_action.split(':', 1)[0] if self.fallback_action else self.fallback_action

    @type.setter
    def type(self, value):
        type_ = value if value else ''
        subtype = self.subtype if self.subtype else ''
        self._set_fallback_action(type_, subtype)

    @property
    def subtype(self):
        type_subtype = self.fallback_action.split(':', 1) if self.fallback_action else ''
        return type_subtype[1] if len(type_subtype) == 2 else None

    @subtype.setter
    def subtype(self, value):
        type_ = self.type if self.type else ''
        subtype = value if value else ''
        self._set_fallback_action(type_, subtype)

    def _set_fallback_action(self, type_, subtype):
        subtype = ':{}'.format(subtype) if subtype else ''
        self.fallback_action = '{}{}'.format(type_, subtype)

    @hybrid_property
    def actionarg1(self):
        return self.fallback_actionid

    @actionarg1.setter
    def actionarg1(self, value):
        self.fallback_actionid = value

    @hybrid_property
    def actionarg2(self):
        return self.fallback_actionargs

    @actionarg2.setter
    def actionarg2(self, value):
        self.fallback_actionargs = value

    @hybrid_property
    def enabled(self):
        return self.commented == 0

    @enabled.expression
    def enabled(cls):
        return not_(cast(cls.commented, Boolean))

    @enabled.setter
    def enabled(self, value):
        self.commented = int(value == 0)
