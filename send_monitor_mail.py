#-*- coding: GB18030 -*-
from mail_lib import *
import sys

if __name__ == '__main__':
    #���ı���
    mail_content = MyHtml(title = "�����ʼ�")
    #�ʼ����������һ���ı�����
    mail_content.add_content(title="ժҪ",content="���ժҪ")
    
    # ����������
    fp = open('./data/test.dat','r')
    tmp_list = []
    index = 0
    title = "��ӱ�����"
    doubleheader = [["����"],["����A"],["����B"],["����C"],["����D"]]
    para_head = ["ָ��1","ָ��2","ָ��3"]
    desc = "�������"
    for i in range(1,len(doubleheader)):
        doubleheader[i] += para_head
    for line in fp :
        items=line.strip().split('\t')
        tmp_list.append(items)
    mail_content.add_table(title=title, doubleheader=doubleheader, header=[],body=tmp_list,desc=desc)
       
    #����ı�������
    mail_content.add_content(title="��ע",content="��ӱ�ע")
    #����html��ʽ���ʼ�����
    html = mail_content.get_html()
    #ָ���ʼ�����,��Ӹ�������ָ��attach_list��ʾû�и���
    _files = []
    receivers = ['jennifer@test.com']
    sender = MailSender(receiver_list=receivers,subject="test email",attach_list=_files,html=html)
    #�ʼ�����
    sender.send_email()
