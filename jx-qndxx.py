import random
import time
from urllib.parse import quote

import requests
import json

stuInfo = [  # 仅需要在此填入openid即可
    "oc2p1111",
    "oc2p2222",
    "oc2p3333"
]

if __name__ == "__main__":

    print("""
    _                            _            
   (_)                          | |           
    ___  ________ __ _ _ __   __| |_  ____  __
   | \ \/ /______/ _` | '_ \ / _` \ \/ /\ \/ /
   | |>  <      | (_| | | | | (_| |>  <  >  < 
   | /_/\_\      \__, |_| |_|\__,_/_/\_\/_/\_\
  _/ |              | |                       
 |__/               |_|       By: xiaoWangSec
""")

    try:
        with open("./users.json", 'r', encoding='utf-8') as reader:
            try:
                userlist = json.load(reader)
            except:
                userlist = json.loads("{}")
    except FileNotFoundError:
        print("user.json文件不存在, 已新建")
        with open("./users.json", 'w') as file:
            file.write("{}")
            userlist = json.loads("{}")

    if len(userlist) != len(stuInfo):  # 新初始化或者新增了用户
        for item in stuInfo:
            if item not in userlist:
                print(f"{item} - 不存在的用户, 尝试读取数据并写入")
                url = "https://www.jxqingtuan.cn/pub/pub/vol/member/info?accessToken="
                resp = requests.get(url + item).json()['vo']
                xm = resp["username"]
                zz = resp["areaid4"]
                userid = resp["id"]
                openid = resp["openid"]
                try:
                    telphone = resp["telphone"]
                except:  # 没有手机号的自动填充手机号
                    updateUrl = "https://www.jxqingtuan.cn/pub/pub/vol/member/updateUserInfo"
                    telphone = "138" + random.randrange(10000000, 99999999)
                    updateDate = f"type=0&userId={resp['id']}&name={quote(resp['username'])}&sex=&birthday=&levelId_1={resp['areaid1']}&levelId_2={resp['areaid2']}&levelId={resp['areaid3']}&subLevelId={resp['areaid4']}&xuehao=&address=&phone=138{telphone}"
                    resp = requests.post(updateUrl, data=updateDate)

                userlist[item] = {
                    "cardNo": xm,  # 姓名
                    "nid": zz,  # 组织
                    "userid": userid,  # 编号
                    # "accessToken": openid,  # openid
                    "subOrg": telphone  # 手机号
                }
            # else:
            #     print("已存在的用户 跳过")

        with open("./users.json", 'w', encoding='utf-8') as writer:
            json.dump(userlist, writer, indent=4)  # 处理完的json写入

    print(f"成功处理{len(userlist)}条记录, 开始执行学习操作")
    resp = \
        json.loads(requests.get("https://www.jxqingtuan.cn/pub/pub/vol/index/index?page=1&pageSize=10").text)[
            "vo"]  # 用于获取最新一期的学习信息
    for userData in userlist:
        session = requests.session()
        session.headers = {
            "Proxy-Connection": "keep-alive",
            "Content-Length": "",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309055b) XWEB/6973 Flue",
            "openid": userData,
            "content-type": "application/x-www-form-urlencoded",
            "Accept": "*/*",
            "Origin": "http://www.jxqingtuan.cn",
            "Referer": "http://www.jxqingtuan.cn/html/",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh",
            "Authorization": userData,
        }

        url = "https://www.jxqingtuan.cn/pub/pub/vol/member/addScoreInfo"  # 获得学习积分的url
        mid = f"check=1&type=3&title=%E9%9D%92%E5%B9%B4%E5%A4%A7%E5%AD%A6%E4%B9%A0&url={quote(resp['studyUrl'])}&openid={userData}&userId={userlist[userData]['userid']}"  # 传入学习链接, openId, userId
        session.post(url, data=mid)  # 模拟获得积分
        time.sleep(5)

        url = "https://www.jxqingtuan.cn/api-client/classRecord/learningRecords"  # 记录学习记录的url
        session.headers["Referer"] = "https://servicewechat.com/wx88ccb2655c6720e2/18/page-frame.html"
        session.headers["content-type"] = "application/json;charset=UTF-8;"
        payload = {
            "accessToken": userData,  # openid
            "course": resp["classId"],  # 大学习期数
            "subOrg": userlist[userData]['subOrg'],  # 手机号
            "nid": userlist[userData]['nid'],  # 组织代码
            "cardNo": userlist[userData]['cardNo'],  # 姓名
        }
        result = session.post(url, data=json.dumps(payload))
        if result.json()['code'] == 200:
            print(userlist[userData]['cardNo'], "学习成功")  # 模拟学习
        else:
            print(userlist[userData]['cardNo'], "学习失败")
        time.sleep(5)

    print(f"成功完成{len(userlist)}次学习, 请等待后台数据刷新")
