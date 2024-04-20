# 2024完全迁移至小程序的重构版本
# 兼容上一个版本的users.json数据格式

"""
重构备注
    所有请求需要带请求头openid和authorization, 填入的是openid, 这两个字段的值是可以一样的, 兼容老版openid
    用户信息接口: https://www.jxqingtuan.cn/api-client/user/getUserDail?accessToken={OPENID}
    记录学习接口1: https://www.jxqingtuan.cn/api-client/classRecord/learningRecords
    记录学习接口2: https://www.jxqingtuan.cn/api-client/userScore/addOrUpdateCourse
    期数查看接口: https://www.jxqingtuan.cn/api-client/classRecord/retakesList

"""
import json
import time

import requests


# stuInfo = [""]

def getDataFromFile():
    try:
        with open("users.json", 'r', encoding='utf-8') as reader:
            try:
                userlist = json.load(reader)
            except:
                userlist = json.loads("{}")
    except FileNotFoundError:
        print("user.json文件不存在, 已新建")
        with open("users.json", 'w') as file:
            file.write("{}")
            userlist = json.loads("{}")
    return userlist


def sessionBuilder(openid: str):
    session = requests.session()
    session.headers = {
        "Connection": "keep-alive",
        # "Content-Length": "",
        "Authorization": openid,
        "charset": "utf-8",
        "requesttype": "",
        "openid": openid,
        "content-type": "application/json",
        "Accept-Encoding": "gzip,compress,br,deflate",
        "Referer": "https://servicewechat.com/wx88ccb2655c6720e2/51/page-frame.html",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/043807 Mobile Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/4G Language/zh_CN MicroMessenger/6.6.1.1220(0x26060135) NetType/4G Language/zh_CN miniProgram"
    }
    # session.verify = False # 如果需要开代理或者抓包请将其设置为False
    return session


def retakesList(r: requests.Session):
    # 这个接口用来获取学习信息, 期数, 时长, 等
    url = "https://www.jxqingtuan.cn/api-client/classRecord/retakesList"
    result = r.get(url).json()['data']['JxgqtClassVoList']
    lst = []  # 存放未学习期数

    for item in result:
        if item['learn'] == False:  # 还没学的
            per = {"d": int(item['duration']), "i": int(item['id'])}  # 单个未学习信息
            lst.append(per)
    return lst


def learningRecords(r: requests.Session, openid: str, yid: int):
    # 记录学习第一条请求
    url = "https://www.jxqingtuan.cn/api-client/classRecord/learningRecords"
    payload = {"accessToken": openid, "course": yid, "retakes": 0}
    req = r.post(url, data=json.dumps(payload))
    if req.status_code == 200:
        return True
    else:
        return False


def addOrUpdateCourse(r: requests.Session, userid: str, orgid: str, duration: int, yid: int):
    # 记录学习第二条请求
    url = "https://www.jxqingtuan.cn/api-client/userScore/addOrUpdateCourse"
    payload = {"studyTime": duration + 100, "classId": yid, "userId": userid, "areaId1": orgid[:5],
               "areaId2": orgid[:9], "areaId3": orgid[:13], "areaId4": orgid, "status": 1, "retakes": 0}
    req = r.post(url, data=json.dumps(payload))
    if req.status_code == 200:
        return True
    else:
        return False


if __name__ == '__main__':
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

    # if len(userlist) != len(stuInfo):  # 新初始化或者新增了用户
    #     for item in stuInfo:
    #         if item not in userlist:
    #             print(f"{item} - 不存在的用户, 尝试读取数据并写入")
    #             url = "https://www.jxqingtuan.cn/api-client/user/getUserDail?accessToken="
    #             session = sessionBuilder(item)
    #             resp = session.get(url + item).json()['data']
    #             xm = resp["username"]
    #             zz = resp["areaid4"]
    #             userid = resp["id"]
    #             openid = resp["openid"]
    #
    #             userlist[item] = {
    #                 "cardNo": xm,  # 姓名
    #                 "nid": zz,  # 组织
    #                 "userid": userid,  # 编号
    #             }
    #         # else:
    #         #     print("已存在的用户 跳过")
    #
    #     with open("users.json", 'w', encoding='utf-8') as writer:
    #         json.dump(userlist, writer, indent=4)  # 处理完的json写入
    userlist = getDataFromFile()
    print(f"成功处理{len(userlist)}条记录, 开始执行学习操作")
    for userData in userlist:
        time.sleep(1)
        session = sessionBuilder(userData)
        print(userlist[userData]['cardNo'], end=" - ")

        try:
            tot = retakesList(session)
            print(f"获取到{len(tot)}条未学习记录")
        except:
            print("获取学习信息失败, 已跳过")
            continue

        for item in tot:
            time.sleep(1)
            print(userlist[userData]['cardNo'], end=" - ")
            try:
                step1 = learningRecords(session, openid=userData, yid=item['i'])
                time.sleep(1)
                step2 = addOrUpdateCourse(session, userid=userlist[userData]['userid'],
                                          orgid=str(userlist[userData]['nid']), yid=item['i'], duration=item['d'])
                time.sleep(1)
                print(f"第{item['i']}期学习成功!")
            except:
                print(f"第{item['i']}期学习出现异常!")
        print(userlist[userData]['cardNo'], "- 学习完成")
    print(f"成功完成{len(userlist)}次学习, 请等待后台数据刷新")
