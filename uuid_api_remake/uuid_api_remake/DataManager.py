# -*- coding: utf-8 -*-
from mcdreforged.api.all import *
import os
import json
import hashlib
import time
from uuid_api_remake.usercache import get_uuid as get_uuid_from_usercache
from uuid_api_remake.usercache import get_name as get_name_from_usercache
from uuid_api_remake.old_uuid_api import get_uuid as get_uuid_from_api

# def tr(key, *args):
#     return ServerInterface.get_instance().tr(f"chat_with_ai.{key}", *args)

def hash_name_with_timestamp(name: str) -> str:
    timestamp = str(int(time.time()))
    combined_string = name + timestamp
    hash_object = hashlib.sha256(combined_string.encode())
    hash_hex = hash_object.hexdigest()
    return hash_hex[:60]
source = None
class DataManager:
    def __init__(self, online_mode: bool):
        self.online_mode = online_mode
        self.uuid_path = './config/uuid_api_remake/uuid.json'
        if not os.path.exists(self.uuid_path):
            with open(self.uuid_path, 'w') as file:
                json.dump({}, file)


    def get_uuid(self, name: str) -> str:
        if not os.path.exists(self.uuid_path):
            with open(self.uuid_path, 'w') as file:
                json.dump({}, file)
        # 读取uuid.json
        if self.checkJson(self.uuid_path):
            with open(self.uuid_path, 'r') as file:
                uuid_data = json.load(file)
                uuid = uuid_data.get(name, None)
            if uuid is None:
                # 若uuid不存在，则尝试从usercache.json获取
                uuid = get_uuid_from_usercache(name)
                if uuid is None:
                    # 若usercache.json也不存在，则尝试从mojang获取uuid
                    try:
                        uuid = get_uuid_from_api(name, online_mode=self.online_mode)
                        source = 'mojang'
                    except Exception as e:
                        # 若获取失败，则生成uuid
                        uuid = hash_name_with_timestamp(name)
                        source = 'generated'
                else:
                    source = 'usercache.json'

                uuid_data[name] = uuid
                with open(self.uuid_path, 'w') as file:
                    json.dump(uuid_data, file, indent=4)
            else:
                source = 'uuid.json'
            if uuid is not None:
                return uuid, source
            else:
                return None, None
    
    def get_name(self, uuid: str) -> str:
        if not os.path.exists(self.uuid_path):
            with open(self.uuid_path, 'w') as file:
                json.dump({}, file)
        # 读取uuid.json
        if self.checkJson(self.uuid_path):
            with open(self.uuid_path, 'r') as file:
                uuid_data = json.load(file)
            # 翻转字典，key为uuid，value为name
            name = None
            for key, value in uuid_data.items():
                if value == uuid:
                    name = key
                    source = 'uuid.json'
                    break
            if name is None:
                # 若uuid.json中不存在，则尝试从usercache.json获取
                name = get_name_from_usercache(uuid)
                if name is None:
                    source = 'unknown'
                else:
                    source = 'usercache.json'
            else:
                source = 'uuid.json'
            return name, source


    def delete_uuid(self, name: str) -> bool:
        if not os.path.exists(self.uuid_path):
            return None
        if self.checkJson(self.uuid_path):
            with open(self.uuid_path, 'r') as file:
                uuid_data = json.load(file)
                if uuid_data.get(name) is not None:
                    uuid = uuid_data[name]
                    del uuid_data[name]
                    with open(self.uuid_path, 'w') as file:
                        json.dump(uuid_data, file, indent=4)
                    return uuid
            return None

    def change_uuid(self, name: str, new_uuid: str) -> bool:
        if not os.path.exists(self.uuid_path):
            return None
        if self.checkJson(self.uuid_path):
            with open(self.uuid_path, 'r') as file:
                uuid_data = json.load(file)
                if uuid_data.get(name) is not None:
                    old_uuid = uuid_data[name]
                    uuid_data[name] = new_uuid
                    with open(self.uuid_path, 'w') as file:
                        json.dump(uuid_data, file, indent=4)
                    return old_uuid, new_uuid
            return None
    
    def change_name(self, uuid: str, new_name: str) -> bool:
        if not os.path.exists(self.uuid_path):
            return None
        if self.checkJson(self.uuid_path):
            with open(self.uuid_path, 'r') as file:
                uuid_data = json.load(file)
                for key, value in uuid_data.items():
                    if value == uuid:
                        uuid_data[new_name] = uuid_data.pop(key)
                        with open(self.uuid_path, 'w') as file:
                            json.dump(uuid_data, file, indent=4)
                        return key
            return None

    def checkJson(self, path: str) -> bool:
        try:
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
                if not content.strip():  # 检查文件内容是否为空
                    print("Json file is empty, initializing...")
                    with open(path, 'w', encoding='utf-8') as file:
                        json.dump({}, file, indent=4)
                    return False
                json_data = json.loads(content)
            return True
        except Exception as e:
            print("Json file is invalid, error: " + str(e))
            return False

    def list_uuid(self) -> list:
        if not os.path.exists(self.uuid_path):
            return None
        if self.checkJson(self.uuid_path):
            with open(self.uuid_path, 'r') as file:
                uuid_data = json.load(file)
                result_list=[]
                for key, value in uuid_data.items():
                    result_list.append({'name': key, 'uuid': value})
                return result_list
        return None

    

