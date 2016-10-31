# -*- coding: utf-8 -*-

# Copyright (C) 2012-2014 Avencall
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

from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Text

from xivo_dao.helpers.db_manager import Base


class Context(Base):

    __tablename__ = 'context'
    __table_args__ = (
        PrimaryKeyConstraint('id'),
        UniqueConstraint('name'),
    )

    id = Column(Integer)
    name = Column(String(39), nullable=False)
    displayname = Column(String(128))
    entity = Column(String(64))
    contexttype = Column(String(40), nullable=False, server_default='internal')
    commented = Column(Integer, nullable=False, server_default='0')
    description = Column(Text)
