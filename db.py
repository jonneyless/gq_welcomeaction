import datetime
import time

import assist
import db_redis
from assist import get_current_time, htmlspecialchars_php, is_number, get_today_time, get_day_int
from dbpool import OPMysql


# ======================================================================================================================

async def group_one_by_num(num):
    opm = OPMysql()

    sql = "select id, flag, title, chat_id, bot_approve_link, opening_at, business_type, recent_dispute from `groups` where group_num = %s and (flag = 2 or flag = 4) and status_in = 1 limit 1" % num

    result = opm.op_select_one(sql)

    opm.dispose()

    return result


async def group_one(group_tg_id):
    opm = OPMysql()

    sql = "select * from `groups` where chat_id = '%s' limit 1" % group_tg_id

    result = opm.op_select_one(sql)

    opm.dispose()

    return result


async def group_flush(group_tg_id):
    opm = OPMysql()

    sql = "select id, chat_id as tg_id, title, flag, trade_type, title, welcome_info, welcome_status, people_limit, limit_one_time, welcome_true_status, welcome_false_status, business_detail_type, business_type, open_status, group_num from `groups` where chat_id = '%s' limit 1" % group_tg_id

    result = opm.op_select_one(sql)

    opm.dispose()

    if result is not None:
        await db_redis.group_set(group_tg_id, result)

    return result
    
    
async def groups_get():
    opm = OPMysql()

    sql = "select id, chat_id as tg_id from `groups` where flag = 2 or flag = 4"

    result = opm.op_select_all(sql)

    opm.dispose()

    return result


async def group_one_by_url(url):
    opm = OPMysql()

    sql = "select id, flag from `groups` where url = '%s' limit 1" % url

    result = opm.op_select_one(sql)

    opm.dispose()

    return result


async def group_save(group_tg_id, title):
    opm = OPMysql()

    sql = "insert into `groups`(chat_id, title, flag, created_at, status_in) values('%s', '%s', '%s', '%s', '%s')" % (
        group_tg_id, title, 2, get_current_time(), 1)

    result = opm.op_update(sql)

    opm.dispose()

    return result


async def group_set_flag(chat_id, flag=2):
    opm = OPMysql()

    sql = "update `groups` set flag = '%s', status_in = 1 where chat_id = %s" % (flag, chat_id)

    result = opm.op_update(sql)

    opm.dispose()

    return result
    
    
async def group_set_bot_link(data_id, link):
    opm = OPMysql()

    sql = "update `groups` set bot_approve_link = '%s' where id = %s" % (link, data_id)

    result = opm.op_update(sql)

    opm.dispose()

    return result
    
    
async def group_set_open_status(data_id, open_status=1):
    opm = OPMysql()

    sql = "update `groups` set open_status = '%s' where id = %s" % (open_status, data_id)

    result = opm.op_update(sql)

    opm.dispose()

    return result
    
    
async def group_set_title(id, title):
    opm = OPMysql()

    sql = "update `groups` set title = '%s' where id = %s" % (title, id)

    result = opm.op_update(sql)

    opm.dispose()

    return result


async def group_set_welcome_info(id, welcome_info):
    opm = OPMysql()

    sql = "update `groups` set welcome_info = '%s', welcome_status = 1 where id = %s" % (welcome_info, id)

    result = opm.op_update(sql)

    opm.dispose()

    return result


async def group_close_welcome_info(id):
    opm = OPMysql()

    sql = "update `groups` set welcome_status = 2 where id = %s" % id

    result = opm.op_update(sql)

    opm.dispose()

    return result


async def group_init(data_id, title):
    opm = OPMysql()

    sql = "update `groups` set title = '%s', yajin = 0, yajin_u = 0, yajin_m = 0, yajin_all = 0, yajin_all_u = 0, yajin_all_m = 0 where id = %s" % (title, data_id)

    result = opm.op_update(sql)

    opm.dispose()

    return result
    
    
# ======================================================================================================================

async def user_one(user_tg_id):
    opm = OPMysql()

    sql = "select id, tg_id, username, firstname, lastname, fullname from users_new where tg_id = '%s' limit 1" % user_tg_id

    result = opm.op_select_one(sql)

    opm.dispose()

    return result


async def user_one_by_username(username):
    opm = OPMysql()

    sql = "select id, tg_id, username, firstname, lastname, fullname from users_new where username = '%s' order by id desc limit 1" % username

    result = opm.op_select_one(sql)

    opm.dispose()

    return result


async def user_save(sender):
    opm = OPMysql()

    sql = "insert into users_new(tg_id, username, firstname, lastname, fullname) values('%s', '%s', '%s', '%s', '%s')" % (
        sender["tg_id"], sender["username"], sender["firstname"], sender["lastname"], sender["fullname"])

    result = opm.op_update(sql)

    opm.dispose()

    return result


async def user_update(id, sender):
    opm = OPMysql()

    sql = "update users_new set username = '%s', firstname = '%s', lastname = '%s', fullname = '%s' where id = %s" % (
        sender["username"], sender["firstname"], sender["lastname"], sender["fullname"], id)

    result = opm.op_update(sql)

    opm.dispose()

    return result


async def user_update_tgid(tg_id, sender):
    opm = OPMysql()

    sql = "update users_new set username = '%s', firstname = '%s', lastname = '%s', fullname = '%s' where tg_id = '%s'" % (
        sender["username"], sender["firstname"], sender["lastname"], sender["fullname"], tg_id)

    result = opm.op_update(sql)

    opm.dispose()

    return result
    
    
async def user_set_private(user_tg_id):
    opm = OPMysql()

    sql = "update users_new set has_private = 1 where tg_id = '%s'" % user_tg_id

    result = opm.op_update(sql)

    opm.dispose()

    return result
    
    
# ======================================================================================================================

async def user_group_single(user_tg_id):
    opm = OPMysql()

    sql = "select id, user_tg_id, created_at from user_group_new where user_tg_id = '%s' order by id asc" % user_tg_id

    result = opm.op_select_one(sql)

    opm.dispose()

    return result


async def user_group_one(group_tg_id, user_tg_id):
    opm = OPMysql()

    sql = "select id, group_tg_id, user_tg_id, status from user_group where group_tg_id = '%s' and user_tg_id = '%s' limit 1" % (
        group_tg_id, user_tg_id)

    result = opm.op_select_one(sql)

    opm.dispose()

    return result


async def user_group_save(group_tg_id, user_tg_id):
    opm = OPMysql()

    sql = "insert into user_group_new(group_tg_id, user_tg_id, created_at) values('%s', '%s', '%s')" % (group_tg_id, user_tg_id, get_current_time())

    result = opm.op_update(sql)

    opm.dispose()

    return result


async def user_group_set(group_tg_id, user_tg_id, created_at):
    opm = OPMysql()

    sql = "update user_group_new set created_at = '%s' where group_tg_id = '%s' and user_tg_id = '%s'" % (created_at, group_tg_id, user_tg_id)

    print(sql)

    result = opm.op_update(sql)

    opm.dispose()

    return result


async def user_group_kick(group_tg_id, user_tg_id):
    obj = await user_group_one(group_tg_id, user_tg_id)
    if obj:
        opm = OPMysql()
    
        sql = "update user_group set status_in = 2, status = 3 where group_tg_id = '%s' and user_tg_id = '%s'" % (
            group_tg_id, user_tg_id)
    
        result = opm.op_update(sql)
    
        opm.dispose()
    
        return result
    else:
        await user_group_save(group_tg_id, user_tg_id)
    
    
async def user_group_restrict(group_tg_id, user_tg_id):
    opm = OPMysql()

    sql = "update user_group set status_in = 1, status = 4 where group_tg_id = '%s' and user_tg_id = '%s'" % (
        group_tg_id, user_tg_id)

    result = opm.op_update(sql)

    opm.dispose()

    return result
    
    
# ======================================================================================================================

async def cheat_one(user_tg_id):
    is_cheat_flag = None

    cheats_ids = await db_redis.cheat_get()
    if cheats_ids is None:
        cheats = await cheat_all()
        cheats_ids = []
        for cheat in cheats:
            cheat_tg_id = cheat["tgid"]
            if is_number(cheat_tg_id):
                cheats_ids.append(int(cheat_tg_id))

        await db_redis.cheat_set(cheats_ids)

    cheats_ids = set(cheats_ids)

    if int(user_tg_id) in cheats_ids:
        is_cheat_flag = True

    return is_cheat_flag


async def cheat_all():
    opm = OPMysql()

    sql = "select tgid from cheats"

    result = opm.op_select_all(sql)

    opm.dispose()

    return result


async def cheat_get(tgid):
    opm = OPMysql()

    sql = "select tgid from cheats where tgid = '%s'" % tgid

    result = opm.op_select_one(sql)

    opm.dispose()

    return result
    
    
async def cheat_save(user_tg_id, sender, reason):
    obj = await cheat_get(user_tg_id)
    if obj is not None:
        return
    
    opm = OPMysql()

    sql = "insert into cheats(tgid, username, firstname, lastname, reason, created_at) values('%s', '%s', '%s', '%s', '%s', '%s')" % (
        user_tg_id, sender["username"], sender["firstname"], sender["lastname"], reason, get_current_time())

    result = opm.op_update(sql)

    opm.dispose()

    return result


async def official_one_full(user_tg_id):
    opm = OPMysql()

    sql = "select * from offical_user where tg_id = '%s' limit 1" % user_tg_id

    result = opm.op_select_one(sql)

    opm.dispose()

    return result


async def cheat_one_no_cache(user_tg_id):
    opm = OPMysql()

    sql = "select id from cheats where tgid = '%s'" % user_tg_id

    result = opm.op_select_one(sql)

    opm.dispose()

    return result
    
    
async def cheat_special_one_no_cache(user_tg_id):
    opm = OPMysql()

    sql = "select id from cheats_special where tgid = '%s'" % user_tg_id

    result = opm.op_select_one(sql)

    opm.dispose()

    return result
    
    
async def official_one(user_tg_id):
    is_official_flag = None

    officials_ids = await db_redis.official_get()
    officials_ids = None
    if officials_ids is None:
        officials = await official_get_flag()
        officials_ids = []
        for official in officials:
            official_tg_id = official["tg_id"]
            if is_number(official_tg_id):
                officials_ids.append(int(official_tg_id))
        await db_redis.official_set(officials_ids)

    officials_ids = set(officials_ids)

    if int(user_tg_id) in officials_ids:
        is_official_flag = True

    return is_official_flag


async def official_get_firstname(user_tg_id):
    opm = OPMysql()

    sql = "select firstname from offical_user where tg_id ='%s'" % user_tg_id

    result = opm.op_select_one(sql)

    opm.dispose()

    if result is None:
        return ""

    return result['firstname']


async def official_get_flag():
    opm = OPMysql()

    sql = "select tg_id from offical_user"

    result = opm.op_select_all(sql)

    opm.dispose()

    return result


async def official_one_by_username(username):
    opm = OPMysql()

    sql = "select id from offical_user where username ='%s'" % username

    result = opm.op_select_one(sql)

    opm.dispose()

    return result
    
    
async def white_one(user_tg_id):
    is_white_flag = None

    whites_ids = await db_redis.white_get()
    if whites_ids is None:
        whites = await white_get()
        whites_ids = []
        for white in whites:
            white_tg_id = white["tg_id"]
            if is_number(white_tg_id):
                whites_ids.append(int(white_tg_id))
        await db_redis.white_set(whites_ids)

    whites_ids = set(whites_ids)

    if int(user_tg_id) in whites_ids:
        is_white_flag = True

    return is_white_flag


async def white_get():
    opm = OPMysql()

    sql = "select tg_id from white_user"

    result = opm.op_select_all(sql)

    opm.dispose()

    return result


async def white_user_bot_one(tg_id):
    opm = OPMysql()

    sql = "select id from white_user_bot where tg_id = '%s'" % tg_id

    result = opm.op_select_one(sql)

    opm.dispose()

    return result
    
    
async def session_user_save(group_tg_id, user_tg_id):
    opm = OPMysql()

    sql = "insert into session_users(chat_id, user_id, created_at) values('%s', '%s', '%s')" % (
        group_tg_id, user_tg_id, get_current_time())

    result = opm.op_update(sql)

    opm.dispose()

    return result


# ======================================================================================================================

async def group_admin_boss_one(user_tg_id):
    opm = OPMysql()

    sql = "select id from group_admin where user_id = '%s' and custom_title = '本公群老板，小心骗子假冒'" % user_tg_id

    result = opm.op_select_one(sql)

    opm.dispose()

    return result
    
    
async def group_boss_pwd_one(user_tg_id):
    opm = OPMysql()

    sql = "select id from group_boss_pwd where user_tg_id = '%s'" % user_tg_id

    result = opm.op_select_one(sql)

    opm.dispose()

    return result


async def group_boss_pwd_set(obj, pwd):
    opm = OPMysql()
    
    sql = "insert into group_boss_pwd(user_tg_id, firstname, lastname, fullname, username, pwd, created_at) values('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (obj["tg_id"], obj["firstname"], obj["lastname"], obj["fullname"], obj["username"], pwd, get_current_time())

    result = opm.op_update(sql)

    opm.dispose()

    return result
    
    
async def group_admin_get_no_cache(user_tg_id):
    opm = OPMysql()

    sql = "select chat_id as group_tg_id from group_admin where user_id = '%s'" % user_tg_id

    result = opm.op_select_all(sql)

    opm.dispose()

    return result
    
    
async def group_admin_one(group_tg_id, user_tg_id):
    is_admin_flag = None

    admins_ids = await db_redis.group_admin_get()
    if admins_ids is None:
        admins = await group_admin_all()
        admins_ids = []
        for admin in admins:
            if is_number(admin["group_tg_id"]) and is_number(admin["user_tg_id"]):
                temp_str = str(admin["group_tg_id"]) + str(admin["user_tg_id"])
                admins_ids.append(temp_str)

        await db_redis.group_admin_set(admins_ids)

    admins_ids = set(admins_ids)

    group_admin_str = str(group_tg_id) + str(user_tg_id)
    if group_admin_str in admins_ids:
        is_admin_flag = True

    return is_admin_flag


async def group_admin_all():
    opm = OPMysql()

    sql = "select chat_id as group_tg_id, user_id as user_tg_id from group_admin"

    result = opm.op_select_all(sql)

    opm.dispose()

    return result


async def group_admin_get(group_tg_id):
    admins = await db_redis.group_admin_one_get(group_tg_id)
    if admins is None or True:
        opm = OPMysql()

        sql = "select user_id as tg_id, username, firstname, lastname, custom_title from group_admin where chat_id = '%s'" % group_tg_id

        print(sql)

        result = opm.op_select_all(sql)

        opm.dispose()

        admins = result

        await db_redis.group_admin_one_set(group_tg_id, admins)

    return admins


async def get_group_info(group_id):
    opm = OPMysql()

    sql = "select * from groups where id = '%s'" % group_id

    result = opm.op_select_one(sql)

    opm.dispose()

    return result


async def getBusiness():
    opm = OPMysql()

    sql = "select id, name from group_business"

    result = opm.op_select_all(sql)

    opm.dispose()

    data = {}
    for business in result:
        data[business['id']] = business['name']

    return data


async def getManages(chatId):
    opm = OPMysql()

    sql = "select user_id, username, status, custom_title from group_admin where chat_id = '%s'" % chatId

    result = opm.op_select_all(sql)

    opm.dispose()

    return result


async def get_group_official_admin(group_tg_id):
    officials = []
    group_admins = await group_admin_get(group_tg_id)
    for group_admin in group_admins:
        user_official = await official_one_full(group_admin["tg_id"])
        if user_official is not None:
            officials.append(group_admin)

    return officials


async def get_group_not_official_admin(group_tg_id):
    officials = []
    group_admins = await group_admin_get_now(group_tg_id)
    
    for group_admin in group_admins:
        group_admin["tg_id"] = group_admin["user_tg_id"]
        
        user_official = await official_one_full(group_admin["tg_id"])
        if user_official is None:
            officials.append(group_admin)

    return officials
    
    
async def group_admin_get_now(group_tg_id):
    opm = OPMysql()

    sql = "select user_id as user_tg_id, custom_title, fullname, username, status from group_admin where chat_id = '%s'" % group_tg_id

    result = opm.op_select_all(sql)

    opm.dispose()

    return result
    
    
async def group_admin_one_now(group_tg_id, user_tg_id):
    opm = OPMysql()

    sql = "select id from group_admin where chat_id = '%s' and user_id = '%s'" % (group_tg_id, user_tg_id)

    result = opm.op_select_one(sql)

    opm.dispose()

    return result
    
    
async def group_admin_update(data_id, obj):
    opm = OPMysql()

    sql = "update group_admin set username = '%s', firstname = '%s', lastname = '%s', updated_at = '%s' where id = %s" % (obj["username"], obj["firstname"], obj["lastname"], get_current_time(), data_id)

    result = opm.op_update(sql)

    opm.dispose()

    return result
    
    
async def group_admin_save(group_tg_id, obj, status):
    opm = OPMysql()

    sql = "insert into group_admin(chat_id, user_id, username, firstname, lastname, status, created_at) values('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
        group_tg_id, obj["tg_id"], obj["username"], obj["firstname"], obj["lastname"], status, get_current_time())

    result = opm.op_update(sql)

    opm.dispose()

    return result
    

async def group_admin_delete(group_tg_id, user_tg_id):
    opm = OPMysql()

    sql = "delete from group_admin where chat_id = '%s' and user_id = '%s'" % (group_tg_id, user_tg_id)

    result = opm.op_update(sql)

    opm.dispose()

    return result
    
    
async def group_admin_del(group_tg_id, user_tg_id):
    opm = OPMysql()

    sql = "delete from group_admin where chat_id = '%s' and user_id = '%s'" % (group_tg_id, user_tg_id)

    result = opm.op_update(sql)

    opm.dispose()

    return result
    
    
# ======================================================================================================================


async def message_first(group_tg_id, user_tg_id):
    val = await db_redis.message_first_get(group_tg_id, user_tg_id)
    if val is not None:
        return False
    else:
        await db_redis.message_first_set(group_tg_id, user_tg_id)
        
        return True
        
        
async def message_one(group_tg_id, message_tg_id):
    opm = OPMysql()

    selectSql = "select user_id as user_tg_id from msg where chat_id = '%s' and message_id = '%s'" % (group_tg_id, message_tg_id)

    result = opm.op_select_one(selectSql)

    opm.dispose()

    return result
    

async def message_get_day(group_tg_id, user_tg_id):
    opm = OPMysql()

    today_date = get_today_time()

    sql = "select id, message_id as message_tg_id from msg where chat_id = '%s' and user_id = '%s' and flag = 1 and created_at >= '%s' limit 300" % (
        group_tg_id, user_tg_id, today_date)

    result = opm.op_select_all(sql)

    opm.dispose()

    return result


async def message_save(group_tg_id, user_tg_id, message_tg_id, info, created_at):
    opm = OPMysql()

    info = htmlspecialchars_php(info)

    sql = "insert into msg(chat_id, user_id, message_id, info, created_at) values('%s', '%s', '%s', '%s', '%s')" % (
        group_tg_id, user_tg_id, message_tg_id, info, created_at)

    result = None
    try:
        result = opm.op_update(sql)
    except Exception:
        print(sql)

    opm.dispose()

    return result
    

async def message_delete(group_tg_id, message_tg_id):
    opm = OPMysql()

    sql = "update msg set flag = 2 where chat_id = '%s' and message_id = '%s'" % (group_tg_id, message_tg_id)

    result = opm.op_update(sql)

    opm.dispose()

    return result


# ======================================================================================================================

async def cheat_bank_get():
    opm = OPMysql()

    sql = "select num from cheat_bank"

    result = opm.op_select_all(sql)

    opm.dispose()

    return result


async def cheat_coin_get():
    opm = OPMysql()

    sql = "select address from cheat_coin"

    result = opm.op_select_all(sql)

    opm.dispose()

    return result


# ======================================================================================================================

async def restrict_word_get(type_str):
    type_str = int(type_str)

    opm = OPMysql()

    sql = "select name, level from words where type = %s" % type_str

    result = opm.op_select_all(sql)

    opm.dispose()

    return result


# ======================================================================================================================

async def config_get(key):
    opm = OPMysql()

    sql = "select val from config where `key` = '%s' limit 1" % key

    result = opm.op_select_one(sql)

    opm.dispose()

    return result

# ======================================================================================================================


async def reply_one(key):
    opm = OPMysql()

    sql = "select val from group_reply where `key` = '%s' limit 1" % key

    result = opm.op_select_one(sql)

    opm.dispose()

    return result


# ======================================================================================================================


async def log_delete_save(group_tg_id, user_tg_id, message_tg_id, reason):
    opm = OPMysql()

    sql = "insert into log_delete_message(group_tg_id, user_tg_id, message_tg_id, reason, created_at) values('%s', '%s', '%s', '%s', '%s')" % (group_tg_id, user_tg_id, message_tg_id, reason, get_current_time())

    result = opm.op_update(sql)

    opm.dispose()

    return result
    
    
async def log_restrict_save(group_tg_id, user_tg_id, until_data, reason):
    opm = OPMysql()

    sql = "insert into log_restrict_user(group_tg_id, user_tg_id, until_data, reason, created_at) values('%s', '%s', '%s', '%s', '%s')" % (group_tg_id, user_tg_id, until_data, reason, get_current_time())

    result = opm.op_update(sql)

    opm.dispose()

    return result
    
    
async def log_kick_save(group_tg_id, user_tg_id, reason):
    opm = OPMysql()

    sql = "insert into log_ban_user(group_tg_id, user_tg_id, reason, created_at) values('%s', '%s', '%s', '%s')" % (
        group_tg_id, user_tg_id, reason, get_current_time())

    result = opm.op_update(sql)

    opm.dispose()

    return result
    
    
# ======================================================================================================================


async def reply_text_get():
    data = await db_redis.reply_text_get()
    if data is not None and False:
        return data
    else:
        opm = OPMysql()
        
        sql = "select keyy, val from config_text where name = 'reply' limit 1"

        result = opm.op_select_one(sql)

        opm.dispose()

        data = None

        if result is not None:
            data = {
                "keyy": result["keyy"],
                "val": result["val"],
            }
            
            await db_redis.reply_text_set(data)

        return data
        

# ======================================================================================================================


async def group_word_get():
    data = await db_redis.group_word_get()
    if data is not None:
        return data
    else:
        opm = OPMysql()

        sql = "select name from group_word"

        result = opm.op_select_all(sql)

        opm.dispose()

        if result is not None:
            await db_redis.group_word_set(result)

        return result


async def search_sensitive_words():
    data = await db_redis.search_sensitive_words()
    if data is None:
        opm = OPMysql()

        sql = "select name from words where type = 11"

        result = opm.op_select_all(sql)

        opm.dispose()

        data = []
        if result is not None:
            for item in result:
                data.append(item['name'])

            await db_redis.search_sensitive_words_set(data)

    return data


async def search_reply_word_get():
    data = await db_redis.search_reply_word_get()
    if data is not None:
        return data
    else:
        opm = OPMysql()
    
        sql = "select `key` as keyy, val as vall from search_word_reply"
    
        result = opm.op_select_all(sql)
    
        opm.dispose()
        
        if result is not None:
            await db_redis.search_reply_word_set(result)
    
        return result
    
    
async def search_reply_word_one(name):
    opm = OPMysql()

    sql = "select val as vall from search_word_reply where `key` = '%s'" % name

    result = opm.op_select_one(sql)

    opm.dispose()

    return result
    
    
async def search_like_word_get():
    data = await db_redis.search_like_word_get()
    if data is not None:
        return data
    else:
        opm = OPMysql()
    
        sql = "select name from search_word_like"
    
        result = opm.op_select_all(sql)
    
        opm.dispose()
        
        if result is not None:
            await db_redis.search_like_word_set(result)
    
        return result
        
        
async def group_word_white_one(name):
    opm = OPMysql()

    sql = "select id from group_word_white where name = '%s'" % name

    result = opm.op_select_one(sql)

    opm.dispose()

    return result
        
        
async def search_word_get():
    data = await db_redis.search_word_get()
    if data is not None:
        return data
    else:
        opm = OPMysql()

        sql = "select name from search_word"

        result = opm.op_select_all(sql)

        opm.dispose()

        if result is not None:
            await db_redis.search_word_set(result)

        return result
        
        
# ======================================================================================================================

async def get_search_words_sql(text, is_title=1):
    search_words = await search_word_get()
    search_words_have = []
    for search_word in search_words:
        name = search_word["name"]
        
        if text.find(name) >= 0:
            search_words_have.append(name)

    search_like_words = await search_like_word_get()
    for search_like_word in search_like_words:
        search_like_word = search_like_word["name"]
        
        search_like_word_arr = search_like_word.split(",")
        has_like = False
        for search_like_word_text in search_like_word_arr:
            if len(search_like_word_text) > 0 and search_like_word_text == text:
                has_like = True
                break
        if has_like:
            for search_like_word_text in search_like_word_arr:
                if len(search_like_word_text) > 0:
                    search_words_have.append(search_like_word_text)
            break
    
    search_words_sql = ""
    if is_title != 1:
        search_words_sql = "rules like '%%%s%%'" % text
    else:
        search_words_sql = "title like '%%%s%%'" % text
        
    if len(search_words_have) > 0:
        if is_title != 1:
            search_words_sql = "(rules like '%%%s%%'" % text
        else:
            search_words_sql = "(title like '%%%s%%'" % text
        
        for name in search_words_have:
            if is_title != 1:
                search_words_sql += " or rules like '%%%s%%'" % name
            else:
                search_words_sql += " or title like '%%%s%%'" % name
        
        search_words_sql += ")"
        
    return search_words_sql


async def groups_search_by_title(text, page, sort="", page_len=20):
    search_words_sql = await get_search_words_sql(text)

    if sort != "":
        name_sort_sql = ""
        field = sort
        sortMode = 'asc'
        if sort[0:1] == '-':
            field = sort[1:len(sort)]
            sortMode = 'desc'

        sort_sql = "search_sort asc, " + field + " " + sortMode
    else:
        name_sort_sql = ", if(POSITION('%s' in title) > 0, 1, 0) as name_sort" % text
        sort_sql = "name_sort desc, search_sort asc, yajin desc"

    offset = (page - 1) * page_len
    
    opm = OPMysql()

    sql = "select open_status, chat_id as tg_id, title, flag, val as link %s from `groups` join group_reply on groups.group_num = group_reply.`key` where status_in = 1 and (flag = 2 or flag = 4) and %s order by %s limit %s,%s" % (name_sort_sql, search_words_sql, sort_sql, offset, page_len)

    result = opm.op_select_all(sql)
    
    opm.dispose()

    return result


async def groups_search_count_by_title(text):
    search_words_sql = await get_search_words_sql(text)
    
    opm = OPMysql()

    sql = "select count(chat_id) as count_num from `groups` join group_reply on groups.group_num = group_reply.`key` where status_in = 1 and (flag = 2 or flag = 4) and %s " % search_words_sql
    
    result = opm.op_select_one(sql)

    opm.dispose()

    return result


async def groups_search_by_rules(text, page, sort, page_len=20):
    search_words_sql = await get_search_words_sql(text, 2)

    if sort != "":
        name_sort_sql = ""
        field = sort
        sortMode = 'asc'
        if sort[0:1] == '-':
            field = sort[1:len(sort)]
            sortMode = 'desc'

        sort_sql = "search_sort asc, " + field + " " + sortMode
    else:
        name_sort_sql = ", if(POSITION('%s' in rules) > 0, 1, 0) as name_sort" % text
        sort_sql = "name_sort desc, search_sort asc, yajin desc"
    
    offeset = (page - 1) * page_len
    
    opm = OPMysql()

    sql = "select open_status, chat_id as tg_id, title, flag, val as link %s from `groups` join group_reply on groups.group_num = group_reply.`key` where status_in = 1 and (flag = 2 or flag = 4) and %s order by %s limit %s,%s" % (name_sort_sql, search_words_sql, sort_sql, offeset, page_len)

    print(sql)

    result = opm.op_select_all(sql)

    opm.dispose()

    return result
    
    
async def groups_search_count_by_rules(text):
    search_words_sql = await get_search_words_sql(text, 2)
    
    opm = OPMysql()

    sql = "select count(chat_id) as count_num from `groups` join group_reply on groups.group_num = group_reply.`key` where status_in = 1 and (flag = 2 or flag = 4) and %s" % search_words_sql

    result = opm.op_select_one(sql)

    opm.dispose()

    return result


async def groups_search_by_rules_limit(text, page_len):
    search_words_sql = await get_search_words_sql(text, 2)
    
    name_sort_sql = "if(POSITION('%s' in rules) > 0, 1, 0) as name_sort" % text
    
    opm = OPMysql()

    sql = "select open_status, chat_id as tg_id, title, flag, val as link, %s from `groups` join group_reply on groups.group_num = group_reply.`key` where status_in = 1 and (flag = 2 or flag = 4) and %s order by name_sort desc, search_sort asc, yajin desc limit %s" % (name_sort_sql, search_words_sql, page_len)
    
    result = opm.op_select_all(sql)

    opm.dispose()

    return result
    

# ======================================================================================================================


async def log_search_save(user_tg_id, text, text_original, data_count, typee = 1):
    return None
    # opm = OPMysql()

    # sql = "insert into log_search(user_tg_id, text, text_original, created_at, data_count, type) values('%s', '%s', '%s', '%s', '%s', '%s')" % (user_tg_id, text, text_original, get_current_time(), data_count, typee)

    # result = opm.op_update(sql)

    # opm.dispose()

    # return result


async def tg_user_new_one(user_tg_id):
    opm = OPMysql()

    sql = "select id from tg_user_new where tg_id = '%s'" % user_tg_id

    result = opm.op_select_one(sql)

    opm.dispose()

    return result

# ======================================================================================================================


async def word_ka_one(text):
    opm = OPMysql()

    sql = "select id from word_ka where name = '%s'" % text

    result = opm.op_select_one(sql)

    opm.dispose()

    return result
    
    
async def word_province_one(text):
    opm = OPMysql()

    sql = "select id from word_province where name = '%s'" % text

    result = opm.op_select_one(sql)

    opm.dispose()

    return result

    
# ======================================================================================================================

async def log_yanzheng_vip_save(user_tg_id, msg_tg_id, keyy, vall):
    opm = OPMysql()

    sql = "insert into log_yanzheng_vip(user_tg_id, msg_tg_id, created_at, keyy, vall) values('%s', '%s', '%s', '%s', '%s')" % (user_tg_id, msg_tg_id, get_current_time(), keyy, vall)

    result = opm.op_update(sql)

    opm.dispose()

    return result
    
    
# ======================================================================================================================

async def get_danbao_admins(admins):
    info_creator = ""
    info_jiaoyiyuan = ""
    info_boss = ""
    info_yewuyuan = ""
    
    for admin in admins:
        if admin["fullname"] is None:
            admin["fullname"] = ""
        if admin["username"] is None:
            admin["username"] = ""  
        if admin["custom_title"] is None:
            admin["custom_title"] = ""
        
        info_admin = "%s,%s,%s" % (admin["user_tg_id"], admin["fullname"], admin["username"])
        if admin["status"] == "creator":
            info_creator = info_admin
            
        if admin["fullname"].find("交易员") >= 0:
            is_official = await official_one(admin["user_tg_id"])
            if is_official is not None:
                info_jiaoyiyuan += info_admin
                info_jiaoyiyuan += "\n"
        if admin["custom_title"].find("本公群老板") >= 0:
            info_boss += info_admin
            info_boss += "\n"
        if admin["custom_title"].find("本公群业务员") >= 0:
            info_yewuyuan += info_admin
            info_yewuyuan += "\n"
        
    return info_creator, info_jiaoyiyuan, info_boss, info_yewuyuan
    

async def danbao_one(group_tg_id):
    opm = OPMysql()

    sql = "select * from log_danbao where group_tg_id = '%s' and status = 1" % group_tg_id

    result = opm.op_select_one(sql)

    opm.dispose()

    return result


async def danbao_save(group, admins):
    info_creator = ""
    info_jiaoyiyuan = ""
    info_boss = ""
    info_yewuyuan = ""
    
    info_creator, info_jiaoyiyuan, info_boss, info_yewuyuan = await get_danbao_admins(admins)
    now = get_current_time()
    yuefei_day = get_day_int()
        
    opm = OPMysql()

    sql = "insert into log_danbao(group_tg_id, title, num, info_creator, info_jiaoyiyuan, info_boss, info_yewuyuan, business_detail_type, yajin_u, yajin_m, yajin, yajin_all_u, yajin_all_m, yajin_all, created_at, yuefei_day) values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (group["tg_id"], group["title"], group["group_num"], info_creator, info_jiaoyiyuan, info_boss, info_yewuyuan, group["business_detail_type"], group["yajin_u"], group["yajin_m"], group["yajin"], group["yajin_all_u"], group["yajin_all_m"], group["yajin_all"], now, yuefei_day)

    result = opm.op_update(sql)

    opm.dispose()

    return result
    

async def danbao_update(log_danbao, group, admins):
    data_id = log_danbao["id"]

    opm = OPMysql()

    info_creator, info_jiaoyiyuan, info_boss, info_yewuyuan = await get_danbao_admins(admins)

    sql_update = "update log_danbao set title = '%s', num = '%s', info_creator = '%s', info_jiaoyiyuan = '%s', info_boss = '%s', info_yewuyuan = '%s', business_detail_type = '%s', yajin_u = '%s', yajin_m = '%s', yajin = '%s', yajin_all_u = '%s', yajin_all_m = '%s', yajin_all = '%s' where id = %s" % (group["title"], group["group_num"], info_creator, info_jiaoyiyuan, info_boss, info_yewuyuan, group["business_detail_type"], group["yajin_u"], group["yajin_m"], group["yajin"], group["yajin_all_u"], group["yajin_all_m"], group["yajin_all"],  data_id)
    result = opm.op_update(sql_update)
    
    sql_insert = "insert into log_danbao_change(data_id, group_tg_id, title, num, info_creator, info_jiaoyiyuan, info_boss, info_yewuyuan, business_detail_type, yajin_u, yajin_m, yajin, yajin_all_u, yajin_all_m, yajin_all, created_at, yuefei, yuefei_day, remark, tuoguan, status, changed_at) values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (data_id, group["tg_id"], group["title"], group["group_num"], info_creator, info_jiaoyiyuan, info_boss, info_yewuyuan, group["business_detail_type"], group["yajin_u"], group["yajin_m"], group["yajin"], group["yajin_all_u"], group["yajin_all_m"], group["yajin_all"], log_danbao["created_at"], log_danbao["yuefei"], log_danbao["yuefei_day"], log_danbao["remark"], log_danbao["tuoguan"], log_danbao["status"], get_current_time())
    
    result = opm.op_update(sql_insert)

    opm.dispose()

    return result
    
    
async def danbao_update_yuefei(data_id, yuefei):
    opm = OPMysql()

    sql_update = "update log_danbao set yuefei = %s where id = %s" % (yuefei, data_id)
    
    result = opm.op_update(sql_update)
    
    opm.dispose()

    return result
    
    
async def danbao_over(data_id):
    opm = OPMysql()

    sql_update = "update log_danbao set status = '%s', ended_at = '%s' where id = %s" % (2, get_current_time(), data_id)
    
    result = opm.op_update(sql_update)
    
    opm.dispose()

    return result
    
    
async def danbao_yuefei_one(data_id, group_tg_id, start_at, ended_at):
    opm = OPMysql()

    sql = "select * from log_danbao_yuefei where data_id = %s and group_tg_id = '%s' and created_at >= '%s' and created_at < '%s'" % (data_id, group_tg_id, start_at, ended_at)

    result = opm.op_select_one(sql)

    opm.dispose()

    return result
    
    
async def danbao_yuefei_save(group, log_danbao, message_tg_id, user_input, created_at, typee = 1):
    user_info = "%s,%s,%s" % (user_input["user_tg_id"], user_input["fullname"], user_input["username"])
    if created_at is None:
        created_at = get_current_time()
    
    opm = OPMysql()

    sql = "insert into log_danbao_yuefei(title, num, business_detail_type, data_id, group_tg_id, message_tg_id, user_info, money, created_at, start_at, type) values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (group["title"], group["group_num"], group["business_detail_type"], log_danbao["id"], log_danbao["group_tg_id"], message_tg_id, user_info, log_danbao["yuefei"], created_at, get_current_time(), typee)

    result = opm.op_update(sql)

    opm.dispose()

    return result
    
    
async def danbao_yuefei_save_no(group, log_danbao, message_tg_id, user_input, created_at, typee = 1):
    user_info = "%s,%s,%s" % (user_input["user_tg_id"], user_input["fullname"], user_input["username"])
    if created_at is None:
        created_at = get_current_time()
    
    opm = OPMysql()

    sql = "insert into log_danbao_yuefei(title, num, business_detail_type, data_id, group_tg_id, message_tg_id, user_info, money, created_at, start_at, type) values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (group["title"], group["group_num"], group["business_detail_type"], log_danbao["id"], log_danbao["group_tg_id"], message_tg_id, user_info, log_danbao["yuefei"], created_at, get_current_time(), typee, 2)

    result = opm.op_update(sql)

    opm.dispose()

    return result
    
    

async def log_msg_path10_get4(group_tg_id, user_tg_id):
    now = assist.get_current_timestamp()
    created_at_timestamp = now - 60 * 10

    opm = OPMysql()

    sql = "select info from log_msg_path10 where group_tg_id = '%s' and user_tg_id = '%s' and created_at_timestamp >= %s order by created_at_timestamp desc limit 4" % (group_tg_id, user_tg_id, created_at_timestamp)
    
    print(sql)

    result = opm.op_select_all(sql)

    opm.dispose()
    
    return result
    

async def log_msg_path10_save(group_tg_id, user_tg_id, msg_tg_id, info, created_at_timestamp):
    opm = OPMysql()

    sql = "insert into log_msg_path10(group_tg_id, user_tg_id, msg_tg_id, info, created_at_timestamp) values('%s', '%s', '%s', '%s', '%s')" % (group_tg_id, user_tg_id, msg_tg_id, info, created_at_timestamp)

    result = None
    try:
        result = opm.op_update(sql)
    except Exception as e:
        print("sql %s %s" % (sql, e))

    opm.dispose()

    return result


async def getTodayAdsData():
    opm = OPMysql()

    today = int(time.mktime(time.strptime(str(datetime.date.today()), '%Y-%m-%d')))

    sql = "select ads_id, keyword_id from ads_bidding where begin_at <= %s and end_at >= %s" % (today, today)

    result = opm.op_select_all(sql)

    opm.dispose()

    return result


async def getAdsByIds(adsIds, position=1):
    opm = OPMysql()

    sql = opm.cur.mogrify("select id, name, url from ads where position = %s and id in %s", (position, adsIds))

    result = opm.op_select_all(sql)

    opm.dispose()

    data = {}
    for ads in result:
        data[str(ads["id"])] = ads

    return data


async def getKeywordByIds(keywordIds):
    opm = OPMysql()

    sql = opm.cur.mogrify("select id, name from ads_keywords where 1 = %s and id in %s", (1, keywordIds))

    result = opm.op_select_all(sql)

    opm.dispose()

    data = {}
    for keyword in result:
        data[str(keyword["id"])] = keyword

    return data


async def getHotWords():
    opm = OPMysql()

    sql = "select text, count(id) as count from log_search group by text order by count desc limit 10"

    result = opm.op_select_all(sql)

    opm.dispose()

    data = []
    for keyword in result:
        data.append(keyword['text'])

    return data


async def updateFakeGroups(groupId):
    opm = OPMysql()

    sql = "select * from fake_groups where group_tg_id = %s" % groupId

    result = opm.op_select_one(sql)

    if result is None:
        sql = "insert into fake_groups(group_tg_id, status) values(%s, 0)" % groupId

        opm.op_update(sql)

    opm.dispose()
