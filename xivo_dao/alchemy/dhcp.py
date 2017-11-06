# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 Avencall
#
# SPDX-License-Identifier: GPL-3.0+

from sqlalchemy.schema import Column, PrimaryKeyConstraint
from sqlalchemy.types import Integer, String

from xivo_dao.helpers.db_manager import Base


class Dhcp(Base):

    __tablename__ = 'dhcp'
    __table_args__ = (
        PrimaryKeyConstraint('id'),
    )

    id = Column(Integer, nullable=False)
    active = Column(Integer, nullable=False, server_default='0')
    pool_start = Column(String(64), nullable=False, server_default='')
    pool_end = Column(String(64), nullable=False, server_default='')
    extra_ifaces = Column(String(255), nullable=False, server_default='')
