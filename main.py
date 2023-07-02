import time

import requests
import json

session = requests.session()
session.headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"
}

id = ""
title = ""

def getCurrent():
    url = "http://www.jxqingtuan.cn/pub/pub/vol/volClass/current"
    res = session.get(url).text
    jsfy = json.loads(res)
    global id
    global title
    id = jsfy['result']['id']
    title = jsfy['result']['title']

if __name__ == '__main__':
    getCurrent()
    url = "http://www.jxqingtuan.cn/pub/pub/vol/volClass/join?accessToken="
    
    payload = {"course":id,"subOrg":None,"nid":"_____CHANGE_____","cardNo":""}
    name = ["_____CHANGE_____", "_____CHANGE_____", "_____CHANGE_____"]

    for i in name:
        payload['cardNo'] = i
        print(session.post(url, data=json.dumps(payload)).text)
        time.sleep(1)

    
