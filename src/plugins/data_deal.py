from nonebot import on_command, require
from pathlib import Path

require("nonebot_plugin_localstore")
from nonebot_plugin_localstore import get_data_file
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, GROUP_ADMIN, GROUP_OWNER
from nonebot.params import ArgPlainText, CommandArg
from nonebot.permission import SUPERUSER
from nonebot.log import logger
import sqlite3, os

hashmap = []
get_sql_path: Path = get_data_file("nonebot_plugin_date_name", "name_data.db")

if not Path.exists(get_sql_path):
    logger.warning("检测到数据库不存在")
    conn_name = sqlite3.connect(get_sql_path)
    conn_name.cursor().execute(f"CREATE TABLE `name` (`group` int(16), `qq` text, `name` text)")
    conn_name.commit()
else:
    conn_name = sqlite3.connect(get_sql_path)
    logger.success("数据库加载成功")

d = conn_name.cursor().execute("SELECT * from `name`").fetchmany()
for i in d:
    hashmap.append([i[0], i[1], i[2]])

ans = {}
a = on_command("开启时间名字", permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER)
t = on_command("关闭时间名字", permission=GROUP_OWNER | GROUP_ADMIN | SUPERUSER)


@a.handle()
async def _(event: GroupMessageEvent, args: Message = CommandArg()):
    if event.group_id in ans:
        ans[event.group_id].append([event.get_user_id()])
    else:
        ans[event.group_id] = [[event.get_user_id()]]
    m = str(args).split()
    for i in range(1, len(m), 2):
        ans[event.group_id].append([m[i - 1], m[i]])
    await a.send("请输入你的昵称")


@a.got("ww")
async def _(event: GroupMessageEvent, n: str = ArgPlainText("ww")):
    for i in ans[event.group_id]:
        if event.get_user_id() in i:
            i.append(n)
        if len(i) == 2:
            if await check(int(i[0]), event.group_id):
                for i_ in range(0, len(hashmap)):
                    if hashmap[i_][0] == event.group_id and hashmap[i_][1] == int(event.get_user_id()):
                        hashmap.pop(i_)
                conn_name.cursor().execute(
                    f'UPDATE `name` SET name="{i[1]}" WHERE qq={int(i[0])} and `group` = {event.group_id}')
            else:
                conn_name.cursor().execute(
                    f'insert into `name` (`group`,`qq`,`name`) values({event.group_id},{int(i[0])},"{i[1]}")')
            hashmap.append([event.group_id, int(i[0]), i[1]])
        else:
            continue
    ans[event.group_id] = []
    conn_name.commit()
    await a.finish("ok")


@t.handle()
async def _(event: GroupMessageEvent):
    if await check(int(event.get_user_id()), event.group_id):
        conn_name.cursor().execute(
            f"DELETE FROM `name` WHERE qq = {int(event.get_user_id())} and `group` = {event.group_id};")
        conn_name.commit()
    for i in range(0, len(hashmap)):
        if hashmap[i][0] == event.group_id and hashmap[i][1] == int(event.get_user_id()):
            hashmap.pop(i)
            break
    await t.finish("退出完毕")


async def check(qq, group):
    f = conn_name.cursor().execute(f"SELECT * from `name` WHERE `qq`={qq} and `group` = {group};").fetchone()
    if not f:
        return False
    else:
        return True
