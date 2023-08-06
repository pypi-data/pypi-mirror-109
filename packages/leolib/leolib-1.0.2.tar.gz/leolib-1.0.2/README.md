# LEOLIB 利昂图书馆座位预约系统API

## 如何导入

`from leolib import User, get_day, get_time`

## 如何使用

```python
 from leolib import User, get_day, get_time
 # 用户对象
 user = User("username", "password", "zw.example.edu.cn")
 # 查看用户信息
 print(user.get_user_info())
```