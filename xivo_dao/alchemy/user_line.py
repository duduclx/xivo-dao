# Copyright 2013-2023 The Wazo Authors  (see the AUTHORS file)
# Copyright (C) 2016 Proformatique Inc.
# SPDX-License-Identifier: GPL-3.0-or-later

from sqlalchemy.types import Integer, Boolean
from sqlalchemy.schema import Column, ForeignKey, Index, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from xivo_dao.helpers.db_manager import Base


class UserLine(Base):

    __tablename__ = 'user_line'
    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'line_id'),
        Index('user_line__idx__user_id', 'user_id'),
        Index('user_line__idx__line_id', 'line_id'),
    )

    user_id = Column(Integer, ForeignKey('userfeatures.id'), nullable=False)
    line_id = Column(Integer, ForeignKey('linefeatures.id'), nullable=False)
    main_user = Column(Boolean, nullable=False)
    main_line = Column(Boolean, nullable=False)

    linefeatures = relationship("LineFeatures")
    userfeatures = relationship("UserFeatures")

    main_user_rel = relationship("UserFeatures",
                                 primaryjoin="""and_(UserLine.user_id == UserFeatures.id,
                                 UserLine.main_user == True)"""
                                 )

    main_line_rel = relationship("LineFeatures",
                                 primaryjoin="""and_(UserLine.line_id == LineFeatures.id,
                                 UserLine.main_line == True)"""
                                 )

    user = relationship('UserFeatures',
                        back_populates='user_lines')

    line = relationship('LineFeatures',
                        back_populates='user_lines')
