# -*- coding: utf-8 -*-

# Copyright (C) 2012-2016 Avencall
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
from sqlalchemy.types import Integer, String

from xivo_dao.helpers.db_manager import Base


class CtiMain(Base):

    __tablename__ = 'ctimain'

    id = Column(Integer, primary_key=True)
    ctis_active = Column(Integer, nullable=False, server_default='1')
    tlscertfile = Column(String(128))
    tlsprivkeyfile = Column(String(128))
    context_separation = Column(Integer)
    live_reload_conf = Column(Integer)
