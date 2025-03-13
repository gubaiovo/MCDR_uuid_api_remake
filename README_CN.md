# MCDR_uuid_api_remake
本插件为UUID API重制版，[原作UUID API链接：https://github.com/AnzhiZhang/MCDReforgedPlugins/tree/master/src/uuid_api](https://github.com/AnzhiZhang/MCDReforgedPlugins/tree/master/src/uuid_api)

本插件使用了原api获取 正版/离线服务器 uuid 的所有代码

### 重制版额外特性：

1. 增加更多命令，便于管理uuid。
2. 所有已获取的 uuid 存放到 `uuid.json` 数据文件中统一管理。
3. 增加 `get_name(uuid)` 函数，可以由uuid获取玩家名。(获取范围为 `uuid.json` `usercache.json`)

### 本插件uuid获取流程 (如果获取失败则执行下一步)：

1. 读取插件数据文件 `uuid.json` 
2. 读取  `usercache.json` ，若读取成功，存放到 `uuid.json` 
3. 调用原api，若获取成功，存放到 `uuid.json` 
4. 使用 `玩家名+时间戳` 的哈希值(sha256)的前50位作为伪uuid，存放到 `uuid.json` 

### 配置文件

参考原作

**注：如果服务器中有皮肤站这类介于正版与离线之间的玩家，或基岩版玩家，无需修改配置文件，对于这些玩家将使用哈希值作为伪uuid**

> 你不需要考虑服务器正盗版问题, 会自己判断
>
> 如果使用了 `BungeeCord` 并开启了正版验证, 或实际的UUID与 `server.properties` 中的 `online-mode` 并不匹配
>
> 将插件的 `manual_mode` 手动模式设置为一个布尔值即可覆盖 `server.properties` 的在线模式

### 命令

除了 `!!uar` `!!uar help` ，其他命令只能在控制台使用

具体使用方法请参考  `!!uar` 或 `!!uar help`

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