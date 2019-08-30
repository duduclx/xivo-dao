# -*- coding: utf-8 -*-
# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_dao.alchemy.accessfeatures import AccessFeatures
from xivo_dao.resources.utils.search import SearchSystem
from xivo_dao.resources.utils.search import SearchConfig


config = SearchConfig(
    table=AccessFeatures,
    columns={
        'id': AccessFeatures.id,
        'host': AccessFeatures.host,
        'feature': AccessFeatures.feature,
        'commented': AccessFeatures.commented,
    },
    default_sort='host',
)

access_feature_search = SearchSystem(config)
