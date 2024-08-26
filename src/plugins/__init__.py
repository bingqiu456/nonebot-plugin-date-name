from nonebot import get_bot, require

require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler
from nonebot.plugin import PluginMetadata
from datetime import datetime
from . import data_deal
from . import config

__plugin_meta__ = PluginMetadata(
    name="群昵称时间",
    description="让你的群昵称显示出当前时间，并且支持多人使用",
    usage=(
        "指令 /开启时间名字 [id] [name] ...\n"
        "/关闭时间名字\n"
        "开启时间名字后面可以加qq号和昵称 可以多人一起用 例如 /开启时间名字 10001 示例 10002 示例2\n"
        "切记 不要在后面加自己的QQ号 否则会出现bug\n"
        "如果自己也想用可以回复自己想要的昵称 和原来的一样\n"
        "如果自己不想用 只是帮别人改 到了输入昵称这一步可以输入-1"
    ),
    type="application",
    config=config.Config,
    homepage="https://github.com/bingqiu456/nonebot-plugin-date-name",
)


@scheduler.scheduled_job('interval', seconds=5)
async def _():
    try:
        bot = get_bot()
        for a in data_deal.hashmap:
            group_id = a[0]
            user_id_2 = a[1]
            now_time = f"{a[2]} " + str(datetime.now().strftime(config.get_time_format))
            await bot.call_api(
                "set_group_card", **{
                    'group_id': group_id,
                    'user_id': user_id_2,
                    'card': now_time})
    except ValueError:
        pass
