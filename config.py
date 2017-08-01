# -*- coding:utf-8 -*-
"""
======================
@author Vincent
@config file
config for database
======================
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from dbclient import DBClient

DBClients = DBClient()
ServersPort = 8005
Base = declarative_base()
EngineRead = create_engine('mysql://%s:%s@%s:%d/%s?charset=utf8' %
                       (DBClients.db.MySQLREAD.User, DBClients.db.MySQLREAD.Passwd,
                        DBClients.db.MySQLREAD.Host,DBClients.db.MySQLREAD.Port, DBClients.db.MySQLREAD.Dbname),
                       encoding='utf8', echo=False,
                       pool_size=100, pool_recycle=3600)
