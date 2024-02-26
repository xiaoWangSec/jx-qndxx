# 添加新用户工具

import json
from appletYouthStudy import sessionBuilder

stuInfo = [""]


if __name__ == '__main__':
    print("添加新用户工具")

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

    if len(userlist) != len(stuInfo):  # 新初始化或者新增了用户
        for item in stuInfo:
            if item not in userlist:
                print(f"{item} - 不存在的用户, 尝试读取数据并写入")
                url = "https://www.jxqingtuan.cn/api-client/user/getUserDail?accessToken="
                session = sessionBuilder(item)
                resp = session.get(url + item).json()['data']
                xm = resp["username"]
                zz = resp["areaid4"]
                userid = resp["id"]
                openid = resp["openid"]

                userlist[item] = {
                    "cardNo": xm,  # 姓名
                    "nid": zz,  # 组织
                    "userid": userid,  # 编号
                }
            # else:
            #     print("已存在的用户 跳过")

        with open("users.json", 'w', encoding='utf-8') as writer:
            json.dump(userlist, writer, indent=4)  # 处理完的json写入
