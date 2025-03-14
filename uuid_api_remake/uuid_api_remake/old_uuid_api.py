# Adapted from code by AnzhiZhang: https://github.com/AnzhiZhang/MCDReforgedPlugins/tree/master/src/uuid_api
# -*- coding: utf-8 -*-
import requests


def online_uuid(name, online_api):
    url = f'{online_api}{name}'
    r = get_try(url)
    if r is None:
        return None
    else:
        return r['id']


def offline_uuid(name, offline_api):
    url = f'{offline_api}{name}'
    r = get_try(url)
    if r is None:
        return None
    else:
        return r['offlineuuid']


def get_try(url):
    for i in range(0, 5):
        try:
            return requests.get(url).json()
        except:
            pass
    return None


def get_uuid(name: str, mojang_online_mode: bool, online_api: str, offline_api: str, use_offline_api: bool): 
    if mojang_online_mode:
        uuid = online_uuid(name, online_api)
    else:
        if use_offline_api:
            uuid = offline_uuid(name, offline_api)
        else:
            return None
    return uuid
