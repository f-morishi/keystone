# Copyright 2014 IBM Corp.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import sqlalchemy as sql

from keystone.common.sql import migration_helpers


def upgrade(migrate_engine):
    try:
        extension_version = migration_helpers.get_db_version(
            extension='endpoint_policy',
            engine=migrate_engine)
    except Exception:
        extension_version = 0

    # This migration corresponds to endpoint_policy extension migration 1. Only
    # update if it has not been run.
    if extension_version >= 1:
        return

    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta = sql.MetaData()
    meta.bind = migrate_engine

    endpoint_policy_table = sql.Table(
        'policy_association',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('policy_id', sql.String(64),
                   nullable=False),
        sql.Column('endpoint_id', sql.String(64),
                   nullable=True),
        sql.Column('service_id', sql.String(64),
                   nullable=True),
        sql.Column('region_id', sql.String(64),
                   nullable=True),
        sql.UniqueConstraint('endpoint_id', 'service_id', 'region_id'),
        mysql_engine='InnoDB',
        mysql_charset='utf8')

    endpoint_policy_table.create(migrate_engine, checkfirst=True)
