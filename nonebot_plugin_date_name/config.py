import json,os
from nonebot import on_command,get_driver
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.log import logger
from nonebot.params import ArgPlainText

def duqu_1():
    try:
        with open("./datename/1.json","r+",encoding="utf-8") as f:
            return json.load(f)
    except(FileNotFoundError):
        return []

def duqu_2():
    try:
        with open("./datename/2.json","r+",encoding="utf-8") as f:
            return json.load(f)
    except(FileNotFoundError):
        return {}

global user
global id_nickname
user = duqu_1()
id_nickname = duqu_2()

start = on_command("开启时间名字",priority=5)
@start.handle()
async def start_Service():
    await start.send("请输入你的昵称")

@start.got("nickname")
async def strat_2(event:GroupMessageEvent,a: str = ArgPlainText("nickname")):
    o = []
    o.append(str(event.group_id))
    o.append(str(event.user_id))
    user.append(str(o))
    logger.success("datenowname:开启成功")
    id_nickname[str(event.user_id)] = a
    await start.finish("ok")

end = on_command("关闭时间名字",priority=5)
@end.handle()
async def end_service(event:GroupMessageEvent):
    try:
        o = []
        o.append(str(event.group_id))
        o.append(str(event.user_id))
        user.remove(str(o))
        id_nickname.pop(str(event.user_id))
    except(ValueError):
        logger.error("datenowname:关闭失败 指定用户不存在")
        pass
    else:
        logger.success("datenowname:关闭现在时间昵称成功！")
        await end.finish("关闭现在时间昵称成功！")

data_upload = on_command("datename更新缓存",priority=9)
@data_upload.handle()
async def upload_data():
    if os.path.exists("datename") == False:
        os.mkdir("datename")
    with open("./datename/1.json","w+",encoding="utf-8") as g:
        g.write(str(user))
        g.close()
    with open("./datename/2.json","w+",encoding="utf-8") as g:
        g.write(str(id_nickname).replace("'",'"'))
        g.close()
    await data_upload.finish("更新缓存完成")

    