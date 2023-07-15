# jx-qndxx
简单易用的江西省青年大学习自动化脚本

# 特性
* 重构后的代码仅需填入`openid`即可完成学习, 无需其他信息
* 支持班级批量学习, 一键完成大学习
* 执行完脚本后, 后台数据会在15分钟内同步

# `newVersionDxx.py`使用方法

## `openId`的获取
打开抓包软件后打开大学习界面, 仅需要停留在首页, 此时查看抓包结果

找到`http://www.jxqingtuan.cn/pub/pub/vol/member/info?accessToken=xxx`的抓包结果, 应该形如

![](https://s3.bmp.ovh/imgs/2023/07/16/1e43ab91b04778ca.png)

`accessToken`后的字符串即为需要的`openid`

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
## 使用方法
* 获取`openId`
* 打开`newVersionDxx.py`, 找到第`8`行的`stuInfo`, 将`openid`填入其中, 例如
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
* 将信息填完并测试脚本可以正常工作
* 在宝塔面板添加一个计划任务, 工作时间为`每周一, 12点30分执行`
