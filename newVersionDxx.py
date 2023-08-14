import os
import time
from urllib.parse import quote

import requests
import json

stuInfo = [ # 仅需要在此填入openid即可
    "openid1",
    "openid2",
    "openid3"
]

def init():
    # 初次启动, 请求所需信息, 并写入本地
    url = "http://www.jxqingtuan.cn/pub/pub/vol/member/info?accessToken="
    print("正在获取所需信息并写入本地")
    with open("./userlist", 'a+', encoding='utf-8') as file:
        for item in stuInfo:
            resp = requests.get(url + item).json()['vo']
            xm = resp['username']
            zz = resp['areaid4']
            userid = resp['id']
            openid = resp['openid']
            try:
                xh = resp['telphone']
            except:
                xh = "114514"
            file.write(f"{xm}|{zz}|{userid}|{openid}|{xh}\n")
            time.sleep(1)
    print(f"{len(stuInfo)}条信息已经成功写入 ./userlist 文件中")

if __name__ == "__main__":

    print("""
    _                            _            
   (_)                          | |           
    ___  ________ __ _ _ __   __| |_  ____  __
   | \ \/ /______/ _` | '_ \ / _` \ \/ /\ \/ /
   | |>  <      | (_| | | | | (_| |>  <  >  < 
   | /_/\_\      \__, |_| |_|\__,_/_/\_\/_/\_\\
  _/ |              | |                       
 |__/               |_|       By: xiaoWangSec
""")

    userlist = [] # 用户信息
    if not os.path.exists("./userlist"): # 判断是否已缓存提交所需信息, 未缓存则进入缓存
        init()

    with open("./userlist", 'r', encoding='utf-8') as reader: # 处理信息
        for item in reader.readlines():
            info = item.strip().split("|")
            userlist.append([info[0], info[1], info[2], info[3], info[4]])
    print(f"成功处理{len(userlist)}条记录, 开始执行学习操作")

    resp = json.loads(requests.get("http://www.jxqingtuan.cn/pub/pub/vol/volClass/current").text)["result"]  # 用于获取最新一期的学习信息

    for userData in userlist:
        session = requests.session()
        session.headers = {
            "Proxy-Connection": "keep-alive",
            "Content-Length": "",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309055b) XWEB/6973 Flue",
            "openid": userData[3],
            "content-type": "application/x-www-form-urlencoded",
            "Accept": "*/*",
            "Origin": "http://www.jxqingtuan.cn",
            "Referer": "http://www.jxqingtuan.cn/html/",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh",
        }

        url = "http://www.jxqingtuan.cn/pub/pub/vol/member/addScoreInfo" # 获得学习积分的url
        mid = f"check=1&type=3&title=%E9%9D%92%E5%B9%B4%E5%A4%A7%E5%AD%A6%E4%B9%A0&url={quote(resp['uri'])}&openid={userData[3]}&userId={userData[2]}" # 传入学习链接, openId, userId
        session.post(url, data=mid)  # 模拟获得积分
        time.sleep(1)

        url = "http://www.jxqingtuan.cn/pub/pub/vol/volClass/join?accessToken="+ userData[3] # 记录学习记录的url
        session.headers["Referer"] = "http://www.jxqingtuan.cn/html/?accessToken=" + userData[3]
        session.headers["content-type"] = "application/json;charset=UTF-8;"
        payload = {
            "accessToken": userData[3],  # openid
            "course": resp["id"],  # 大学习期数
            "subOrg": userData[4],  # 学号
            "nid": userData[1],  # 组织代码
            "cardNo": userData[0],  # 姓名
        }
        print(session.post(url, data=json.dumps(payload)).text)  # 模拟学习
        time.sleep(1)

    print(f"成功完成{len(userlist)}次学习, 请等待后台数据刷新")

