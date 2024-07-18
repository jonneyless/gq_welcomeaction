import asyncio
from telethon import TelegramClient, events, Button
import db
import db_redis
from dbpool import OPMysql


async def make_cache(group_tg_id):
    opm = OPMysql()

    sql = "select user_id as tg_id, username, firstname, lastname from group_admin where chat_id = '%s'" % group_tg_id

    result = opm.op_select_all(sql)

    opm.dispose()

    admins = result

    await db_redis.group_admin_one_set(group_tg_id, admins)
    
    return admins


async def index():
    print("test...")
    group_tg_id = -1001839355001
    data = await make_cache(group_tg_id)
    
    print(data)
    
    
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(index())
    loop.close()