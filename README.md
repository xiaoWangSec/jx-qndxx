# jx-qndxx
简单易用的江西省青年大学习自动化脚本

# 优化计划（11月30日前完成）

1. 增加自动重试功能: 请求失败时自动重试

2. 整合修改手机号功能: 初始化时如果不存在手机号自动添加

3. 优化信息组织方式: 调整现有信息保存方式，新增用户不必每次删除文件


# 系统怎么双改了?😅😅😅

2023.11.21: 修改记录学习接口, 最新脚本调用小程序接口

(虽然小程序接口使用的是新openid, 但是老的似乎也可以用)

另外服务器似乎不稳定, 已修改sleep时间为5s, 如果运行时出现404等代码建议多次运行并调高延时

数据每天凌晨两点更新

<s>1. 大学习链接和期数的接口已修改</s>

<s>2. 现已强制要求填入手机号并带格式验证</s>

# 特性
* 重构后的代码仅需填入`openid`即可完成学习, 无需其他信息
* 支持班级批量学习, 一键完成大学习
* 执行完脚本后, 后台数据会在15分钟内同步
* 附带批量修改手机号脚本

# 使用方法目录
* [1. openId的获取方法](#获取openId)
* [2. 批量获取openId](#批量获取openId)
* [3. 批量修改手机号](#批量修改手机号)
* [4. 批量大学习](#批量大学习)

# 获取openId
打开抓包软件后打开大学习界面, 仅需要停留在首页, 此时查看抓包结果

找到`http://www.jxqingtuan.cn/pub/pub/vol/member/info?accessToken=xxx`的抓包结果, 应该形如

![](https://s3.bmp.ovh/imgs/2023/07/16/1e43ab91b04778ca.png)

`accessToken`后的字符串即为需要的`openid`

# 批量获取openId

## 如果你是团支书则可以在大学习管理后台界面抓包获得全班同学的`openid`
参考步骤如下

![](https://s3.bmp.ovh/imgs/2023/07/16/4b88762d3798587c.png)

![](https://s3.bmp.ovh/imgs/2023/07/16/de9363ba40593a21.png)
```
import json

if __name__ == '__main__':

    DATA_HERE = """

"""

    for item in json.loads(DATA_HERE)['list']:
        print(f'"{item["userid"]}",')
```

# 批量修改手机号
2023.10之后需要填写手机号才能进入学习界面, 可以使用脚本批量修改
* 请在`newVersionDxx.py`中将`userId`填入`stuInfo`中, 多条请使用列表的格式填入
* 运行`updatePhoneNumber.py`即可自动获取`userId`并修改随即手机号

# 批量大学习

* 请确保已经填写好正确的openId, 并且已经运行过一次`updatePhoneNumber.py`(如果网络波动导致错误请重试)
* 打开`newVersionDxx.py`, 找到`stuInfo`, 将`openid`填入其中, 例如
```
stuInfo = [ # 仅需要在此填入openid即可
    "oc2p4795ba88ecda1",
    "oc2p4795ba88ecda2",
    "oc2p4795ba88ecda3"
]
```
* 运行脚本, 首次执行(`userlist`文件不存在)时, 会自动请求获取所需信息并写入本地
* 学习记录将在15分钟内显示在后台

# 最佳实践
<s>* 将信息填完并测试脚本可以正常工作
* 在宝塔面板添加一个计划任务, 工作时间为`每周一, 12点30分执行`
</s>
系统修改频繁 建议每次手动执行脚本