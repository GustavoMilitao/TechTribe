# SPDX-FileCopyrightText: 2023 
#
# SPDX-License-Identifier: MPL-2.0


import databases
import sqlalchemy

from techtribe.config import settings

settings = settings()

database = databases.Database(settings.db_url)
metadata = sqlalchemy.MetaData()
