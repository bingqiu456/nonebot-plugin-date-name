import json
from nonebot import get_bot
from nonebot_plugin_apscheduler import scheduler
from . import config
from datetime import datetime




@scheduler.scheduled_job('interval', seconds=5)
async def _():
        bot = get_bot()
        for a in config.user:
            user_id = json.loads(str(a).replace("'",'"'))
            group_id = user_id[0]
            user_id_2 = user_id[1]
            now_time = str(config.id_nickname[user_id_2])+str(" ")+str(datetime.now().strftime("%A %p %Y-%m-%d %H:%M"))
            await bot.call_api(
                "set_group_card",**{
                'group_id':group_id,
                'user_id':user_id_2,
                'card':now_time})
            
            
