# -*- coding: utf-8 -*-
import os
import json
import requests
from typing import Optional
import uuid
import threading
from mcdreforged.api.all import *
import hashlib



class Config(Serializable):
    online_api: str = 'https://api.mojang.com/users/profiles/minecraft/{}'
    mojang_online_mode_fallback: bool = True
    permissions: dict = {
        "help": 3,
        "get": 3
    }
    
config: Config
is_online_mode: bool = True 
offline_uuid_path: str 
offline_uuid_lock = threading.Lock()

def _read_usercache(identifier: str, find_key: str, return_key: str) -> Optional[str]:
    usercache_path = os.path.join('server', 'usercache.json')
    if not os.path.exists(usercache_path):
        return None
    try:
        with open(usercache_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for entry in data:
            if entry.get(find_key) == identifier:
                return entry.get(return_key)
    except (json.JSONDecodeError, IOError):
        return None
    return None

def _get_from_offline_cache(name: str) -> Optional[str]:
    global offline_uuid_path
    with offline_uuid_lock:
        try:
            if not os.path.exists(offline_uuid_path):
                return None
            with open(offline_uuid_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get(name)
        except (json.JSONDecodeError, IOError):
            return None
def _save_to_offline_cache(name: str, new_uuid: str):
    global offline_uuid_path
    with offline_uuid_lock:
        try:
            data = {}
            if os.path.exists(offline_uuid_path):
                with open(offline_uuid_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if content:
                        data = json.loads(content)
            data[name] = new_uuid
            with open(offline_uuid_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error saving to offline cache: {e}")
            
def _generate_offline_uuid(username: str) -> str:
    name = "OfflinePlayer:" + username
    
    md5 = hashlib.md5(name.encode("utf-8")).digest()
    ba = bytearray(md5)
    ba[6] = (ba[6] & 0x0f) | 0x30
    ba[8] = (ba[8] & 0x3f) | 0x80
    return str(uuid.UUID(bytes=bytes(ba)))
        

def _get_online_uuid_from_api(name: str) -> Optional[str]:
    global is_online_mode, config
    try:
        url = config.online_api.format(name)
        print(url)
        response = requests.get(url, timeout=5)
        response.raise_for_status() 
        return str(uuid.UUID(response.json().get('id')))
    except requests.RequestException:
        return None
    except json.JSONDecodeError:
        return None


def get_uuid(name: str) -> Optional[str]:
    if is_online_mode:
        # usercache.json 
        uuid = _read_usercache(name, 'name', 'uuid')
        if uuid is not None:
            return uuid
        # API
        return _get_online_uuid_from_api(name)
    else:
        uuid = _get_from_offline_cache(name)
        if uuid is not None:
            return uuid
        uuid = _generate_offline_uuid(name)
        _save_to_offline_cache(name, uuid)
        return uuid

def get_name(uuid: str) -> Optional[str]:
    global is_online_mode, offline_uuid_path
    name = _read_usercache(uuid, 'uuid', 'name')
    if name is not None:
        return name
    if not is_online_mode:
        with offline_uuid_lock:
            try:
                if not os.path.exists(offline_uuid_path):
                    return None
                with open(offline_uuid_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for name_entry, uuid_entry in data.items():
                        if uuid_entry == uuid:
                            return name_entry
            except (json.JSONDecodeError, IOError):
                return None
    return None


def _determine_online_mode(server: PluginServerInterface):
    global is_online_mode, config
    properties_path = os.path.join('server', 'server.properties')
    
    found_in_properties = False
    if os.path.exists(properties_path):
        try:
            with open(properties_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip().startswith('online-mode='):
                        value = line.split('=', 1)[1].strip()
                        is_online_mode = value.lower() == 'true'
                        server.logger.info(f"从 server.properties 中检测到 online-mode: {is_online_mode}")
                        found_in_properties = True
                        break
        except Exception as e:
            server.logger.warning(f"读取 server.properties 失败: {e}，将使用插件配置")

    if not found_in_properties:
        is_online_mode = config.mojang_online_mode_fallback
        server.logger.info(f"未在 server.properties 中找到 online-mode，使用插件配置: {is_online_mode}")

def command_register(server: PluginServerInterface):
    global config
    builder = SimpleCommandBuilder()
    require = Requirements()
    level_dict = config.permissions
    builder.command('!!uar help', help_message)
    builder.command('!!uar get <name>', get_uuid_in_game)
    builder.arg('name', Text)
    
    for literal in level_dict:
        permission = level_dict[literal]

        builder.literal(literal).requires(
            require.has_permission(permission),
            failure_message_getter=lambda err, p=permission: "lack_permission"
        )

    builder.register(server)

def on_load(server: PluginServerInterface, old):
    global config, offline_uuid_path
    config = server.load_config_simple('config.json', target_class=Config)
    offline_uuid_path = server.get_data_folder() + '/offline_uuid.json'
    if not os.path.exists(offline_uuid_path):
        with open(offline_uuid_path, 'w') as f:
            json.dump({}, f)
    _determine_online_mode(server)

    command_register(server)

def get_uuid_in_game(source: CommandSource, context: dict):
    name = context['name']
    source.reply(f"查询 §e{name}§r UUID...")
    uuid = get_uuid(name)
    if uuid:
        message = RText(f"§c{name} §a->§r §b{uuid}").h("§a点击复制UUID到剪贴板").c(RAction.copy_to_clipboard, uuid)
        source.reply(message)
    else:
        source.reply(f"§c查询失败: 无法找到玩家 §e{name}§c 的 UUID。")
        
def help_message(source: CommandSource, context: dict):
    source.reply("!!uar help - 查看帮助信息。")
    source.reply("!!uar <name> - 查询 Minecraft 玩家的 UUID。")
