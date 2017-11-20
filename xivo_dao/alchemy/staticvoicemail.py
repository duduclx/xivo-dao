# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# SPDX-License-Identifier: GPL-3.0+

from sqlalchemy.schema import Column, PrimaryKeyConstraint, Index
from sqlalchemy.types import Integer, String, Text

from xivo_dao.helpers.db_manager import Base


class StaticVoicemail(Base):

    __tablename__ = 'staticvoicemail'
    __table_args__ = (
        PrimaryKeyConstraint('id'),
        Index('staticvoicemail__idx__category', 'category')
    )

    id = Column(Integer, nullable=False)
    cat_metric = Column(Integer, nullable=False, server_default='0')
    var_metric = Column(Integer, nullable=False, server_default='0')
    commented = Column(Integer, nullable=False, server_default='0')
    filename = Column(String(128), nullable=False)
    category = Column(String(128), nullable=False)
    var_name = Column(String(128), nullable=False)
    var_val = Column(Text)
