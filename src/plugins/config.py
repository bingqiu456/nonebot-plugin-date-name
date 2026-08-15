from nonebot import get_plugin_config
from pydantic import BaseModel


class Config(BaseModel):
    """配置时间格式"""
    time_format: str = "%A %p %Y-%m-%d %H:%M"
    set_self_card: bool = False  # 是否将机器人自己在群里的群名片设置为当前时间
    self_card_name: str = ""  # 机器人自己群名片的时间前缀，留空则只显示时间


config = get_plugin_config(Config)

get_time_format: str = config.time_format
set_self_card: bool = config.set_self_card
self_card_name: str = config.self_card_name
