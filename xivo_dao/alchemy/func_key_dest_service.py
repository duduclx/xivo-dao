# -*- coding: utf-8 -*-

# Copyright (C) 2014 Avencall
#
# SPDX-License-Identifier: GPL-3.0+

from xivo_dao.alchemy.extension import Extension
from xivo_dao.alchemy.func_key import FuncKey
from xivo_dao.helpers.db_manager import Base

from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKeyConstraint, CheckConstraint, PrimaryKeyConstraint
from sqlalchemy.types import Integer


class FuncKeyDestService(Base):

    __tablename__ = 'func_key_dest_service'
    __table_args__ = (
        PrimaryKeyConstraint('func_key_id', 'destination_type_id', 'extension_id'),
        ForeignKeyConstraint(['func_key_id', 'destination_type_id'],
                             ['func_key.id', 'func_key.destination_type_id']),
        ForeignKeyConstraint(['extension_id'],
                             ['extensions.id']),
        CheckConstraint('destination_type_id = 5')
    )

    func_key_id = Column(Integer)
    destination_type_id = Column(Integer, server_default="5")
    extension_id = Column(Integer)

    func_key = relationship(FuncKey)
    extension = relationship(Extension)
