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
    name = context['name']
    uuid, uuid_source= get_uuid(name)
    source.reply(f'§c{name} -> {uuid}, {uuid_source}')

def delete_uuid_in_console(source: CommandSource, context: CommandContext):
    if not source.is_console:
        source.reply(tr("error.not_console"))
    data = DataManager(online_mode)
    name = context['name']
    uuid = data.delete_uuid(name)
    if uuid is None:
        source.reply(tr("error.no_name"))
    else:
        source.reply(f'{tr('delete_uuid')} §c{name} -> {uuid}')
    
    
def change_uuid_in_console(source: CommandSource, context: CommandContext):
    if not source.is_console:
        source.reply(tr("error.not_console"))
    data = DataManager(online_mode)
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
    data = DataManager(online_mode)
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
    data = DataManager(online_mode)
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
    data = DataManager(online_mode)
    return data.get_uuid(name)[0]


def get_name(uuid: str) -> str:
    data = DataManager(online_mode)
    return data.get_name(uuid)[0]




class Config(Serializable):
    online_mode: Union[bool, None] = None

properties_path = os.path.join('server', 'server.properties')
online_mode = True
config: Config

def on_load(server: PluginServerInterface, old):
    command_register(server)
    global config, online_mode
    config = server.load_config_simple(
        'config.json',
        target_class=Config
    )
    online_mode = get_online_mode(server)
    server.logger.debug(tr('now_online_status'), online_mode)

def get_online_mode(server):
    global config
    # 手动设置覆盖
    server.logger.info(config.online_mode)
    if config.online_mode is not None and isinstance(config.online_mode, bool):
        server.logger.info(tr('use_setting_status'), config.online_mode)
        return config.online_mode

    # 读取服务器配置
    if not os.path.isfile(properties_path):
        server.logger.error(tr('error.no_server_properties'))
        return True
    else:
        with open(properties_path) as f:
            for i in f.readlines():
                if 'online-mode' in i:
                    server.logger.debug(tr('find_config'), i)
                    server_properties_config = i.split('=')[1].replace('\n', '')
                    break
        if server_properties_config == 'true':
            return True
        elif server_properties_config == 'false':
            return False
        else:
            server.logger.error(tr('error.invalid_server_properties'))
            return True

        

