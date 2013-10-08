#-*- encoding:utf-8 -*-
#Author:icenan2@gmail.com
import smtplib, mimetypes
import base64
import os
import string
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.Header import Header
from email.mime.image import MIMEImage
import random

fconfig=open("./config.ini")
fsender=open("./senders/"+os.listdir("./senders/")[0],'r')
#读取收件人信息
frecipients=open("./recipients/"+os.listdir("./recipients/")[0],'r')
#用于统计无效地址,追加方式打开
fnotfound=open("./mails_not_found","a")
sender_lists=fsender.readlines()
config_list=fconfig.readlines()
content=""
#去除行尾的换行符，在linux下换行符为'\n\r'两个字节
subject=config_list[0].replace("\n","")
subject=subject.replace("\r","")
for i in range(1,len(config_list)):
  config_list[i]=config_list[i].replace("\n","")
  config_list[i]=config_list[i].replace("\r","")
  content+=config_list[i]
#print content
#在邮件内容的最下方加上一段随机序列
appendix="<br/><p style='visibility:hidden'>This is your lucky number "+str(random.randint(1000000000000000000000000000000,9000000000000000000000000000000000000000000000000000000000000))+"</p>"
content+=appendix
#txt = MIMEText("这是邮件内容~~", _subtype='plain',  _charset='UTF-8')
#添加html的邮件内容
'''
txt = MIMEText("<img src='https://lh5.ggpht.com/XC1quyRCu5o9RJLMAtpwBx8mLeJrsHqoVh9k8DuCdJdiGAiGV2uXuG1EboqawOkFHw=w124'></img><br/><a href='https://play.google.com/store/apps/details?id=com.rootroader.nlzn&feature=search_result#?t=W251bGwsMSwxLDEsImNvbS5yb290cm9hZGVyLm5sem4iXQ..'>Google Play 下载地址</a><br/><a href='http://m.163.com/android/software/328qj3.html'>网易下载地址</a><br/><p ><font size='3' color='red'>寂寞时，用它，找他，找她。。。!</font></p>", _subtype='html',  _charset='UTF-8')
'''
txt=MIMEText(content,_subtype='html',_charset='UTF-8')
#msg.attach(txt)

def send_mail(sender,recipient):
  PORT="25"
  PREFIX="smtp."
 # msg = MIMEMultipart()
 # msg['Subject'] = Header('或许，你一直在寻找这样一款应用', charset='UTF-8')
 # msg.attach(txt)
  msg = MIMEMultipart()
  #msg['Subject'] = Header('或许，你一直在寻找这样一款应用', charset='UTF-8')
  msg['subject']=Header(subject,charset='UTF-8')
  msg.attach(txt)
  sender.strip()
  recipient.strip()
  sender=sender.replace('\n','')
  sender=sender.replace('\r','')
  if not sender.split():
    return 6
  sender_address=sender.split(':')
  password=sender_address[1]
  sender_name=sender_address[0].split('@')[0]  #获取用户名和邮箱后缀
  postfix=sender_address[0].split('@')[1]
  msg['From'] = sender_address[0]
 # if 0==cmp(postfix,"gmail.com") :  #gmail邮箱端口特殊处理
  #  PORT="587"
  if 0==cmp(postfix,"aol.com") or 0==cmp(postfix,"gmail.com")  or 0==cmp(postfix,"AOL.COM") or 0==cmp(postfix,"GMAIL.COM"):# @aol.com和 gmail邮箱端口号特殊处理
    PORT="587"
  if postfix.find("yahoo")>=0 or postfix.find("YAHOO")>=0: #雅虎邮箱的前缀特殊处理
    PREFIX="smtp.mail."
  if 0==cmp(postfix,"hotmail.com") or 0==cmp(postfix,"HOTMAIL.COM"):
    postfix="live.com"
  print u"连接邮件服务器:  "+PREFIX+postfix+":"+PORT
  try:
    smtp = smtplib.SMTP(PREFIX+postfix,PORT)
  except Exception,e:
    print u"服务器连接错误"
    print str(e)
    return 4
  #smtp.connect(PREFIX+postfix+PORT)
  #gmail使用安全连接
  
  if 0==cmp(postfix,"gmail.com"):
    try:
      smtp.ehlo()
      smtp.starttls()
      smtp.ehlo()
    except Exception,e:
      print "安全连接建立失败"
      print str(e)
      return 5

  print u"发件人:"+sender_address[0]
  try:
    smtp.login(sender_address[0],password)
  except Exception,e:
    print sender_address[0]+" login error"
    print str(e)
    return 3
  recipient=recipient.replace('\n','')
  recipient=recipient.replace('\r','')
  print u"收件人:"+recipient
  msg['To']= recipient
# print 'hello  '+ msg['To']
  try:
    e=smtp.sendmail(sender_address[0], recipient, msg.as_string())
  except smtplib.SMTPRecipientsRefused :
    print u'该收件人地址不存在'
    return 1
  except Exception ,e:
    print u"发送失败"
    print str(e)
    return 2
  print u'发送成功'#发送成功
  #global count
  #count+=1
  return 0
  time.sleep(4)#等待8s
  smtp.quit()
print u"开始发送邮件..."
if __name__ == '__main__':
  count=0
  single_count=0
  length=len(sender_lists)
  i=0
  for recipient in frecipients:
#    time.sleep(6)
    if not recipient.split():
      continue
    if single_count>2:#如果同一个邮箱连续发送超过2封邮件，则换下一个邮箱
      i=(i+1)%length  #循环利用发件列表
      single_count=0  #更换发件邮箱，统计归零
      ret=send_mail(sender_lists[i],recipient)
    else:
      ret=send_mail(sender_lists[i],recipient)
    if 1==ret:
       fnotfound.write(recipient+'\n')
    elif 0==ret:
      count+=1
      single_count+=1
    else:
      i=(i+1)%length  #循环利用发件列表
      single_count=0  #更换发件邮箱，统计归零
print u"发送结束,本次累计发送"+str(count)+u"封邮件"
print u"按任意键退出程序..."
s=raw_input()
fnotfound.close()
fconfig.close()
frecipients.close()
