from nonebot import on_command
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.params import ArgPlainText
from collections import Counter
import sqlite3,os

hashmap =  []# 预处理

conn_name = sqlite3.connect(os.path.dirname(__file__)+"/name.db")
d = conn_name.cursor().execute("SELECT * from `name`").fetchmany()
for i in d:
    hashmap.append([i[0],i[1],i[2]])
    

ans = {}
a = on_command("开启时间名字")
t = on_command("关闭时间名字")

@a.handle()
async def _(event:GroupMessageEvent):
    ans[event.get_user_id()] = [event.group_id]
    await a.send("请输入你的昵称")

@a.got("ww")
async def _(event: GroupMessageEvent,n: str  = ArgPlainText("ww")):
    ans[event.get_user_id()].append(n)
    if await check(int(event.get_user_id()),event.group_id):
        conn_name.cursor().execute(f'UPDATE `name` SET name="{n}" WHERE qq={int(event.get_user_id())} and `group` = {event.group_id}')
    else:
        conn_name.cursor().execute(f'insert into `name` (`group`,`qq`,`name`) values({event.group_id},{int(event.get_user_id())},"{n}")')
    hashmap.append([event.group_id,int(event.get_user_id()),n])
    conn_name.commit()
    await a.finish("ok")

@t.handle()
async def _(event: GroupMessageEvent):
    if await check(int(event.get_user_id()),event.group_id):
        conn_name.cursor().execute(f"DELETE FROM `name` WHERE qq = {int(event.get_user_id())} and `group` = {event.group_id};")
        conn_name.commit()
    for i in range(0,len(hashmap)):
        if hashmap[i][0] == event.group_id and hashmap[i][1] == int(event.get_user_id()):
            hashmap.pop(i)
            break
    await t.finish("退出完毕")

async def check(qq,group):
    f = conn_name.cursor().execute(f"SELECT * from `name` WHERE `qq`={qq} and `group` = {group};").fetchone()
    if not f: return False
    else: return True
