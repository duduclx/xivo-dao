# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 Avencall
# Copyright (C) 2016 Proformatique Inc.
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
from sqlalchemy.schema import Column, PrimaryKeyConstraint
from sqlalchemy.types import Integer, String, Enum

from xivo_dao.helpers.db_manager import Base


class Callerid(Base):

    __tablename__ = 'callerid'
    __table_args__ = (
        PrimaryKeyConstraint('type', 'typeval'),
    )

    mode = Column(Enum('prepend', 'overwrite', 'append',
                       name='callerid_mode',
                       metadata=Base.metadata))
    callerdisplay = Column(String(80), nullable=False, server_default='')
    type = Column(Enum('callfilter', 'incall', 'group', 'queue',
                       name='callerid_type',
                       metadata=Base.metadata))
    typeval = Column(Integer, nullable=False, autoincrement=False)

    @hybrid_property
    def name(self):
        if self.callerdisplay == '':
            return None
        return self.callerdisplay

    @name.setter
    def name(self, value):
        if value is None:
            self.callerdisplay = ''
        else:
            self.callerdisplay = value
