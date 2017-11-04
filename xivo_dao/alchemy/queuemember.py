# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
# Copyright (C) 2016 Proformatique Inc.
#
# SPDX-License-Identifier: GPL-3.0+

from xivo_dao.helpers.db_manager import Base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import (Column,
                               Index,
                               PrimaryKeyConstraint,
                               UniqueConstraint)
from sqlalchemy.types import Integer, String, Enum


class QueueMember(Base):

    __tablename__ = 'queuemember'
    __table_args__ = (
        PrimaryKeyConstraint('queue_name', 'interface'),
        UniqueConstraint('queue_name', 'channel', 'usertype', 'userid', 'category'),
        Index('queuemember__idx__category', 'category'),
        Index('queuemember__idx__channel', 'channel'),
        Index('queuemember__idx__userid', 'userid'),
        Index('queuemember__idx__usertype', 'usertype'),
    )

    queue_name = Column(String(128))
    interface = Column(String(128))
    penalty = Column(Integer, nullable=False, server_default='0')
    commented = Column(Integer, nullable=False, server_default='0')
    usertype = Column(Enum('agent', 'user', name='queuemember_usertype', metadata=Base.metadata), nullable=False)
    userid = Column(Integer, nullable=False)
    channel = Column(String(25), nullable=False)
    category = Column(Enum('queue', 'group', name='queue_category', metadata=Base.metadata), nullable=False)
    position = Column(Integer, nullable=False, server_default='0')

    user = relationship('UserFeatures',
                        primaryjoin="""and_(QueueMember.usertype == 'user',
                                            QueueMember.userid == UserFeatures.id)""",
                        foreign_keys='QueueMember.userid')

    group = relationship('GroupFeatures',
                         primaryjoin="""and_(QueueMember.category == 'group',
                                             QueueMember.queue_name == GroupFeatures.name)""",
                         foreign_keys='QueueMember.queue_name')

    def _set_default_channel(self):
        if self.user and self.user.lines:
            main_line = self.user.lines[0]
            if main_line.endpoint_sip:
                self.channel = 'SIP'
            elif main_line.endpoint_sccp:
                self.channel = 'SCCP'
            elif main_line.endpoint_custom:
                self.channel = '**Unknown**'

    def fix(self):
        self._set_default_channel()
        if self.user and self.user.lines:
            main_line = self.user.lines[0]
            if main_line.endpoint_sip:
                self.interface = '{}/{}'.format(self.channel, main_line.endpoint_sip.name)

            elif main_line.endpoint_sccp:
                self.interface = '{}/{}'.format(self.channel, main_line.endpoint_sccp.name)

            elif main_line.endpoint_custom:
                self.interface = main_line.endpoint_custom.interface
