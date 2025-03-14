# -*- coding: utf-8 -*-
import os
from typing import Union
from mcdreforged.api.all import *
from uuid_api_remake.DataManager import DataManager

def tr(key, *args):
    return ServerInterface.get_instance().tr(f"uuid_api_remake.{key}", *args)

def command_register(server: ServerInterface):
    builder = SimpleCommandBuilder()
    builder.command('!!uar', get_help)
    builder.command('!!uar help', get_help)
    builder.command('!!uar <name>', get_uuid_in_console)
    builder.command('!!uar list', list_uuid_in_console)
    builder.command('!!uar del <name>', delete_uuid_in_console)
    builder.command('!!uar change uuid <name> <new_uuid>', change_uuid_in_console)
    builder.command('!!uar change name <uuid> <new_name>', change_name_in_console)
    builder.arg('name', Text)
    builder.arg('uuid', Text)
    builder.arg('new_uuid', Text)
    builder.arg('new_name', Text)
    builder.register(server)

def get_help(source: CommandSource):
    source.reply(tr("help_message"))

def get_uuid_in_console(source: CommandSource, context: CommandContext):
    if not source.is_console:
        source.reply(tr("error.not_console"))
    data = getDataManager()
    name = context['name']
    uuid, uuid_source= data.get_uuid(name)
    source.reply(f'§c{name} -> {uuid}, {uuid_source}')

def delete_uuid_in_console(source: CommandSource, context: CommandContext):
    if not source.is_console:
        source.reply(tr("error.not_console"))
    data = getDataManager()
    name = context['name']
    uuid = data.delete_uuid(name)
    if uuid is None:
        source.reply(tr("error.no_name"))
    else:
        source.reply(f'{tr('delete_uuid')} §c{name} -> {uuid}')
    
    
def change_uuid_in_console(source: CommandSource, context: CommandContext):
    if not source.is_console:
        source.reply(tr("error.not_console"))
    data = getDataManager()
    name = context['name']
    new_uuid = context['new_uuid']
    old_uuid = data.change_uuid(name, new_uuid)
    if old_uuid is None:
        source.reply(tr("error.no_name"))
    else:
        source.reply(f'{tr("change_uuid")} §c{name}: {old_uuid} -> {new_uuid}')
    

def change_name_in_console(source: CommandSource, context: CommandContext):
    if not source.is_console:
        source.reply(tr("error.not_console"))
    data = getDataManager()
    uuid = context['uuid']
    new_name = context['new_name']
    old_name = data.change_name(uuid, new_name)
    if old_name is None:
        source.reply(tr("error.no_uuid"))
    else:
        source.reply(f'{tr("change_name")} §c{uuid}: {old_name} -> {new_name}')
    
def list_uuid_in_console(source: CommandSource):
    if not source.is_console:
        source.reply(tr("error.not_console"))
    data = getDataManager()
    uuid_list = data.list_uuid()
    if uuid_list is None:
        source.reply(tr("error.Json_empty"))
    else:
        if len(uuid_list) == 0:
            source.reply(tr("list_uuid.empty"))
        else:
            source.reply(tr("list_uuid.header"))
            for entry in uuid_list:
                source.reply(f'§c{entry["name"]} -> {entry["uuid"]}')
            

def get_uuid(name: str) -> str:
    data = getDataManager()
    return data.get_uuid(name)[0]


def get_name(uuid: str) -> str:
    data = getDataManager()
    return data.get_name(uuid)[0]

def test_api() -> bool:
    data = getDataManager()
    return data.test()

# Adapted from code by AnzhiZhang: https://github.com/AnzhiZhang/MCDReforgedPlugins/tree/master/src/uuid_api
class Config(Serializable):
    mojang_online_mode: bool = True
    online_api: str = 'https://api.mojang.com/users/profiles/minecraft/'
    use_offline_api: bool = True
    offline_api: str = 'http://tools.glowingmines.eu/convertor/nick/'

properties_path = os.path.join('server', 'server.properties')
mojang_online_mode = True
online_api = 'https://api.mojang.com/users/profiles/minecraft/'
use_offline_api = True
offline_api = 'http://tools.glowingmines.eu/convertor/nick/'
config: Config

def on_load(server: PluginServerInterface, old):
    command_register(server)
    global config, mojang_online_mode, online_api, use_offline_api, offline_api
    config = server.load_config_simple(
        'config.json',
        target_class=Config
    )
    try:
        mojang_online_mode, online_api, use_offline_api, offline_api = get_config()
    except Exception as e:
        server.logger.error(tr('error.load_config_error'), e)
    server.logger.debug(tr('now_online_status'), mojang_online_mode)

def get_config():
    global config
    return config.mojang_online_mode, config.online_api, config.use_offline_api, config.offline_api

def getDataManager():
    global mojang_online_mode, online_api, use_offline_api, offline_api
    return DataManager(mojang_online_mode, online_api, use_offline_api, offline_api)

