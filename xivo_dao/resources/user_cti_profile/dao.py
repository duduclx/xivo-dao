# -*- coding: utf-8 -*-
#
# Copyright 2013-2017 The Wazo Authors  (see the AUTHORS file)
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

from xivo_dao.helpers.db_utils import flush_session
from xivo_dao.helpers.db_manager import daosession
from xivo_dao.alchemy.userfeatures import UserFeatures as UserSchema
from xivo_dao.alchemy.cti_profile import CtiProfile
from xivo_dao.helpers import errors


@daosession
def find_profile_by_userid(session, userid):
    user = session.query(UserSchema).filter(UserSchema.id == userid).first()
    if user is None:
        raise errors.not_found('User', id=userid)
    if user.cti_profile_id is None:
        return None
    query = session.query(CtiProfile).filter(CtiProfile.id == user.cti_profile_id)
    return query.first()


@daosession
def edit(session, user_cti_profile):
    with flush_session(session):
        user = (session.query(UserSchema)
                .filter(UserSchema.id == user_cti_profile.user_id)
                .first())
        if user_cti_profile.enabled is not None:
            user.enableclient = 1 if user_cti_profile.enabled else 0
        if user_cti_profile.cti_profile_id is not None:
            user.cti_profile_id = user_cti_profile.cti_profile_id
        session.add(user)
