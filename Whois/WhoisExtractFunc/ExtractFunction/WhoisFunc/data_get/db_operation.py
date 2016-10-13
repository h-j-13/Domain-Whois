#!/usr/bin/python
# encoding:utf-8

#
# 数据库操作模块
# @author 王凯
#

import MySQLdb
import datetime
import ConfigParser
import threading
import static


logger = static.logger_db

class DataBase :
    # 数据库初始化
    def __init__(self):
        self.host = static.DB_HOST
        self.user = static.USERNAME
        self.passwd = static.PASSWORD
        self.charset = 'utf8'
        self.db_lock = threading.Lock() # 数据库操作锁

    # 执行连接数据库操作
    def get_connect(self):
        if self.db_lock.acquire():
            try:
                self.conn = MySQLdb.Connection(
                    host = self.host, user = self.user, passwd = self.passwd, charset = self.charset)
                self.cursor = self.conn.cursor()
            except MySQLdb.Error, e:
                logger.error('get_connect error_info: %d: %s' % (e.args[0], e.args[1]))
            self.db_lock.release()

    # 关闭数据库链接
    def db_close(self):
        if self.db_lock.acquire():
            try:
                self.conn.close()
            except MySQLdb.Error, e: 
                logger.error('db_close error_info: %d: %s' % (e.args[0], e.args[1]))
            self.db_lock.release()

    #　commit
    def db_commit(self):
        if self.db_lock.acquire():
            try:
                self.conn.commit()
            except MySQLdb.Error, e:  
                logger.error('db_commit error_info: %d: %s' % (e.args[0], e.args[1]))
            self.db_lock.release()
    
    # 数据库数据查找
    def db_select(self, **args):

        if args['nature'] == 'whois_addr': # 单条服务器地址查询
            sql = """SELECT addr, func, flag_finished FROM {TABLE_WHOIS_ADDR} WHERE tld = '{tld}'"""\
            .format(TABLE_WHOIS_ADDR = static.TABLE_WHOIS_ADDR, tld = args['tlds'])

        elif args['nature'] == 'domain_whois': # 域名whois信息查询
            table_whois = self.get_table_name(args['domain'].split('.')[0])
            sql = """SELECT domain, flag, domain_status, top_whois_server, sec_whois_server, reg_name, reg_phone,\
        reg_email, org_name, sponsoring_registrar, name_server, creation_date, expiration_date, updated_date, \
         insert_time, details, hash_value FROM {table_whois} WHERE domain = '{domain}'"""\
             .format(table_whois = table_whois, domain = args['domain'])

        elif args['nature'] == 'proxyIP': # 选择socket代理
            sql = """SELECT ip, port FROM {table_proxy} WHERE method = 1 and speed < 3"""\
            .format(table_proxy = static.TABLE_PROXY)

        elif args['nature'] == 'domains': # 获得初始导入域名, 从中提取出flag = -6的域名
            sql = """SELECT domain FROM {table_whois} WHERE flag = -6 limit {read_num}"""\
            .format(table_whois = args['table_whois'], read_num = static.READ_NUM)

        elif args['nature'] == 'whois_addr_table': # 获取整个whois_addr信息
            sql = """SELECT tld, addr FROM {table_whois_addr} WHERE flag_addr = 1""".format(
                table_whois_addr = static.TABLE_WHOIS_ADDR
                )
        elif args['nature'] == 'server_ip': # 获取whois_server_ip
            sql = """SELECT svr_name, ip, port_available FROM {TABLE_SVR_IP}""".format(TABLE_SVR_IP = static.TABLE_SVR_IP)
        else:
            return
        return self.__execute__(sql)

    # 数据库数据插入
    def db_insert(self, **args):

        sql = """INSERT INTO {table_whois}(domain, flag, domain_status, top_whois_server, sec_whois_server, reg_name, reg_phone,\
        reg_email, org_name, sponsoring_registrar, name_server, creation_date, expiration_date, updated_date, insert_time, details, hash_value) VALUES(\
        '{domain}', {flag}, '{domain_status}', '{top_whois_server}', '{sec_whois_server}', '{reg_name}', '{reg_phone}', '{reg_email}', '{org_name}',\
         '{sponsoring_registrar}', '{name_server}', '{creation_date}', '{expiration_date}', '{updated_date}', '{insert_time}', '{details}', {hash_value})"""\
        .format(
            table_whois = self.get_table_name(args['domain'].split('.')[0]),
            domain = args['domain'],
            flag = args['flag'],
            domain_status = args['domain_status'],
            top_whois_server = args['top_whois_server'],
            sec_whois_server = args['sec_whois_server'],
            reg_name = args['reg_name'],
            reg_phone = args['reg_phone'],
            reg_email = args['reg_email'],
            org_name = args['org_name'],
            creation_date = args['creation_date'],
            expiration_date = args['expiration_date'],
            updated_date = args['updated_date'],
            insert_time = args['insert_time'],
            details = args['details'],
            hash_value = args['hash_value'],
            sponsoring_registrar = args['sponsoring_registrar'],
            name_server = args['name_server'],
        )
        self.__execute__(sql)


    # whois数据更新
    def db_update(self, **args):

        table_whois = self.get_table_name(args['domain'].split('.')[0])
        sql = """UPDATE table_whois SET flag = {flag}, domain_status = '{domain_status}', top_whois_server = '{top_whois_server}', \
        sec_whois_server = '{sec_whois_server}', reg_name = '{reg_name}', reg_phone = '{reg_phone}', reg_email = '{reg_email}', \
        org_name = '{org_name}', creation_date = '{creation_date}', expiration_date = '{expiration_date}', updated_date = '{updated_date}', \
        insert_time = '{insert_time}', details = '{details}', hash_value = {hash_value}, sponsoring_registrar = '{sponsoring_registrar}', \
        name_server = '{name_server}' WHERE domain = '{domain}'""".format(
            table_whois = table_whois,
            domain = args['domain'],
            flag = args['flag'],
            domain_status = args['domain_status'],
            top_whois_server = args['top_whois_server'],
            sec_whois_server = args['sec_whois_server'],
            reg_name = args['reg_name'],
            reg_phone = args['reg_phone'],
            reg_email = args['reg_email'],
            org_name = args['org_name'],
            creation_date = args['creation_date'],
            expiration_date = args['expiration_date'],
            updated_date = args['updated_date'],
            insert_time = args['insert_time'],
            details = args['details'],
            hash_value = args['hash_value'],
            sponsoring_registrar = args['sponsoring_registrar'],
            name_server = args['name_server'],
            ) 

        self.__execute__(sql)

    # 删除whois记录信息
    # @param domain
    def db_delete(sql, **args):
        table_whois = self.get_table_name(args['domain'].split('.')[0])

        sql  = """DELETE FROM {table_whois} WHERE domain = '{domain}'""".format(
            table_whois = table_whois,
            domain = args['domain']
            )
        self.__execute__(sql)

    # 执行sql语句
    # @param sql sql语句
    def __execute__(self, sql):
        result = None
        if self.db_lock.acquire():
            try:
                self.cursor.execute(sql)
                result = self.cursor.fetchall()
            except MySQLdb.Error, e:
                if e.args[0] == 2013 or e.args[0] == 2006: # 数据库连接出错，重连
                    self.db_lock.release()
                    self.get_connect()
                    logger.info('数据库重新连接')
                    result = self.__execute__(sql) # 重新执行
                    self.db_lock.acquire()
                else:
                    logger.error('db_execute error_info: %d: %s' % (e.args[0], e.args[1]))
            self.db_lock.release()

        return result if result else None


    # 获取操作domain_whois表的表名
    # @param host_name 主机名
    def get_table_name(self, host_name):
        
        table_whois = static.DATABASE_WHOIS + '.domain_whois_'
        # 其他类
        if host_name.find('xn--') == 0:
            return table_whois + 'other'
        # 数字类
        elif host_name[0].isdigit():
            return table_whois + 'num'
        # 字母类
        elif host_name[0].isalpha():
            return table_whois + host_name[0].upper()
        # 其他类
        else:
            return table_whois + 'other'

if __name__ == '__main__':

    db = DataBase()
    db.get_connect()

    # result = db.db_select("whois_addr", "com")[0]
    # print result

    i = 0
    result = db.db_select(nature = 'domains', table_whois = 'DomainWhois.domain_whois_A')
    for domain in result:
        print domain[0],
        i += 1
        print '  ', i
    
    db.db_close()