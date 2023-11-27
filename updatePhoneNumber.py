import random
import time

import requests
from urllib.parse import quote
import newVersionDxx

if __name__ == '__main__':
    stuInfo = newVersionDxx.stuInfo

    url = "https://www.jxqingtuan.cn/pub/pub/vol/member/updateUserInfo"

    for item in stuInfo:
        session = requests.session()
        session.headers = {
            # "Proxy-Connection": "keep-alive",
            # "Content-Length": "",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309055b) XWEB/6973 Flue",
            "content-type": "application/x-www-form-urlencoded",
            "Accept": "*/*",
            "openid": item,
            "Authorization": item,
            "Referer": "https://servicewechat.com/wx88ccb2655c6720e2/18/page-frame.html",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh",
        }

        infoGetUrl = "https://www.jxqingtuan.cn/pub/pub/vol/member/info?accessToken=" + item
        infoData = session.get(infoGetUrl).json()['vo']

        updateDate = f"type=0&userId={infoData['id']}&name={quote(infoData['username'])}&sex=&birthday=&levelId_1={infoData['areaid1']}&levelId_2={infoData['areaid2']}&levelId={infoData['areaid3']}&subLevelId={infoData['areaid4']}&xuehao=&address=&phone=138{random.randrange(10000000, 99999999)}"

        resp = session.post(url, data=updateDate)
        print(resp.text)
        time.sleep(1)

