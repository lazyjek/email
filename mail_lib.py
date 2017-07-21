#!/usr/bin/python
#-*- coding: GB18030 -*-
import json
#import MySQLdb
from datetime import *
import time
import calendar
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
import os
import sys
import logging

reload(sys)
sys.setdefaultencoding('gb18030')

log_file="./log/send_mail.log"
log_level = logging.NOTSET


if not os.path.exists(os.path.dirname(log_file)):
    os.makedirs(os.path.dirname(log_file))

# set up logging to file - see previous section for more details
logging.basicConfig(level = log_level,
                    format = '%(levelname)-8s: %(asctime)s: %(message)s',
                    datefmt = '%m-%d %H:%M:%S',
                    filename = log_file,
                    filemode = 'a')
# define a Handler which writes WARNING messages or higher to the log.wf
logfile_warn = open(log_file + ".warn", 'a')
fh_warn = logging.StreamHandler(logfile_warn)
fh_warn.setLevel(logging.WARNING)
# set a format which is simpler for console use
formatter = logging.Formatter('%(levelname)-8s: %(asctime)s: %(message)s', "%m-%d %H:%M:%S")
# tell the handler to use this format
fh_warn.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(fh_warn)

logger = logging.getLogger('')

class log:   
    @staticmethod
    def info(msg):
        global logger
        logger.info(msg)
    @staticmethod
    def warning(msg):
        global logger_wf
        logger.warning(msg)
        
    @staticmethod
    def debug(msg):
        global logger
        logger.debug(msg)

    @staticmethod
    def stream():
        global logfile_warn
        return logfile_warn

class MyContent:
    def __init__(self,title="",content=""):
        self.title = unicode(title,'gbk')
        #self.content = content
        self.content = unicode(content,'gbk')

    def gen_content(self):
        thtml = "<table style=\"margin-top:20px;width:100%\">\n"
        thtml += "<table style=\"padding-top:1px;width:100%;\"><tr><td style=\"width:4px;background:red;margin:0;vertical-align:middle;\"></td><td><h3 style=\"font-family:Microsoft YaHei;font-size:16px;font-weight:bold;text-align:left;margin:0;gadding:0px 8px;\">\n"
        thtml += self.title
        thtml += "</h3></td>"
        thtml +="</tr></table>\n"
        
        #生成文本内容
        thtml +="<table><div>&nbsp;&nbsp;"
        thtml += self.content
        thtml +="</div></table>"
        thtml +="<br><br>"
        return thtml        

class MyTable:
    """
        生成表格，表格样式为:title,表格内容,查看更过,表格说明
    """
    def __init__(self, title="", doubleheader=[], header=[], body=[], current=-1, more="", desc=""):
        self.title = title
        self.doubleheader=doubleheader
        self.header = header
        self.body = body
        self.current = current
        self.more = more
        self.desc = desc

    def gen_table(self):
        length = len(self.doubleheader)
        thtml = "<table style=\"margin-top:20px;width:100%\">\n"
        thtml += "<table style=\"padding-top:1px;width:100%;\"><tr><td style=\"width:4px;background:red;margin:0;vertical-align:middle;\"></td><td><h3 style=\"font-family:Microsoft YaHei;font-size:16px;font-weight:bold;text-align:left;margin:0;gadding:0px 8px;\">\n"
        thtml += unicode(self.title,'gbk')
        thtml += "</h3></td>"
        thtml +="</tr></table>\n"
        #生成表格
        thtml += "<table style=\"width:100%;border:1px solid black;border:0px;border-collapse:separate;\">"
        thtml += "<tr>\n"
        #双行表头
        f_head = []
        s_head = []
        for i in range(0, length):
            f_head.append(self.doubleheader[i][0])
            if len(self.doubleheader[i]) == 1:
                thtml += "<th rowspan=\"2\" style=\"height:33px;background:rgb(68, 87, 117);color:#fff;font-size:13px;font-weight:bold;text-align:center;vertical-align:middle\">"
                thtml += unicode(self.doubleheader[i][0],'gbk')
            else:
                s_head += self.doubleheader[i][1:]
                col_num = len(self.doubleheader[i][1:])
                thtml += "<th colspan=\""+ str(col_num) +"\" style=\"height:33px;background:rgb(68, 87, 117);color:#fff;font-size:13px;font-weight:bold;text-align:center;vertical-align:middle\">"
                thtml += unicode(self.doubleheader[i][0],'gbk')
            thtml += "</th>\n";
        thtml += "</tr>\n"
        
        thtml += "<tr>\n"
        #表头第二行
        for para in s_head:
            thtml += "<th style=\"height:33px;background:rgb(68, 87, 117);color:#fff;font-size:13px;font-weight:bold;text-align:center;vertical-align:middle\">"
            thtml += unicode(para,'gbk')
            thtml += "</th>\n";
        thtml += "</tr>\n"

        #处理表格内容
        body_head = self.body[0]
        full_len = len(body_head)
        final_body = []
        idx = -1
        for i in range(0, len(self.body)):
            line = self.body[i]
            if len(line) == full_len:
                idx += 1
                final_body.append([])
                #final_body[idx] = []
            final_body[idx].append(line)
        
        #第一列可作为包含多行的表头。
        cnt = 0
        row_span_cnt = 0
        for sub_body in final_body:
            row_num = len(sub_body)         
            span_flag = 0
            for line in sub_body:
                if cnt%2 == 0:
                    thtml += "<tr style=\"display:table-row;border-collapse:separate;height:33px;line-height:33px;font-family:Microsoft YaHei;font-weight:normal;font-size:13px;vertical-align:middle;\">\n"
                else:
                    thtml += "<tr style=\"display:table-row;border-collapse:separate;height:33px;line-height:33px;font-family:Microsoft YaHei;font-weight:normal;font-size:13px;vertical-align:middle;background:#e3e6e6;\">\n"
                
                for para in line:
                    if span_flag == 0:
                        span_flag = 1
                        if row_span_cnt%2 == 0:
                            thtml += "<td rowspan=\""+ str(row_num) +"\" style=\"vertical-align:middle;text-align:center;\">"
                        else:
                            thtml += "<td rowspan=\""+ str(row_num) +"\" style=\"vertical-align:middle;text-align:center;background:#e3e6e6;\">"
                        row_span_cnt += 1
                    else:
                        thtml += "<td style=\"vertical-align:middle;text-align:center;\">"
                    thtml += unicode(str(para),'gbk')
                    thtml += "</td>\n"
                    #thtml += "</th>\n";
                    #thtml += "</td>\n"
                    #thtml += "</tr>\n";

                cnt += 1
                thtml += "</tr>\n";

        thtml += "</table>"
        #生成表格说明
        if self.desc != "":
            thtml += "<table style=\"width:100%;padding-bottom: 1px;\"><tr><td align=\"left\"><p style=\"font-family:Microsoft YaHei;font-size:13px;color:gray\">&nbsp;"
            thtml += unicode(self.desc,'gbk')
            thtml += "</p><td></tr></table>"
        thtml += "</table>"
        thtml +="<br><br>"
        return thtml

class MyHtml:
    def __init__(self,title):
        self.html = "<html>"

    def add_content(self,title,content):
        content = MyContent(title,content)
        self.html += content.gen_content()

    def add_table(self,title,doubleheader,header,body,current=-1,more="",desc=""):
        table =  MyTable(title=title, doubleheader=doubleheader, header=header, body=body, current=current, more=more, desc=desc)
        self.html += table.gen_table()

    def get_html(self):
        self.html += "</table></html>"
        return self.html

class MailSender:
    def __init__(self,receiver_list=[],subject="",attach_list=[],html="",sender="jennifer@test.com"):
        self.receiver_list = receiver_list
        self.subject = unicode(subject,"gbk")
        self.attach_list = attach_list
        self.sender = sender
        self.html = html

    def send_email(self):
        if len(self.receiver_list) == 0:
            log.warning("receiver num is 0,will exit")
            return False
                   
        msg = MIMEMultipart('alternative')
        msg['Subject'] = u"【Subject】" + self.subject
        msg['To'] = ";".join(self.receiver_list)
        msg["From"] = ("%s<jennifer@test.com>") % (Header(u'Jennifer Yang','utf-8'),)
        
        # Create the body of the message (an HTML version).
        part1 = MIMEText(self.html, 'html',_charset='gbk')
        msg.attach(part1)
        
        # add attach
        for filelist in self.attach_list:
            if os.path.exists(filelist[0]):
                att = MIMEText(open(filelist[0], 'r').read(), 'base64', 'utf-8')
                att["Content-Type"] = '%s'%filelist[1]
                att["Content-Disposition"] = 'attachment; filename="%s"'%os.path.basename(filelist[0])
                msg.attach(att)
        
        smtp = smtplib.SMTP()
        smtp.connect('xxxxxxxx.com')
        smtp.sendmail(self.sender, self.receiver_list, msg.as_string())
        smtp.quit()

if __name__ == '__main__':
    #正文标题
    mail_content = MyHtml("html title")
    #邮件正文中添加一段文本描述
    mail_content.add_content("summary","a test contest</br> a test contest")
    mail_content.add_table(title="table4",doubleheader=[["测试1","测试2"],["测试3"],["测试4","测试5","测试6"],["测试7"]],header=[],body=[[1,2,3,4,5],[1,2,3,4],[1,2,3,4],[5,5,5,5,5],[3,3,3,3],[1,1,1,1]],desc="desc")

    #生成html格式的邮件正文
    html = mail_content.get_html()
    out_f = open("./out_mail.html",'w')
    out_f.write(html+"\n")
    
    #指定邮件标题,添加附件，不指定attach_list表示没有附件
    sender = MailSender(receiver_list=["jennifer@test.com"],subject="test_subject",attach_list=[["./test.txt"]],html=html)
    
    #邮件发送
    sender.sen
