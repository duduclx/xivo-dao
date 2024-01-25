# Copyright 2017-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_dao.alchemy.moh import MOH
from xivo_dao.resources.utils.search import SearchSystem, SearchConfig


config = SearchConfig(
    table=MOH, columns={'name': MOH.name, 'label': MOH.label}, default_sort='label'
)

moh_search = SearchSystem(config)
