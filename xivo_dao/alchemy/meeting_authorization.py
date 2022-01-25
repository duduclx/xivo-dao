# -*- coding: utf-8 -*-
# Copyright 2021-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from sqlalchemy import text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.types import (
    DateTime,
    Text
)
from xivo_dao.helpers.db_manager import Base


def utcnow_with_tzinfo():
    from datetime import datetime
    try:
        from datetime import timezone
        return datetime.now(timezone.utc)
    except ImportError:
        # NOTE: Python2 this is unused anyway
        return datetime.now()


class MeetingAuthorization(Base):

    __tablename__ = 'meeting_authorization'

    uuid = Column(UUID(as_uuid=True), server_default=text('uuid_generate_v4()'), primary_key=True)
    guest_uuid = Column(UUID(as_uuid=True), nullable=False)
    meeting_uuid = Column(UUID(as_uuid=True), ForeignKey('meeting.uuid', ondelete='CASCADE'), nullable=False)
    guest_name = Column(Text)
    status = Column(Text)
    created_at = Column(DateTime(timezone=True), default=utcnow_with_tzinfo, server_default=text("(now() at time zone 'utc')"))

    meeting = relationship(
        'Meeting',
        primaryjoin='Meeting.uuid == MeetingAuthorization.meeting_uuid',
        foreign_keys='MeetingAuthorization.meeting_uuid',
        viewonly=True,
    )
    guest_endpoint_sip = relationship(
        'EndpointSIP',
        secondary='meeting',
        secondaryjoin='EndpointSIP.uuid == Meeting.guest_endpoint_sip_uuid',
        primaryjoin='MeetingAuthorization.meeting_uuid == Meeting.uuid',
        viewonly=True,
        uselist=False,
    )
