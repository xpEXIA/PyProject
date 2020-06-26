# 更改Django数据库链接方法
import pymysql
pymysql.version_info=(1,3,13,"final",0)
pymysql.install_as_MySQLdb()