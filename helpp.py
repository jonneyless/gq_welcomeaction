import asyncio
import re

import config
# import tg
import db
import db_redis
from assist import get_current_timestamp, handle_chat, get_current_time
from config import ybjqr_bot_id


# from tg import remove_admin_tel as tg_remove_admin_tel



# ======================================================================================================================

async def reply_and_delete_last(group_tg_id, key_short, bot, event, msg, buttons=None):
    group_tg_id = int(group_tg_id)
    
    m = None
    if buttons is None:
        m = await event.reply(message=msg, parse_mode="html", link_preview=False)
    else:
        m = await event.reply(message=msg, buttons=buttons, parse_mode="html", link_preview=False)

    last_m_id = await db_redis.last_message_id_get(group_tg_id, key_short)
    if last_m_id is not None:
        last_m_id = int(last_m_id)
        try:
            await bot.delete_messages(group_tg_id, last_m_id)
        except Exception:
            pass

    if m is not None:
        if hasattr(m, "id"):
            await db_redis.last_message_id_set(group_tg_id, m.id, key_short)
            

async def create_and_update_group(chat_id, chat):
    chat = handle_chat(chat_id, chat)

    group_tg_id = chat["tg_id"]
    group_title = chat["title"]

    group = await db.group_one(group_tg_id)
    if group is None:
        await db.group_save(group_tg_id, group_title)
        return
    
    if group["title"] != group_title:
        await db.group_set_title(group["id"], group_title)

    group["title"] = group_title
    group["flag"] = int(group["flag"])
    group["trade_type"] = int(group["trade_type"])
    group["welcome_status"] = int(group["welcome_status"])
    group["people_limit"] = int(group["people_limit"])
    group["limit_one_time"] = int(group["limit_one_time"])

    group["welcome_true_status"] = int(group["welcome_true_status"])
    group["welcome_false_status"] = int(group["welcome_false_status"])
    
    if (hasattr(group, "business_type")) or ("business_type" in group):
        group["business_type"] = int(group["business_type"])
    else:
        group["business_type"] = 1

    if (hasattr(group, "open_status")) or ("open_status" in group):
        group["open_status"] = int(group["open_status"])
    else:
        group["open_status"] = 1

    if group["limit_one_time"] < 1:
        group["limit_one_time"] = 1

    if "send_user_change" in group:
        group["send_user_change"] = int(group["send_user_change"])
    else:
        group["send_user_change"] = 2

    return group


async def create_and_update_user(bot, group_tg_id, sender):
    sender["group_tg_id"] = group_tg_id
    
    # userr = await db.user_one(sender["tg_id"])
    # if userr is not None:
        # msg = "用户tgid：`%s`," % sender["tg_id"]
        # flag = False
        # if (userr["username"] != sender["username"]):
        #     msg += " 用户名 %s 改为 %s" % (userr["username"], sender["username"])
        #     flag = True
        # if (userr["fullname"] != sender["fullname"]):
        #     if flag:
        #         msg += ",昵称 %s 改为 %s" % (userr["fullname"], sender["fullname"])
        #     else:
        #         msg += " 昵称 %s 改为 %s" % (userr["fullname"], sender["fullname"])
        #     flag = True
         
        # if flag:
        #     user_change_status = await db_redis.user_change_status_get(sender["tg_id"])
        #     if user_change_status is None:
        #         await db_redis.user_change_status_set(sender["tg_id"])
                
        #         await tg.send(bot, group_tg_id, msg)
        #         await db.message_save(group_tg_id, config.ybjqr_bot_id, -1, msg, get_current_time())

    return sender


async def check_user(bot, event, group, sender):
    userr = await db_redis.hwdb_user_get(sender["tg_id"])
    if userr is None:
        await db_redis.hwdb_user_set(sender["tg_id"], sender)
        return
    
    # 新user：sender
    # 老user：userr
    
    msg = "用户tgid：`%s`，" % sender["tg_id"]
    flag = False
    if (userr["username"] != sender["username"]):
        msg += " 用户名 %s 改为 %s" % (userr["username"], sender["username"])
        flag = True
    if (userr["fullname"] != sender["fullname"]):
        if flag:
            msg += "，昵称 %s 改为 %s" % (userr["fullname"], sender["fullname"])
        else:
            msg += " 昵称 %s 改为 %s" % (userr["fullname"], sender["fullname"])
        flag = True
        
    if flag:
        # 有修改
        await db_redis.hwdb_user_set(sender["tg_id"], sender)
        await db.user_update_tgid(sender["tg_id"], sender)
        
        if group is not None:
            if group["send_user_change"] == 1:
                flag_username = await has_username_restrict_word(sender["username"])
                if flag_username:
                    return
                
                flag_fullname = await has_fullname_restrict_word(sender["fullname"])
                if flag_fullname:
                    return
            
                await tg.send(bot, group["tg_id"], msg)
                
                
# ======================================================================================================================


async def get_user_role(group_tg_id, user_tg_id):
    is_official = await db.official_one(user_tg_id)
    is_white = await db.white_one(user_tg_id)

    is_admin = None
    if group_tg_id is not None:
        is_admin = await db.group_admin_one(group_tg_id, user_tg_id)

    if is_official is None:
        is_official = False
    else:
        is_official = True

    if is_white is None:
        is_white = False
    else:
        is_white = True

    if is_admin is None:
        is_admin = False
    else:
        is_admin = True

    return is_official, is_white, is_admin


async def is_general_user(group_tg_id, user_tg_id):
    is_official = await db.official_one(user_tg_id)
    is_admin = None
    if group_tg_id is not None:
        is_admin = await db.group_admin_one(group_tg_id, user_tg_id)

    if is_official is None:
        is_official = False
    else:
        is_official = True

    if is_admin is None:
        is_admin = False
    else:
        is_admin = True

    flag = True
    if is_official or is_admin:
        flag = False

    return flag


async def is_huione_user(user_tg_id):
    is_official, is_white, is_admin = await get_user_role(None, user_tg_id)

    flag = False
    if is_official or is_white:
        flag = True

    return flag


async def like_admin(group_tg_id, sender):
    group_admins = await db.group_admin_get(group_tg_id)

    group_admin_like = None
    for group_admin in group_admins:
        try:
            if (sender["firstname"] == group_admin["firstname"]) and (sender["lastname"] == group_admin["lastname"]):
                if (int(sender["tg_id"]) != int(group_admin["tg_id"])) and \
                        sender["username"] != group_admin["username"]:
                    group_admin_like = group_admin
                    break
        except:
            print("redis error %s" % group_tg_id)

    return group_admin_like


# ======================================================================================================================


async def has_cheat_bank(text):
    cheat_banks = await db_redis.cheat_bank_get()
    if cheat_banks is None:
        cheat_banks_data = await db.cheat_bank_get()
        cheat_banks = []
        for item in cheat_banks_data:
            cheat_banks.append(item["num"])
        await db_redis.cheat_bank_set(cheat_banks)

    cheat_bank = None
    for item in cheat_banks:
        if text.find(item) >= 0:
            cheat_bank = item
            break

    return cheat_bank


async def has_cheat_coin(text):
    cheat_coins = await db_redis.cheat_coin_get()
    if cheat_coins is None:
        cheat_coins_data = await db.cheat_coin_get()
        cheat_coins = []
        for item in cheat_coins_data:
            cheat_coins.append(item["address"])
        await db_redis.cheat_coin_set(cheat_coins)

    cheat_coin = None
    for item in cheat_coins:
        if text.find(item) >= 0:
            cheat_coin = item
            break

    return cheat_coin


# ======================================================================================================================

def handle_text(text):
    text = text.replace("𝅹", "")
    text = text.replace(" ", "")
    text = text.replace(",", "")
    text = text.replace(".", "")
    text = text.replace("，", "")
    text = text.replace("。", "")
    text = text.replace("+", "")
    text = text.replace("-", "")
    text = text.replace("*", "")
    text = text.replace("/", "")
    text = text.replace("(", "")
    text = text.replace("（", "")
    text = text.replace(")", "")
    text = text.replace("）", "")
    text = text.replace("、", "")

    text = text.lower()

    return text


async def has_restrict_word(text, type_str):
    # text = handle_text(text)

    # restrict_words = await db_redis.restrict_word_get(type_str)
    # if restrict_words is None:
    #     restrict_words_data = await db.restrict_word_get(type_str)
    #     restrict_words = []
    #     for item in restrict_words_data:
    #         restrict_words.append(item)
    #     await db_redis.restrict_word_set(type_str, restrict_words)

    # restrict_word = None
    # for item in restrict_words:
    #     name = item["name"]
    #     name = handle_text(name)
    #     level = int(item["level"])

    #     replace_flag = False
    #     if text.find(name) >= 0:
    #         if restrict_word is None:
    #             replace_flag = True
    #         else:
    #             if restrict_word["level"] < level:
    #                 replace_flag = True
    #     if replace_flag:
    #         restrict_word = {
    #             "name": name,
    #             "level": level,
    #         }

    # return restrict_word
    
    text = handle_text(text)

    restrict_words = await db_redis.restrict_word_get(type_str)
    if restrict_words is None:
        restrict_words_data = await db.restrict_word_get(type_str)
        restrict_words = []
        for item in restrict_words_data:
            restrict_words.append(item)
        await db_redis.restrict_word_set(type_str, restrict_words)
    
    pattern_name = "(.+)\(\.\*\)(.+)"

    restrict_word = None
    for item in restrict_words:
        name = item["name"]
        level = int(item["level"])
        
        replace_flag = False
        
        result_name = re.match(pattern_name, name)
        if result_name is None:
            name = handle_text(name)
            
            if text.find(name) >= 0:
                if restrict_word is None:
                    replace_flag = True
                else:
                    if restrict_word["level"] < level:
                        replace_flag = True
                        
            if replace_flag:
                restrict_word = {
                    "name": name,
                    "level": level,
                }
                
                return restrict_word
        else:
            pattern1 = name
            pattern1 = "(.*)" + pattern1
            pattern1 = pattern1 + "(.*)"
            
            pattern1 = pattern1.lower()
    
            match_result = None
            try:
                match_result = re.match(pattern1, text)
            except:
                print("%s is error" % name)

            if match_result is not None:
                print("fullname %s, word %s" % (text, name))
                
                if restrict_word is None:
                    replace_flag = True
                else:
                    if restrict_word["level"] < level:
                        replace_flag = True
            if replace_flag:
                restrict_word = {
                    "name": item["name"],
                    "level": level,
                }
                
                return restrict_word

    return restrict_word


async def has_fullname_restrict_word(fullname):
    type_str = "4"
    return await has_restrict_word(fullname, type_str)


async def has_username_restrict_word(username):
    type_str = "9"
    return await has_restrict_word(username, type_str)


async def has_intro_restrict_word(intro):
    type_str = "9"
    return await has_restrict_word(intro, type_str)


async def has_msg_restrict_word(text):
    type_str = "1"
    return await has_restrict_word(text, type_str)


# ======================================================================================================================

async def get_config_text_len_limit():
    key = "limit_text_len"

    limit_text_len = await db_redis.config_get(key)
    if limit_text_len is None:
        limit_text_len = await db.config_get(key)
        if limit_text_len is None:
            limit_text_len = config.limit_text_len
        else:
            limit_text_len = limit_text_len["val"]

        await db_redis.config_set(key, limit_text_len)

    return int(limit_text_len)


async def get_config_limit_time():
    key = "limit_time"

    limit_time = await db_redis.config_get(key)
    if limit_time is None:
        limit_time = await db.config_get(key)
        if limit_time is None:
            limit_time = config.limit_text_len
        else:
            limit_time = limit_time["val"]

        await db_redis.config_set(key, limit_time)

    return int(limit_time)


async def get_config_limit_num():
    key = "limit_num"

    limit_num = await db_redis.config_get(key)
    if limit_num is None:
        limit_num = await db.config_get(key)
        if limit_num is None:
            limit_num = config.limit_num
        else:
            limit_num = limit_num["val"]

        await db_redis.config_set(key, limit_num)

    return int(limit_num)


async def get_config_limit_all_time():
    key = "limit_all_time"

    limit_all_time = await db_redis.config_get(key)
    if limit_all_time is None:
        limit_all_time = await db.config_get(key)
        if limit_all_time is None:
            limit_all_time = config.limit_all_time
        else:
            limit_all_time = limit_all_time["val"]

        await db_redis.config_set(key, limit_all_time)

    return int(limit_all_time)


async def get_config_limit_all_group_num():
    key = "limit_all_group_num"

    limit_all_group_num = await db_redis.config_get(key)
    if limit_all_group_num is None:
        limit_all_group_num = await db.config_get(key)
        if limit_all_group_num is None:
            limit_all_group_num = config.limit_all_group_num
        else:
            limit_all_group_num = limit_all_group_num["val"]

        await db_redis.config_set(key, limit_all_group_num)

    return int(limit_all_group_num)


async def get_config_limit_cancel_restrict():  # 天
    key = "limit_cancel_restrict"

    limit_cancel_restrict = await db_redis.config_get(key)
    if limit_cancel_restrict is None:
        limit_cancel_restrict = await db.config_get(key)
        if limit_cancel_restrict is None:
            limit_cancel_restrict = config.limit_cancel_restrict
        else:
            limit_cancel_restrict = limit_cancel_restrict["val"]

        await db_redis.config_set(key, limit_cancel_restrict)

    return int(limit_cancel_restrict)


async def get_config_welcome_true_status():
    key = "welcome_true_status"

    welcome_true_status = await db_redis.config_get(key)
    if welcome_true_status is None:
        welcome_true_status = await db.config_get(key)
        if welcome_true_status is None:
            welcome_true_status = config.welcome_true_status
        else:
            welcome_true_status = welcome_true_status["val"]

        await db_redis.config_set(key, welcome_true_status)

    return int(welcome_true_status)


async def get_config_welcome_false_status():
    key = "welcome_false_status"

    welcome_false_status = await db_redis.config_get(key)
    if welcome_false_status is None:
        welcome_false_status = await db.config_get(key)
        if welcome_false_status is None:
            welcome_false_status = config.welcome_false_status
        else:
            welcome_false_status = welcome_false_status["val"]

        await db_redis.config_set(key, welcome_false_status)

    return int(welcome_false_status)


async def get_config_welcome_true_info():
    key = "welcome_true_info"

    welcome_true_info = await db_redis.config_get(key)
    if welcome_true_info is None:
        welcome_true_info = await db.config_get(key)
        if welcome_true_info is None:
            welcome_true_info = config.welcome_true_info
        else:
            welcome_true_info = welcome_true_info["val"]

        await db_redis.config_set(key, welcome_true_info)

    return welcome_true_info


async def get_config_welcome_false_info():
    key = "welcome_false_info"

    welcome_false_info = await db_redis.config_get(key)
    if welcome_false_info is None:
        welcome_false_info = await db.config_get(key)
        if welcome_false_info is None:
            welcome_false_info = config.welcome_false_info
        else:
            welcome_false_info = welcome_false_info["val"]

        await db_redis.config_set(key, welcome_false_info)

    return welcome_false_info


# ======================================================================================================================


async def vip_msg_empty(user_tg_id):
    await db_redis.vip_msg_set(user_tg_id, [])


async def vip_msg_set(user_tg_id, message_tg_id, text):
    current_timestamp = get_current_timestamp()

    data = await db_redis.vip_msg_get(user_tg_id)

    data_new = []
    if data is not None:
        for item in data:
            item_message_tg_id = item["message_tg_id"]
            item_text = item["text"]
            item_timestamp = int(item["timestamp"])

            # 仅保存1小时内
            if current_timestamp - item_timestamp < 1800:
                data_new.append({
                    "message_tg_id": item_message_tg_id,
                    "text": item_text,
                    "timestamp": item_timestamp,
                })

    data_new.append({
        "message_tg_id": message_tg_id,
        "text": text,
        "timestamp": current_timestamp,
    })

    await db_redis.vip_msg_set(user_tg_id, data_new)


async def vip_msg_get(user_tg_id):
    current_timestamp = get_current_timestamp()

    data = await db_redis.vip_msg_get(user_tg_id)

    data_new = []
    if data is not None:
        for item in data:
            item_message_tg_id = item["message_tg_id"]
            item_text = item["text"]
            item_timestamp = int(item["timestamp"])

            # 仅保存1小时内
            if current_timestamp - item_timestamp < 1800:
                data_new.append({
                    "message_tg_id": item_message_tg_id,
                    "text": item_text,
                    "timestamp": item_timestamp,
                })

    return data_new


# ======================================================================================================================


async def user_send_limit_one_set(group_tg_id, user_tg_id):
    current_timestamp = get_current_timestamp()

    data = await db_redis.user_send_limit_one_get(group_tg_id, user_tg_id)

    data_new = []
    if data is not None:
        for item in data:
            item_timestamp = int(item)
            # 仅保存1小时内
            if current_timestamp - item_timestamp < 3600:
                data_new.append(item_timestamp)
    data_new.append(current_timestamp)

    await db_redis.user_send_limit_one_set(group_tg_id, user_tg_id, data_new)


async def user_send_limit_set(group_tg_id, user_tg_id):
    current_timestamp = get_current_timestamp()

    data = await db_redis.user_send_limit_get(user_tg_id)

    data_new = []
    if data is not None:
        for item in data:
            item_group_tg_id = item["group_tg_id"]
            item_timestamp = int(item["timestamp"])
            # 仅保存1小时内
            if current_timestamp - item_timestamp < 3600:
                data_new.append({
                    "group_tg_id": item_group_tg_id,
                    "timestamp": item_timestamp,
                })
    data_new.append({
        "group_tg_id": group_tg_id,
        "timestamp": current_timestamp,
    })

    await db_redis.user_send_limit_set(user_tg_id, data_new)


# ======================================================================================================================

async def has_user_send_limit_one(group_tg_id, user_tg_id):
    limit_time = await get_config_limit_time()
    limit_num = await get_config_limit_num()

    current_timestamp = get_current_timestamp()
    start_timestamp = current_timestamp - limit_time

    flag = False
    num = 0
    data = await db_redis.user_send_limit_one_get(group_tg_id, user_tg_id)
    
    if data is not None:
        for item in data:
            item_timestamp = int(item)
            if item_timestamp > start_timestamp:
                num = num + 1

    if num >= limit_num:
        flag = True

    return flag


async def has_user_send_limit(group_tg_id, user_tg_id):
    limit_all_time = await get_config_limit_all_time()
    limit_all_group_num = await get_config_limit_all_group_num()

    current_timestamp = get_current_timestamp()
    start_timestamp = current_timestamp - limit_all_time

    flag = False
    num = 0
    group_tg_id_arr = []
    data = await db_redis.user_send_limit_get(user_tg_id)
    if data is not None:
        for item in data:
            item_group_tg_id = item["group_tg_id"]
            item_timestamp = int(item["timestamp"])

            if item_timestamp > start_timestamp:
                if item_group_tg_id not in group_tg_id_arr:
                    num = num + 1
                    group_tg_id_arr.append(item_group_tg_id)

    until_date = None
    if num >= limit_all_group_num:
        flag = True
        limit_cancel_restrict = await get_config_limit_cancel_restrict()
        until_date = current_timestamp + limit_cancel_restrict * 86400

    return flag, group_tg_id_arr, until_date

# ======================================================================================================================


async def user_at_official_set(group_tg_id, user_tg_id):
    current_timestamp = get_current_timestamp()

    data = await db_redis.user_at_official_get(group_tg_id, user_tg_id)

    data_new = []
    if data is not None:
        for item in data:
            item_timestamp = int(item)
            # 仅保存3分钟内
            if current_timestamp - item_timestamp < 180:
                data_new.append(item_timestamp)
    data_new.append(current_timestamp)

    await db_redis.user_at_official_set(group_tg_id, user_tg_id, data_new)


async def user_at_official_get_num(group_tg_id, user_tg_id):
    current_timestamp = get_current_timestamp()

    data = await db_redis.user_at_official_get(group_tg_id, user_tg_id)

    data_new = []
    if data is not None:
        for item in data:
            item_timestamp = int(item)
            # 仅保存3分钟内
            if current_timestamp - item_timestamp < 180:
                data_new.append(item_timestamp)

    return len(data_new)
    
# ======================================================================================================================


async def respond_and_delete(bot, event, group_tg_id, info, sleep_time=3):
    m = await event.reply(message=info)   
    await asyncio.sleep(sleep_time)
    if m is not None and hasattr(m, "id"):
        await tg.delete_only(bot, group_tg_id, m.id)
        
    await event.delete()
    
    
async def remove_not_official_admin(bot, group_tg_id):
    admins = await db.group_admin_get_now(group_tg_id)
    admins_kick_num = 0
    admins_kick_num_ok = 0
    for admin in admins:
        admin_tg_id = int(admin["user_tg_id"])

        if admin_tg_id == ybjqr_bot_id:
            continue

        admin_is_official = await db.official_one(admin_tg_id)
        if admin_is_official is not None:
            continue

        tg_user = await db.tg_user_new_one(admin_tg_id)
        if tg_user is not None:
            continue

        admins_kick_num = admins_kick_num + 1
        
        # flag = await tg_remove_admin_tel(bot, group_tg_id, admin_tg_id)
        flag = await bot.edit_admin(int(group_tg_id), int(admin_tg_id), is_admin=False)
        
        if flag is not None and flag:
            admins_kick_num_ok = admins_kick_num_ok + 1
            await db.group_admin_del(group_tg_id, admin_tg_id)

    msg = "(机器人管理请手动回收)\n"
    msg += "回收管理成功\n"
    if admins_kick_num != admins_kick_num_ok:
        msg += "部分管理回收失败，请使用 回收管理 命令重新回收管理\n"
        
    return msg
    

async def has_yuefei(log_danbao):
    data_id = log_danbao["id"]
    group_tg_id = log_danbao["group_tg_id"]
    created_at = str(log_danbao['created_at'])
    yuefei_day = int(log_danbao['yuefei_day'])
    now = get_current_time()
    
    created_at_timestamp = time2timestamp(created_at)
    now_timestamp = get_current_timestamp()
    month_num = math.ceil((now_timestamp - created_at_timestamp) / (86400 * 30))
    
    text_arr = []
    flag = True # 月费已全部结清

    for i in range(month_num + 1):
        start_timestamp = created_at_timestamp + 86400 * i * 30
        end_timestamp = start_timestamp + 86400 * 30
        
        if start_timestamp > now_timestamp:
            break
        
        start_at = timestamp2time(start_timestamp)
        end_at = timestamp2time(end_timestamp)
        
        log_yuefei = await db.danbao_yuefei_one(data_id, group_tg_id, start_at, end_at)
        if log_yuefei is None:
            text_arr.append(get_simple_day(start_at) + "到" + get_simple_day(end_at))
            flag = False
            
    return flag, text_arr
    
    
async def yuefei_sava_all(group, log_danbao, message_tg_id, userr, flag=1):
    data_id = log_danbao["id"]
    group_tg_id = log_danbao["group_tg_id"]
    created_at = str(log_danbao['created_at'])
    yuefei_day = int(log_danbao['yuefei_day'])
    now = get_current_time()
    
    created_at_timestamp = time2timestamp(created_at)
    now_timestamp = get_current_timestamp()
    month_num = math.ceil((now_timestamp - created_at_timestamp) / (86400 * 30))
    
    for i in range(month_num + 1):
        start_timestamp = created_at_timestamp + 86400 * i * 30
        end_timestamp = start_timestamp + 86400 * 30
        
        if start_timestamp > now_timestamp:
            break
        
        start_at = timestamp2time(start_timestamp)
        end_at = timestamp2time(end_timestamp)
        
        log_yuefei = await db.danbao_yuefei_one(data_id, group_tg_id, start_at, end_at)
        if log_yuefei is None:
            if flag == 1:
                await db.danbao_yuefei_save(group, log_danbao, message_tg_id, userr, timestamp2time(start_timestamp + 1), 2)
            else:
                await db.danbao_yuefei_save_no(group, log_danbao, message_tg_id, userr, timestamp2time(start_timestamp + 1), 2)
                
                