import os
import json

cache_dir = './server/usercache.json'
def get_uuid(name: str):
    if not os.path.exists(cache_dir):
        return None
    with open(cache_dir, 'r') as f:
        user_cache = json.load(f)
    for item in user_cache:
        if item['name'] == name:
            return item['uuid']
    return None
        
def get_name(uuid: str):
    if not os.path.exists(cache_dir):
        return None
    with open(cache_dir, 'r') as f:
        user_cache = json.load(f)
    for item in user_cache:
        if item['uuid'] == uuid:
            return item['name']
    return None

if __name__ == '__main__':
    uuid = get_uuid('GuBai_ovo')
    print(uuid)
    name = get_name(uuid)
    print(name)