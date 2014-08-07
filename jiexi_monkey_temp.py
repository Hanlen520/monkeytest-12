#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
import os
import re
from ftplib import FTP 
import sys
import GetDB_class
import ConfigParser
import time
import shutil
import MySQLdb.cursors


#tail.py
#Usage: python tail.py FILENAME LINES
#similar to linux command: tail -n LINES FILENAME
def last_lines(filename, lines = 1):
     #print the last several line(s) of a text file
     """
     Argument filename is the name of the file to print.
     Argument lines is the number of lines to print from last.
     """
     lines = int(lines)
     block_size = 1024
     block = ''
     nl_count = 0
     start = 0
     fsock = file(filename, 'rU')
     try:
         #seek to end
         fsock.seek(0, 2)
         #get seek position
         curpos = fsock.tell()
         while(curpos > 0): #while not BOF
             #seek ahead block_size+the length of last read block
             curpos -= (block_size + len(block));
             if curpos < 0: curpos = 0
             fsock.seek(curpos)
             #read to end
             block = fsock.read()
             nl_count = block.count('n')
             #if read enough(more)
             if nl_count >= lines: break
         #get the exact start position
         for n in range(nl_count-lines+1):
             start = block.find('n', start)+1
     finally:
         fsock.close()
     #print it out
     return block[start:]

def get_text_file(filename):
        if not os.path.exists(filename):
                print("ERROR: file not exit: %s" % (filename))
                return None

        if not os.path.isfile(filename):
                print("ERROR: %s not a filename." % (filename))
                return None

        f = open(filename, "r")
        content = f.read()
        f.close()

        return content


def ftp_up(filename = "image\monkey_run_end.png"): 
    ftp=FTP()
    ftp.set_debuglevel(2)#打开调试级别2，显示详细信息;0为关闭调试信息 
    ftp.connect('192.168.9.163','21')#连接 
    ftp.login('monkey','monkey')#登录，如果匿名登录则用空串代替即可 
    #print ftp.getwelcome()#显示ftp服务器欢迎信息 
    #ftp.cwd('xxx/xxx/') #选择操作目录 
    bufsize = 1024#设置缓冲块大小 
    file_handler = open(filename,'rb')#以读模式在本地打开文件 
    ftp.storbinary('STOR %s' % os.path.basename(filename),file_handler,bufsize)#上传文件 
    ftp.set_debuglevel(0) 
    file_handler.close() 
    ftp.quit()
    print "ftp up OK" 

#last_lines(sys.argv[1], sys.argv[2]) #print the last s
#***读取配置信息,
cf = ConfigParser.ConfigParser()
cf.read("config.conf")

appCnName = cf.get("appinfo", "appCnName")
appEnName = cf.get("appinfo", "appEnName")
appVersion = cf.get("appinfo", "version")
packageName = cf.get("appinfo", "packageName")
zhongduan = cf.get("zhongduan", "zhongduan")
zhongduan_os=cf.get("zhongduan", "os")
##########
last_lines_text = last_lines('monkey_temp.txt', 500)
allcontent= get_text_file('monkey_temp.txt')
#print "last_lines_text:",last_lines_text
if(last_lines_text==""):
     exit()
sStrs= last_lines_text
sStr = 'CRASH: '+str(packageName)
sStr02 = "ANR in "+str(packageName)
nPos = sStrs.find(sStr)
nPos02 = allcontent.find(sStr02)
print nPos02
#exit()

if nPos>0:
     print "::应用崩溃了",sStr
     isCrash = 1
     crashKeyWords=sStr
elif nPos02>0:
     print "::应用崩溃了",sStr
     isCrash = 1
     last_lines_text = allcontent
     crashKeyWords=sStr02
else:
     print "::finished"
     last_lines_text = last_lines_text[-100:] #截取倒数
     isCrash = 0
     crashKeyWords=""
first_lines_text = ""
file02 = open("monkey_temp.txt")
lines = file02.readlines()[0:2]
for line in lines:
  first_lines_text = first_lines_text + str(line)
file02.close()


import socket
#获取本机电脑名
myPcName = socket.getfqdn(socket.gethostname(  ))
#获取本机ip
#myIpaddr = socket.gethostbyname(myPcName)
myIpaddr=""
print myPcName #电脑名
print myIpaddr #ip地址
###############################################
onTime = '%d-%02d-%02d %d:%d:%d' %time.localtime()[0 : 6]
curr_runnedTime = time.ctime()
theImageName = onTime.replace(':','')
theImageName = theImageName.replace(' ','-')
print theImageName
path00 = os.getcwd()
path = path00+"\\image\\"
newname=None
for file in os.listdir(path):
    if os.path.isfile(os.path.join(path,file))==True:
        if file.find('\.')<0:
            newname=appEnName+theImageName+file
            print "newname",newname
            os.rename(os.path.join(path,file),os.path.join(path,newname))
            print file,'ok'
        else:
            newname=None
            print "else"
if(newname):
    up_imagename = "image\\"+newname
    ftp_up(up_imagename)
    shutil.move(path+newname,path00+"\\image-bak\\"+newname)
else:
    print u"无截图"

#***读取数据库连接，
GetDB_instance = GetDB_class.GetDB()
conn = GetDB_instance.getDBconn()
cursor = conn.cursor(MySQLdb.cursors.DictCursor)
sql_select_zhongduan = "select * from app_test_main where zhongduan= '"+ zhongduan +"' and appCnName = '"+ appCnName +"'"
res001 = cursor.execute(sql_select_zhongduan)
conn.commit()
if(res001>0):
    pass
else:
    #***写sql语句，
    sql_insert_appinfo= "insert into app_test_main(appCnName,appEnName,appVersion,isRichinfo,os,zhongduan)\
    values('"+str(appCnName)+"','"+str(appEnName)+"','"+str(appVersion)+"','"+str(1)+"','"+str("andriod")+"','"+str(zhongduan)+"')"
    print sql_insert_appinfo
    #***执行sql语句，入数据库
    res002 = cursor.execute(sql_insert_appinfo)
    conn.commit()

#***写sql语句，
sql_insert_monkey_log= "insert into monkey_log(appCnName,appEnName,appVersion,zhongduan,pcName,ipAddr,isCrash,runFirstLinesLog,crashNotes,crashKeyWords,scr_image_file,onTime)\
values('"+str(appCnName)+"','"+str(appEnName)+"','"+str(appVersion)+"','"+str(zhongduan)+"','"+str(myPcName)+"','"+str(myIpaddr)+"','"+str(isCrash)+"','"+str(first_lines_text)+"','"+str(last_lines_text)+"','"+str(crashKeyWords)+"','"+str(newname)+"','"+onTime+"')"
print sql_insert_monkey_log
#***执行sql语句，入数据库
res003 = cursor.execute(sql_insert_monkey_log)
conn.commit()
