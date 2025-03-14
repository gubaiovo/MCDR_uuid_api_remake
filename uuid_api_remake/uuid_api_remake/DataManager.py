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
    def __init__(self, mojang_online_mode: bool,online_api: str, using_offline_api: bool, offline_api: str):

        self.mojang_online_mode = mojang_online_mode
        self.online_api = online_api
        self.using_offline_api = using_offline_api
        self.offline_api = offline_api

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
                    # 若usercache.json也不存在，则尝试从api获取uuid
                    try:
                        uuid = get_uuid_from_api(
                            name=name,
                            mojang_online_mode=self.mojang_online_mode,
                            online_api=self.online_api,
                            use_offline_api=self.using_offline_api,
                            offline_api=self.offline_api
                            )
                    except Exception as e:
                        pass
                    if uuid is None:
                        uuid = hash_name_with_timestamp(name)
                        source = 'generated'
                    else:
                        source = 'api'
                else:
                    source = 'usercache.json'

                uuid_data = self.remove_same_uuid(uuid, name, uuid_data)
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
                    else:
                        return None
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

            
    def remove_same_uuid(self, uuid: str, new_name: str, uuid_data):
        keys_to_remove = []
        for key, value in uuid_data.items():
            if value == uuid and key != new_name:
                keys_to_remove.append(key)
        for key in keys_to_remove:
            uuid_data.pop(key)
        return uuid_data
    
    def test(self):
        test_name = 'test_name'
        test_uuid = 'test_uuid'
        # 测试get_uuid
        test_get_uuid_from_uuid_json = None
        test_get_uuid_from_usercache = None
        test_get_uuid_from_api = None
        test_get_uuid_from_generated = None
        if self.checkJson(self.uuid_path):
            with open(self.uuid_path, 'r') as file:
                uuid_data = json.load(file)
            test_get_uuid_from_uuid_json = uuid_data.get(test_name)
            test_get_uuid_from_usercache = get_uuid_from_usercache(test_name)
            test_get_uuid_from_api = get_uuid_from_api(
                                name=test_name,
                                mojang_online_mode=self.mojang_online_mode,
                                online_api=self.online_api,
                                use_offline_api=self.using_offline_api,
                                offline_api=self.offline_api
                                )
            test_get_uuid_from_generated = hash_name_with_timestamp(test_name)
        print('test_get_uuid_from_uuid_json:', test_get_uuid_from_uuid_json)
        print('test_get_uuid_from_usercache:', test_get_uuid_from_usercache)
        print('test_get_uuid_from_api:', test_get_uuid_from_api)
        print('test_get_uuid_from_generated:', test_get_uuid_from_generated)
        # 测试get_name
        test_get_name = None
        if self.checkJson(self.uuid_path):
            with open(self.uuid_path, 'r') as file:
                uuid_data = json.load(file)
            test_get_name = self.get_name(test_uuid)
        print('test_get_name:', test_get_name)        
        
    

