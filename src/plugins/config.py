from nonebot import get_plugin_config
from pydantic import BaseModel


class Config(BaseModel):
    """配置时间格式"""
    time_format: str = "%A %p %Y-%m-%d %H:%M"


config = get_plugin_config(Config)

get_time_format: str = config.time_format
