# -*- coding: utf-8 -*-
import requests


def online_uuid(name):
    url = f'https://api.mojang.com/users/profiles/minecraft/{name}'
    r = get_try(url)
    if r is None:
        return None
    else:
        return r['id']


def offline_uuid(name):
    url = f'http://tools.glowingmines.eu/convertor/nick/{name}'
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


def get_uuid(name: str, online_mode: bool): 
    if online_mode:
        uuid = online_uuid(name)
    else:
        uuid = offline_uuid(name)
    return uuid