#coding:utf-8
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 第三方 SMTP 服务
mail_host="smtp.qq.com"  #设置服务器
mail_user="1187853170@qq.com"    #用户名
mail_pass="lndjibwypswljghd"   #口令,QQ邮箱是输入授权码


sender = '1187853170@qq.com'
receivers = ['1402619706@qq.com']  # 接收邮件

message = MIMEText('程序运行正常', 'plain', 'utf-8')
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
