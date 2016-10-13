# coding:utf-8

#
# Whois检测程序
# func  : 发送邮件
# time  : 2016.9.8
# author: @`13
#

from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import time
import ConfigParser
import smtplib
from get_info import WhoisInfoMonitor

# 邮件类
class Mail:
    """实现邮件的发送"""

    def __init__(self):
        """读取基本配置内容
            @WhoisMonitor.conf : 配置文件"""
        cf = ConfigParser.ConfigParser()
        cf.read("WhoisMonitor.conf")  # 读取内容
        self.SENDER = cf.get('Mail', 'sender')  # 送信人
        self.PASSCODE = cf.get('Mail', 'passcode')  # 授权码
        self.RECEIVER = cf.get('Mail', 'receiver')  # 收信人
        self.SMTP_HOST = cf.get('Mail', 'smtp_host')  # smtp服务器地址

    @staticmethod
    def format_addr(s):
        """地址格式配饰"""
        # 为了处理含有中文的情况
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(),
                           addr.encode('utf-8') if isinstance(addr, unicode) else addr))

    def send_mail(self):
        """发送邮件"""
        # 邮件基本信息
        from_addr = self.SENDER  # 送信人
        password = self.PASSCODE  # 授权码
        to_addr = self.RECEIVER  # 收信人
        smtp_server = self.SMTP_HOST    # smtp服务器地址
        # 获取whois信息
        WM = WhoisInfoMonitor()
        WhoisSystemInfo = WM.unionInfo()
        # 消息基本信息
        msg = MIMEText(WhoisSystemInfo, 'plain', 'utf-8')    # 主体内容
        msg['From'] = self.format_addr(u'HITwh NSlab <%s>' % from_addr)  # 来自
        msg['To'] = self.format_addr(u'`13 <%s>' % to_addr)  # 送往
        localdate = str(time.strftime("%Y-%m-%d", time.localtime(time.time())))  # 获取本地时间
        msg['Subject'] = Header(u'GetDomainWhois 系统 %s 运行情况汇报' \
                                % localdate, 'utf-8').encode()  # 获取本地时间
        # 送出消息
        server = smtplib.SMTP(smtp_server, 25)  # 连接smtp服务器
        server.set_debuglevel(0)  # 设置debug等级为0 - 无显示
        server.login(from_addr, password)  # 登陆
        server.sendmail(from_addr, [to_addr], msg.as_string())  # 送信
        server.quit()  # 退出


if __name__ == '__main__':
    M = Mail()
    M.send_mail()
