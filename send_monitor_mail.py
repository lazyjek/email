#-*- coding: GB18030 -*-
from mail_lib import *
import sys

if __name__ == '__main__':
    #正文标题
    mail_content = MyHtml(title = "测试邮件")
    #邮件正文中添加一段文本描述
    mail_content.add_content(title="摘要",content="添加摘要")
    
    # 插入表格内容
    fp = open('./data/test.dat','r')
    tmp_list = []
    index = 0
    title = "添加表格标题"
    doubleheader = [["日期"],["类型A"],["类型B"],["类型C"],["类型D"]]
    para_head = ["指标1","指标2","指标3"]
    desc = "添加描述"
    for i in range(1,len(doubleheader)):
        doubleheader[i] += para_head
    for line in fp :
        items=line.strip().split('\t')
        tmp_list.append(items)
    mail_content.add_table(title=title, doubleheader=doubleheader, header=[],body=tmp_list,desc=desc)
       
    #添加文本描述块
    mail_content.add_content(title="备注",content="添加备注")
    #生成html格式的邮件正文
    html = mail_content.get_html()
    #指定邮件标题,添加附件，不指定attach_list表示没有附件
    _files = []
    receivers = ['jennifer@test.com']
    sender = MailSender(receiver_list=receivers,subject="test email",attach_list=_files,html=html)
    #邮件发送
    sender.send_email()
