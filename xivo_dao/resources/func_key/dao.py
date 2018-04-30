# -*- coding: utf-8 -*-
# Copyright 2014-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from xivo_dao.alchemy.extension import Extension
from xivo_dao.alchemy.func_key_dest_forward import FuncKeyDestForward
from xivo_dao.alchemy.func_key_mapping import FuncKeyMapping
from xivo_dao.alchemy.userfeatures import UserFeatures
from xivo_dao.helpers.db_manager import daosession
from xivo_dao.resources.func_key.model import ForwardTypeConverter


@daosession
def find_all_forwards(session, user_id, fwd_type):
    type_converter = ForwardTypeConverter()

    query = (
        session.query(FuncKeyDestForward.number.label('number'))
        .join(Extension,
              FuncKeyDestForward.extension_id == Extension.id)
        .join(FuncKeyMapping,
              FuncKeyMapping.func_key_id == FuncKeyDestForward.func_key_id)
        .join(UserFeatures,
              UserFeatures.func_key_private_template_id == FuncKeyMapping.template_id)
        .filter(UserFeatures.id == user_id)
        .filter(Extension.typeval == type_converter.model_to_db(fwd_type))
    )
    return query.all()
