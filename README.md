## 介绍
这是一个小米路由器[官方固件]后台的API整合  
可以实现程序控制端口转发等自动化操作  
路由器型号：AC2100  

## 运行环境
1.Python3

## 示例代码
```python
from miwifi.miwifi import Api
if __name__ == '__main__':
    # 在网页[登录界面]代码里查找'var Encrypt ='"
    key = 'a2ffa5c9be07488bbxxxxxxxxxxxxxxx'
    # 运行程序 设备的MAC
    deviceId = 'xx:xx:xx:xx'
    # 路由器地址
    addr = 'http://192.168.1.1'
    # 管理员密码
    password = 'passwd'
	
    #获取API对象 自动登入获取stok
    api = Api(key=key, deviceId=deviceId, addr=addr, password=password)
    #获取单个端口转发并打印出来
    for data in api.api_xqnetwork_portforward_list1()['list']:
        print("ip:%s:%s -> port:%s"%(data['destip'],data['srcport'],data['destport']))
    #添加一个端口转发
    api.api_xqnetwork_add_redirect("test",1,50,"192.168.1.114",50)
    #应用端口转发更改
    api.api_xqnetwork_redirect_apply()
    #删除端口转发
    api.api_xqnetwork_delete_redirect(50,1)
    api.api_xqnetwork_redirect_apply()

    #未封装接口 GET同理
    api.post('url',{'参数': 'parm'})
```

## 已知问题
概率出现401错误，只能重新运行程序，暂未发现解决方案。