import time
from urllib.parse import quote

import requests
import json

stuInfo = [  # 数据结构 ["学号", "姓名", "openId", "组织代码", "userId"]
    ["1140001", "野兽", "oc2p4795ba88ecda2", "N0088001145141919", "1"],
    ["1140002", "先辈", "oc2p43fd381f722d1", "N0088001145141919", "2"],
    ["1140003", "哼哼哼", "oc2p470b9e1f41dc7", "N0088001145141919", "3"],
]


def sign():
    # 批量为userid写入用户信息
    url = "http://www.jxqingtuan.cn/pub/pub/vol/member/updateUserInfo"
    for userData in stuInfo:
        session = requests.session()
        session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309055b) XWEB/6973 Flue",
            "openid": userData[2],
        }
        payload = f"type=0&userId={userData[4]}&name={userData[1]}&sex=&birthday=&levelId_1={userData[3][:5]}&levelId_2={userData[3][:9]}&levelId={userData[3][:13]}&subLevelId={userData[3]}&xuehao=&address=&phone={userData[0]}"
        print(session.post(url, params=payload).text)
        time.sleep(1)


if __name__ == "__main__":
    # sign() # 仅需要在最初使用脚本时执行一次, 目的是确保信息正确填写, 否则学习记录无法被正常插入

    resp = json.loads(requests.get("http://www.jxqingtuan.cn/pub/pub/vol/volClass/current").text)["result"]  # 用于获取最新一期的学习信息

    for userData in stuInfo:
        session = requests.session()
        session.headers = {
            "Proxy-Connection": "keep-alive",
            "Content-Length": "",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309055b) XWEB/6973 Flue",
            "openid": userData[2],
            "content-type": "application/x-www-form-urlencoded",
            "Accept": "*/*",
            "Origin": "http://www.jxqingtuan.cn",
            "Referer": "http://www.jxqingtuan.cn/html/",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh",
        }

        url = "http://www.jxqingtuan.cn/pub/pub/vol/member/addScoreInfo" # 获得学习积分的url
        mid = f"check=1&type=3&title=%E9%9D%92%E5%B9%B4%E5%A4%A7%E5%AD%A6%E4%B9%A0&url={quote(resp['uri'])}&openid={userData[2]}&userId={userData[4]}" # 传入学习链接, openId, userId
        session.post(url, data=mid)  # 模拟获得积分
        time.sleep(1)

        url = "http://www.jxqingtuan.cn/pub/pub/vol/volClass/join?accessToken="+ userData[2] # 记录学习记录的url
        session.headers["Referer"] = "http://www.jxqingtuan.cn/html/?accessToken=" + userData[2]
        session.headers["content-type"] = "application/json;charset=UTF-8;"
        payload = {
            "accessToken": userData[2],  # openid
            "course": resp["id"],  # 大学习期数
            "subOrg": userData[0],  # 学号
            "nid": userData[3],  # 组织代码
            "cardNo": userData[1],  # 姓名
        }
        print(session.post(url, data=json.dumps(payload)).text)  # 模拟学习
        time.sleep(1)
