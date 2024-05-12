# jx-qndxx
简单易用的江西省青年大学习自动化脚本

# 推荐使用GUI版本
<s>💩山代码 能用就行</s>

直接运行`GUI.py`即可

点击`添加新用户`后输入`openid`可添加新用户, 一行一个

双击某行学习该条记录, 右键该记录可以删除该用户

点击`开始学习`可批量学习


# 获取单个openId
## 仅供参考 思路类似
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


# 最佳实践
打开GUI 手动运行
