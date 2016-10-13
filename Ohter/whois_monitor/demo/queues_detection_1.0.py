#coding:utf-8
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import paramiko
import os
import commands
import subprocess
import re

def send_mail(mail_id):
    # 第三方 SMTP 服务
    mail_host="smtp.qq.com"  #设置服务器
    mail_user="1187853170@qq.com"    #用户名
    mail_pass="lndjibwypswljghd"   #口令,QQ邮箱是输入授权码


    sender = '1187853170@qq.com'
    receivers = [mail_id]  # 接收邮件

    message = MIMEText('队列数小于85000，请检查', 'plain', 'utf-8')
    message['From'] = Header("hitnslab", 'utf-8')
    message['To'] =  Header("you", 'utf-8')

    subject = '运行监测'
    message['Subject'] = Header(subject, 'utf-8')

    try:
      smtpObj = smtplib.SMTP_SSL(mail_host, 465)
      smtpObj.login(mail_user,mail_pass)
      smtpObj.sendmail(sender, receivers, message.as_string())
      smtpObj.quit()
      print u"邮件发送成功"
    except smtplib.SMTPException,e:
      print e

def queues_det(interval_time,tigger_number):

    while 1:
        ssh1 = paramiko.SSHClient()
        ssh1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        link1={'ip':'172.29.152.249','uername':'hitnslab','password':'platform'}
        ssh1.connect(link1['ip'],22,link1['uername'],link1['password'])

        stdin, stdout, stderr = ssh1.exec_command("sudo rabbitmqctl list_queues",get_pty=True)
        stdin.write('platform\n')
        stdin.flush()

        for i in range(4):
            a=stdout.readline()
        mode = re.compile(r'\d+')
        num=mode.findall(a)[0]
        if(num<tigger_number):
            send_mail(mail_id='450943084@qq.com')
        time.sleep(interval_time*60)


if __name__ == "__main__":
    queues_det(interval_time=30,tigger_number=85000)#间隔时间，触发大小