#-*-coding:utf-8-*
import urllib.request
from bs4 import BeautifulSoup
import socket
import time
from urllib.error import URLError
import urllib.request
import json
#import urlopen


def get_ip():
    url = 'http://www.net.cn/static/customercare/yourip.asp'
    req = urllib.request.Request(url)
    rsp=urllib.request.urlopen(req)
    html=rsp.read().decode('utf-8',"ignore")
    html=BeautifulSoup(html,'html.parser')
    iph2=html.h2
    global ip
    ip=iph2.get_text()
    #print("你的公网IP是:",ip)

print("\n----开始侦测本机公网IP地址----")
get_ip()
#send_ip()

#执行更改godaddy的ddns
api_url = 'https://api.godaddy.com/v1/domains/1kqiu.app/records';

def update_NS(api_url,ip_addr):
    #定义http请求头
    head = {}
    #定义服务器返回json数据给我们
    head['Accept'] = 'application/json'

    head['Content-Type'] = 'application/json'

    head['Authorization'] = 'sso-key dLYqYpZmrVRm_KvFMFytv1EnASdZuJwW7WX:UqeyxxRG6Xr9oaX5hipLCJ' 

    #定义解析记录
    records_a = {
        "data" : ip_addr,
        "name" : "@",
        "ttl" : 600,
        "type" : 'A',
     }

    records_NS01 = {
         "data" : "ns07.domaincontrol.com",
         "name" : "@",
         "ttl" : 3600,
         "type" : "NS",
     }

    records_NS02 = {
         "data" : "ns08.domaincontrol.com",
         "name" : "@",
         "ttl" : 3600,
         "type" : "NS",
     }

    put_data = [records_a,records_NS01,records_NS02]

    try:
         req = urllib.request.Request(api_url,headers = head,data = json.dumps(put_data).encode(),method = "PUT")
         rsp = urllib.request.urlopen(req)

         code = rsp.getcode()
         if code == 200:
             print('成功更改域名解析了：'+ ip_addr)
         else:
             print('更改失败！')
    except:
        print('错误！')

#监听
i=0
while i == 0:
    get_ip()
    print ("当前公网IP:",ip)
    tmp1_ip=ip
#    print("tmp1_ip:",tmp1_ip)
    print("------休息30秒------")
    time.sleep(30)
    get_ip()
    tmp2_ip=ip
#   print("tmp2_ip:",tmp2_ip)
    if tmp1_ip == tmp2_ip:
        print("########OJBK,地址没变！########")
    else:
        ip=tmp2_ip
        print("公网地址改变:",ip)
        update_NS(api_url,ip_addr)
        print("同步到远程服务器成功！")
        print("\n########继续检查########")



