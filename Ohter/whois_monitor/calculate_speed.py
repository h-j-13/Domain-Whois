#!/usr/bin/python
# encoding:utf-8

#
# Whois检测程序
# func  : 客户端速度计算
# time  : 2016.9.9
# author: @`13
#

import datetime
from db_opreation import DataBase
import ConfigParser


class client_speed:
    """客户端数据处理"""
    def __init__(self):
        """读取配置文件"""
        cf = ConfigParser.ConfigParser()
        cf.read("WhoisMonitor.conf")
        self.client_speed = []  # 客户端速度列表
        self.client1_ip_list = cf.get('Whois', 'GetDomainWhoisClient_1').split(';')  # 客户端ip群1
        self.client2_ip_list = cf.get('Whois', 'GetDomainWhoisClient_2').split(';')  # 客户端ip群2取
        self.client2_status = '未初始化'    # 二类客户端状态

    @staticmethod
    def getDatabaseTime():
        """:return 数据库当前时间"""
        DB = DataBase()
        DB.get_connect()
        SQL = """SELECT now()"""
        currentTime = DB.execute(SQL)[0][0]
        DB.db_close()
        return currentTime

    def calculateClientSpeed(self):
        """ 计算客户端时间
        :return @clientSpeedInfo 各个客户端速度信息组成的字符串
        :return @client2_status 二类客户端状态信息"""
        clientSpeedInfo = ''    # 客户端速度信息
        client2_status = ''  # 清空状态信息
        currentTime = self.getDatabaseTime()    # 当前数据库时间
        earlyTime = currentTime - datetime.timedelta(days=1)  # 前一天数据库时间
        DB = DataBase()  # 实例化数据库对象
        DB.get_connect()
        for ip in self.client1_ip_list:
            SQL = """SELECT max(`count`),min(`count`) from whois_sys_log.client_count_log_{client_num}
            WHERE insert_time > '{early_time}' AND insert_time < '{current_time}';""".format(
                client_num=ip.split('.')[-1], early_time=earlyTime,  current_time=currentTime
            )
            max_count, min_count = DB.execute(SQL)[0]
            clientSpeed_perHour = (max_count - min_count)/23.5  # 客户端平均每小时速度
            clientSpeedInfo += ip.split('.')[-1]+"客户端平均处理速度为：\t"+str(clientSpeed_perHour)[:7]+"(个/小时)\n"

        for ip in self.client2_ip_list:
            SQL = """SELECT max(`count`),min(`count`) from whois_sys_log.client_count_log_{client_num}
            WHERE insert_time > '{early_time}' AND insert_time < '{current_time}';""".format(
                client_num=ip.split('.')[-1], early_time=earlyTime,  current_time=currentTime
            )
            max_count, min_count = DB.execute(SQL)[0]
            clientSpeed_perHour = (max_count - min_count)/23.5  # 客户端平均每小时速度
            client2_status += ip.split('.')[-1] + "客户端状态：\t"
            if clientSpeed_perHour > 100:
                client2_status += "正常\n"
            else:
                client2_status += "崩溃！\n"
            clientSpeedInfo += ip.split('.')[-1]+"客户端平均处理速度为：\t"+str(clientSpeed_perHour)[:7]+"(个/小时)\n"
        return clientSpeedInfo, client2_status

if __name__ == '__main__':
    WM = client_speed()
    WM.calculateClientSpeed()
