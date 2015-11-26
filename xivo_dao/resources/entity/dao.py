# -*- coding: utf-8 -*-

# Copyright (C) 2014 Avencall
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

from xivo_dao.alchemy.entity import Entity as EntitySchema
from xivo_dao.helpers.db_manager import daosession


@daosession
def default_entity_name(session):
    return session.execute(EntitySchema.query_default_name()).scalar()


@daosession
def default_entity_id(session):
    return session.execute(EntitySchema.query_default_id()).scalar()
