from nonebot import get_bot
from nonebot_plugin_apscheduler import scheduler
from . import config
from datetime import datetime

@scheduler.scheduled_job('interval', seconds=5)
async def _():
        try:
            bot = get_bot()
            for a in config.hashmap:
                group_id = a[0]
                user_id_2 = a[1]
                now_time = f"{a[2]} "+str(datetime.now().strftime("%A %p %Y-%m-%d %H:%M"))
                await bot.call_api(
                    "set_group_card",**{
                    'group_id':group_id,
                    'user_id':user_id_2,
                    'card':now_time})
        except(ValueError):
            pass
