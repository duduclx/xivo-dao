# -*- coding: utf-8 -*-
# Copyright 2015-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from xivo_dao.helpers.db_manager import daosession

from .persistor import QueuePersistor
from .search import queue_search


@daosession
def search(session, **parameters):
    return QueuePersistor(session, queue_search).search(parameters)


@daosession
def get(session, queue_id):
    return QueuePersistor(session, queue_search).get_by({'id': queue_id})


@daosession
def get_by(session, **criteria):
    return QueuePersistor(session, queue_search).get_by(criteria)


@daosession
def find(session, queue_id):
    return QueuePersistor(session, queue_search).find_by({'id': queue_id})


@daosession
def find_by(session, **criteria):
    return QueuePersistor(session, queue_search).find_by(criteria)


@daosession
def find_all_by(session, **criteria):
    return QueuePersistor(session, queue_search).find_all_by(criteria)


@daosession
def create(session, queue):
    return QueuePersistor(session, queue_search).create(queue)


@daosession
def edit(session, queue):
    QueuePersistor(session, queue_search).edit(queue)


@daosession
def delete(session, queue):
    QueuePersistor(session, queue_search).delete(queue)


@daosession
def associate_schedule(session, queue, schedule):
    QueuePersistor(session, queue_search).associate_schedule(queue, schedule)


@daosession
def dissociate_schedule(session, queue, schedule):
    QueuePersistor(session, queue_search).dissociate_schedule(queue, schedule)


@daosession
def associate_member_user(session, queue, member):
    QueuePersistor(session, queue_search).associate_member_user(queue, member)


@daosession
def dissociate_member_user(session, queue, member):
    QueuePersistor(session, queue_search).dissociate_member_user(queue, member)


@daosession
def associate_member_agent(session, queue, member):
    QueuePersistor(session, queue_search).associate_member_agent(queue, member)


@daosession
def dissociate_member_agent(session, queue, member):
    QueuePersistor(session, queue_search).dissociate_member_agent(queue, member)
