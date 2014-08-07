# -*- coding: utf8 -*-
import time
import sys, string
import os, re
import MySQLdb.cursors
import ConfigParser


class GetDB:
    #获取数据库连接
    def getDBconn(self):
        try:
            cf = ConfigParser.ConfigParser()
            cf.read("config.conf")
            host_value = cf.get("db", "host")
            port_value = cf.get("db", "port")
            dbname_value = cf.get("db", "dbname")
            dbuser_value = cf.get("db", "dbuser")
            dbpasswd_value = cf.get("db", "dbpasswd")
            conn = MySQLdb.connect(host=host_value,port=int(port_value),user=dbuser_value,passwd=dbpasswd_value,db=dbname_value,charset='utf8')
            return conn
        except Exception, e:
            print e
            sys.exit()
