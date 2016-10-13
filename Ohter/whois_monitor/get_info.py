# coding:utf-8

#
# Whois检测程序
# func  : 获取系统状态信息
# time  : 2016.9.8
# author: @`13
#

import ConfigParser
import paramiko
from calculate_speed import client_speed
import time

class WhoisInfoMonitor():
    """Whois信息监测类"""

    def __init__(self):
        """基本配置获取"""
        cf = ConfigParser.ConfigParser()
        cf.read("WhoisMonitor.conf")  # 读取配置文件内容
        # 服务器部分
        self.srv_ip = cf.get('Whois', 'GetDomainWhoisService')  # 服务器ip
        self.srv_user = cf.get('Whois', 'GetDomainWhoisService_username')  # 服务器用户名
        self.srv_pw = cf.get('Whois', 'GetDomainWhoisService_password')  # 服务器密码
        self.srv_process_status = 'Error：未初始化'  # 服务器进程信息
        self.srv_MQ_status = {'domain_queue': -1, 'whois_queue': -1}  # 服务器RabbitMQ信息
        # 1类客户端部分
        self.clinet1_num = cf.getint('Whois', 'GetDomainWhois_num_1')  # 1类客户端数量
        self.client1_ip_list = cf.get('Whois', 'GetDomainWhoisClient_1').split(';')   # 集群ip
        self.client1_user_list = cf.get('Whois', 'GetDomainWhoisClient_1_username').split(';')  # 集群u用户名
        self.client1_pw_list = cf.get('Whois', 'GetDomainWhoisClient_1_password').split(';')  # 集群密码
        self.client1_process_status = 'Error：未初始化'  # 客户端进程信息
        # 2类客户端部分 需要两层ssh连接
        self.clinet2_num = cf.getint('Whois', 'GetDomainWhois_num_2')  # 2类客户端数量
        self.client2_ip = cf.get('Whois', 'GetDomainWhoisClient_2_IP')  # 中间层ip
        self.client2_user = cf.get('Whois', 'GetDomainWhoisClient_2_USER')  # 中间层用户名
        self.client2_pw = cf.get('Whois', 'GetDomainWhoisClient_2_PW')  # 中间层密码
        self.client2_ip_list = cf.get('Whois', 'GetDomainWhoisClient_2').split(';')  # 集群ip
        self.client2_user_list = cf.get('Whois', 'GetDomainWhoisClient_2_username').split(';')  # 集群u用户名
        self.client2_pw_list = cf.get('Whois', 'GetDomainWhoisClient_2_password').split(';')  # 集群密码
        self.client2_process_status = 'Error：未初始化'  # 客户端进程信息

    def getSrvInfo(self):
        """249主服务器内容检测"""
        ssh_249 = paramiko.SSHClient()  # 建立连接
        ssh_249.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        link249 = {'ip': self.srv_ip, 'uername': self.srv_user, 'password': self.srv_pw}  # 连接基本信息
        ssh_249.connect(link249['ip'], 22, link249['uername'], link249['password'])  # 连接
        stdin, stdout, stderr = ssh_249.exec_command(
            "sudo rabbitmqctl list_queues", get_pty=True)  # 获取RabbitMQ队列信息
        stdin.write('platform\n')
        stdin.flush()
        RabbitMQ_info = stdout.readlines()
        stdin.flush()
        stdin, stdout, stderr = ssh_249.exec_command(
            "ps ax|grep main", get_pty=True)  # 获取GetDomainWhois程序运行信息
        GetDomainWhoisSrv_info = stdout.readlines()
        ssh_249.close()  # 关闭连接
        # 处理服务器信息部分
        # 获取进程信息
        if self.isSrvAlive(GetDomainWhoisSrv_info):
            self.srv_process_status = "主程序正常运行中...\n"
        else:
            self.srv_process_status = "主程序异常崩溃！...\n"
        # 获取队列信息
        for line in RabbitMQ_info:
            if line.find("domain_queue") != -1:
                self.srv_MQ_status['domain_queue'] = line.split('domain_queue', 1)[1].strip()
            if line.find("whois_queue") != -1:
                self.srv_MQ_status['whois_queue'] = line.split('whois_queue', 1)[1].strip()
        return self.srv_process_status, self.srv_MQ_status

    def getClient1Info(self):
        """获取1类客户端集群信息"""
        self.client1_process_status = ''  # 清空原有内容
        for i in range(self.clinet1_num):
            ssh_client = paramiko.SSHClient()  # 建立连接
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            link_client = {'ip': self.client1_ip_list[i],
                           'uername': self.client1_user_list[i],
                           'password': self.client1_pw_list[i]}  # 连接基本信息
            ssh_client.connect(link_client['ip'], 22,
                               link_client['uername'],
                               link_client['password'])  # 连接
            stdin, stdout, stderr = ssh_client.exec_command(
                "ps ax|grep main", get_pty=True)  # 获取RabbitMQ队列信息
            stdin.flush()
            process_info = stdout.readlines()
            if self.isSrvAlive(process_info):
                clinetinfo = self.client1_ip_list[i].split('.')[-1]+"客户端运行情况：正常\n"
            else:
                clinetinfo = self.client1_ip_list[i].split('.')[-1]+"客户端运行情况：崩溃!\n"
            self.client1_process_status += clinetinfo
        return self.client1_process_status

    def getClient2Info(self):
        """获取2类客户端集群信息"""
        self.client2_process_status = ''  # 清空原有内容
        # 通过堡垒机获取信息失败，改为通过数据库内容判断。
        # for i in range(self.clinet2_num):
        #     ssh_client = paramiko.SSHClient()  # 建立连接
        #     ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #     link_client = {'ip': self.client2_ip,
        #                    'uername': self.client2_user,
        #                    'password': self.client2_pw}  # 连接基本信息
        #     ssh_client.connect(link_client['ip'], 22,
        #                        link_client['uername'],
        #                        link_client['password'])  # 连接
        #     stdin, stdout, stderr = ssh_client.exec_command(
        #         "clear".format(user=self.client2_user_list[i],
        #                                  ip=self.client2_ip_list[i]), get_pty=True)  # 二次ssh连接
        #     stdin.flush()
        #     process_info = stdout.readlines()
        #     print process_info
        CS = client_speed()
        self.client2_process_status = CS.calculateClientSpeed()[1]
        return self.client2_process_status

    def getClientSpeedInfo(self):
        """获取客户端速度信息"""
        CS = client_speed()
        return CS.calculateClientSpeed()[0]

    def unionInfo(self):
        """信息汇总"""
        summaryInfo = ''    # 总结信息
        summaryInfo += '---主程序相关信息---\n\n'
        summaryInfo += self.getSrvInfo()[0]
        summaryInfo += '\n---当前RabbitMQ情况---\n\n'
        summaryInfo += 'domain_queue:\t'
        summaryInfo += str(self.srv_MQ_status['domain_queue'])
        summaryInfo += '\nwhois_queue:\t'
        summaryInfo += str(self.srv_MQ_status['whois_queue'])
        summaryInfo += '\n\n---客户端相关信息---\n\n'
        summaryInfo += self.getClient1Info()
        summaryInfo += self.getClient2Info()
        summaryInfo += '\n---客户端速度信息---\n\n'
        summaryInfo += self.getClientSpeedInfo()
        summaryInfo += '\n\n'
        summaryInfo += '    以上内容生成与：'
        currentTime = str(time.strftime("%Y年%m月%d日 %H:%M:%S",time.localtime(time.time())))
        summaryInfo += currentTime
        summaryInfo += '\n    * 客户端速度取上一日平均值\n\n'
        summaryInfo += '    Power by @`13 -HITwh NSlab 2016.9'
        return summaryInfo

    @staticmethod
    def isSrvAlive(process_info):
        """判断服务器运行状态
            @Srv_info:从终端获取的进程信息"""
        for line in process_info:
            if line.find("python main.py") != -1:
                return True
        return False


if __name__ == '__main__':
    WM = WhoisInfoMonitor()
    WM.unionInfo()
