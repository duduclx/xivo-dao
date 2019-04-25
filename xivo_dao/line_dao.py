# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_dao.alchemy.linefeatures import LineFeatures
from xivo_dao.alchemy.line_extension import LineExtension
from xivo_dao.alchemy.user_line import UserLine
from xivo_dao.alchemy.extension import Extension as ExtensionTable
from xivo_dao.helpers.db_manager import daosession


@daosession
def get_interface_from_exten_and_context(session, extension, context):
    res = (session
           .query(LineFeatures.protocol,
                  LineFeatures.name,
                  UserLine.main_line)
           .join(LineExtension, LineExtension.line_id == LineFeatures.id)
           .join(ExtensionTable, LineExtension.extension_id == ExtensionTable.id)
           .outerjoin(UserLine, UserLine.line_id == LineFeatures.id)
           .filter(ExtensionTable.exten == extension)
           .filter(ExtensionTable.context == context))

    interface = None
    for row in res.all():
        interface = _format_interface(row.protocol, row.name)
        if row.main_line:
            return interface

    if not interface:
        raise LookupError('no line with extension %s and context %s' % (extension, context))

    return interface


def _format_interface(protocol, name):
    if protocol == 'custom':
        return name
    else:
        return '%s/%s' % (protocol.upper(), name)
