# UUID API REMAKE
本插件为UUID API重制版，[原作UUID API链接：https://github.com/AnzhiZhang/MCDReforgedPlugins/tree/master/src/uuid_api](https://github.com/AnzhiZhang/MCDReforgedPlugins/tree/master/src/uuid_api)

### 本插件uuid获取流程 (如果获取失败则执行下一步)：

1. 判断服务器正版/离线
2. 
    (1). 正版：
        1. 读取 usercache.json，失败则下一步
        2. 调用 API
    (2). 离线
        1. 读取 offline_uuid.json，失败则下一步
        2. 本地计算 uuid，保存到 offline_uuid.json
    

### 配置文件

```json
{
    "online_api": "https://api.mojang.com/users/profiles/minecraft/{}",
    "mojang_online_mode_fallback": true,
    "permissions": {
        "help": 3,
        "get": 3
    }
}
```

**mojang_online_mode_fallback**: 当插件无法判断服务器正版/离线时，由该项决定使用正版/离线 uuid 获取方式  
**online_api**: 获取正版 uuid 的 API  
**permissions**: 权限管理，数值参考 [MCDReforgedPermissions](https://docs.mcdreforged.com/zh-cn/latest/permission.html)  

### 命令

具体使用方法请参考 `!!uar help`

### API使用方法

获取玩家名对应的uuid：

```python
import uuid_api_remake

name = ... # str
uuid = uuid_api_remake.get_uuid(name)
print(uuid)
```

获取uuid对应的玩家名(获取范围为 `uuid.json` `usercache.json`)

```python
import uuid_api_remake

uuid = ... # str
name = uuid_api_remake.get_name(uuid)
print(name)
```