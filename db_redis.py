import json

from redis import Redis

import db
from assist import get_current_timestamp, get_tomorrow_timestamp
from config import redisInfo

redis_host = redisInfo['host']
redis_port = redisInfo['port']

conn = Redis(host=redis_host, port=redis_port, db=0)
conn11 = Redis(host=redis_host, port=redis_port, db=11)

prefix = "welcome_"


# ======================================================================================================================

async def group_one(group_tg_id):
    key = prefix + "group" + str(group_tg_id)
    
    val = conn.get(key)
    if val is None:
        return None
    else:
        return json.loads(val)


async def group_set(group_tg_id, val):
    key = prefix + "group" + str(group_tg_id)

    conn.set(key, json.dumps(val), 300)  # 5分钟


# ======================================================================================================================

async def groups_get():
    key = prefix + "groups"
    val = conn.get(key)
    if val is None:
        return None
    else:
        return json.loads(val)


async def groups_set(val):
    key = prefix + "groups"

    conn.set(key, json.dumps(val), 3600)  # 1小时


# ======================================================================================================================

async def status_check_group_get(group_tg_id):
    key = prefix + "check_1" + str(group_tg_id)

    return conn.get(key)


async def status_check_group_set(group_tg_id):
    key = prefix + "check_1" + str(group_tg_id)

    conn.set(key, 9, 1)  # 5分钟


async def group_last_check_message_id_get(group_tg_id):
    key = prefix + "check_message_id_" + str(group_tg_id)

    return conn.get(key)


async def group_last_check_message_id_set(group_tg_id, message_id):
    key = prefix + "check_message_id_" + str(group_tg_id)

    conn.set(key, message_id, 86400)  # 一天


async def group_last_close_message_id_get(group_tg_id):
    key = prefix + "close_message_id_" + str(group_tg_id)

    return conn.get(key)


async def group_last_close_message_id_set(group_tg_id, message_id):
    key = prefix + "close_message_id_" + str(group_tg_id)

    conn.set(key, message_id, 86400)  # 一天
    

async def group_last_error_message_id_get(group_tg_id):
    key = prefix + "error_message_id_" + str(group_tg_id)

    return conn.get(key)


async def group_last_error_message_id_set(group_tg_id, message_id):
    key = prefix + "error_message_id_" + str(group_tg_id)

    conn.set(key, message_id, 86400)  # 一天
    

async def group_last_si_message_id_get(group_tg_id):
    key = prefix + "si_message_id_" + str(group_tg_id)

    return conn.get(key)


async def group_last_si_message_id_set(group_tg_id, message_id):
    key = prefix + "si_message_id_" + str(group_tg_id)

    conn.set(key, message_id, 86400)  # 一天

# ======================================================================================================================

async def word_username_get():
    key = prefix + "word_username"

    val = conn.get(key)
    if val is not None:
        return json.loads(val)
    else:
        return None


async def word_username_set(data):
    key = prefix + "word_username"
    val = json.dumps(data)

    conn.set(key, json.dumps(val), 3600)  # 1小时


# ======================================================================================================================

async def official_get():
    key = prefix + "officials"

    val = conn.get(key)
    if val is None:
        return None
    else:
        return json.loads(val)


async def official_set(val):
    key = prefix + "officials"

    conn.set(key, json.dumps(val), 3600)  # 1小时


# ======================================================================================================================

async def white_get():
    key = prefix + "whites"

    val = conn.get(key)
    if val is None:
        return None
    else:
        return json.loads(val)


async def white_set(val):
    key = prefix + "whites"

    conn.set(key, json.dumps(val), 3600)  # 1小时


# ======================================================================================================================

async def cheat_get():
    key = prefix + "cheats"

    val = conn.get(key)
    if val is None:
        return None
    else:
        return json.loads(val)


async def cheat_set(val):
    key = prefix + "cheats"

    conn.set(key, json.dumps(val), 3600)  # 1小时


# ======================================================================================================================


async def group_admin_get():
    key = prefix + "group_admin"

    val = conn.get(key)
    if val is None:
        return None
    else:
        return json.loads(val)


async def group_admin_set(val):
    key = prefix + "group_admin"

    conn.set(key, json.dumps(val), 3600)  # 1小时


# async def group_admin_single_get(group_tg_td):
#     key = prefix + "group_admin_single" + str(group_tg_td)

#     val = conn.get(key)
#     if val is None:
#         return None
#     else:
#         return json.loads(val)


# async def group_admin_single_set(group_tg_td, val):
#     key = prefix + "group_admin_single" + str(group_tg_td)

#     conn.set(key, json.dumps(val), 3600)  # 1小时
    

# ======================================================================================================================


async def group_admin_one_get(group_tg_id):
    key = prefix + "group_admin_" + str(group_tg_id)

    val = conn.get(key)
    if val is None:
        return None
    else:
        return json.loads(val)


async def group_admin_one_set(group_tg_id, val):
    key = prefix + "group_admin_" + str(group_tg_id)

    conn.set(key, json.dumps(val), 3600)  # 1小时


# ======================================================================================================================

async def cheat_bank_get():
    key = prefix + "cheat_bank"

    val = conn.get(key)
    if val is None:
        return None
    else:
        return json.loads(val)


async def cheat_bank_set(val):
    key = prefix + "cheat_bank"

    conn.set(key, json.dumps(val), 3600)  # 1小时


# ======================================================================================================================

async def cheat_coin_get():
    key = prefix + "cheat_coin"

    val = conn.get(key)
    if val is None:
        return None
    else:
        return json.loads(val)


async def cheat_coin_set(val):
    key = prefix + "cheat_coin"

    conn.set(key, json.dumps(val), 3600)  # 1小时


# ======================================================================================================================

async def config_get(key):
    key = prefix + key

    val = conn.get(key)
    if val is None:
        return None
    else:
        return val


async def config_set(key, val):
    key = prefix + key

    conn.set(key, val, 300)  # 5分钟


# ======================================================================================================================

async def reply_text_get():
    key = prefix + "reply_text"

    val = conn.get(key)
    if val is None:
        return None
    else:
        return json.loads(val)


async def reply_text_set(val):
    key = prefix + "reply_text"

    conn.set(key, json.dumps(val), 180)  # 5分钟
    
    
    
# ======================================================================================================================

async def restrict_word_get(type_str):
    key = prefix + "restrict_word_" + type_str

    val = conn.get(key)
    if val is None:
        return None
    else:
        return json.loads(val)


async def restrict_word_set(type_str, val):
    key = prefix + "restrict_word_" + type_str

    conn.set(key, json.dumps(val), 3600)  # 1小时


# ======================================================================================================================


async def user_send_limit_one_get(group_tg_id, user_tg_id):
    key = prefix + str(group_tg_id) + str(user_tg_id)

    val = conn.get(key)
    if val is None:
        return None
    else:
        return json.loads(val)


async def user_send_limit_one_set(group_tg_id, user_tg_id, val):
    key = prefix + str(group_tg_id) + str(user_tg_id)

    conn.set(key, json.dumps(val), 864000)  # 10天


# ======================================================================================================================

async def user_send_limit_get(user_tg_id):
    key = prefix + str(user_tg_id)

    val = conn.get(key)
    if val is None:
        return None
    else:
        return json.loads(val)


async def user_send_limit_set(user_tg_id, val):
    key = prefix + str(user_tg_id)

    conn.set(key, json.dumps(val), 864000)  # 10天


# ======================================================================================================================

async def last_welcome_message_id_get(group_tg_id):
    key = prefix + "last_welcome_message_id_" + str(group_tg_id)

    return conn.get(key)


async def last_welcome_message_id_set(group_tg_id, message_tg_id, limit_one_time):
    key = prefix + "last_welcome_message_id_" + str(group_tg_id)

    conn.set(key, message_tg_id, limit_one_time)  # 1天


# ======================================================================================================================

async def vip_msg_get(user_tg_id):
    key = prefix + "vip" + str(user_tg_id)

    val = conn.get(key)
    if val is None:
        return None
    else:
        return json.loads(val)


async def vip_msg_set(user_tg_id, val):
    key = prefix + "vip" + str(user_tg_id)

    conn.set(key, json.dumps(val), 864000)  # 10天


# ======================================================================================================================

async def middleware_user_set(data):
    key = prefix + "middleware_user"

    conn.rpush(key, json.dumps(data))


def middleware_user_get():
    key = prefix + "middleware_user"

    data = conn.lpop(key)
    if data is None:
        return data
    else:
        return json.loads(data)


async def middleware_user_one_set(user_tg_id):
    key = prefix + "middleware_user" + str(user_tg_id)

    conn.set(key, 9, 300)  # 5分钟
    

async def middleware_user_one_get(user_tg_id):
    key = prefix + "middleware_user" + str(user_tg_id)

    return conn.get(key)
    
    
# ======================================================================================================================

async def middleware_msg_set(data):
    key = prefix + "middleware_msg"

    conn.rpush(key, json.dumps(data))


def middleware_msg_get():
    key = prefix + "middleware_msg"

    data = conn.lpop(key)
    if data is None:
        return data
    else:
        return json.loads(data)


# ======================================================================================================================

async def middleware_delete_day_set(data):
    key = prefix + "middleware_delete_day"

    conn.rpush(key, json.dumps(data))


def middleware_delete_day_get():
    key = prefix + "middleware_delete_day"

    data = conn.lpop(key)
    if data is None:
        return data
    else:
        return json.loads(data)


# ======================================================================================================================


async def user_change_status_set(user_tg_id):
    key = prefix + "user_change_status" + str(user_tg_id)

    conn.set(key, 9, 60)  # 1分钟
    

async def user_change_status_get(user_tg_id):
    key = prefix + "user_change_status" + str(user_tg_id)

    return conn.get(key)
    
    
# ======================================================================================================================

async def last_message_id_get(group_tg_id, key_short):
    key = prefix + key_short + str(group_tg_id)

    return conn.get(key)


async def last_message_id_set(group_tg_id, message_id, key_short):
    key = prefix + key_short + str(group_tg_id)

    conn.set(key, message_id, 86400)  # 一天


# ======================================================================================================================

async def message_first_get(group_tg_id, user_tg_id):
    key = prefix + str(group_tg_id) + str(user_tg_id) + "message_first";

    return conn.get(key)


async def message_first_set(group_tg_id, user_tg_id):
    current_timestamp = get_current_timestamp()
    tomorrow_timestamp = get_tomorrow_timestamp()
    
    key = prefix + str(group_tg_id) + str(user_tg_id) + "message_first";

    conn.set(key, 9, (tomorrow_timestamp - current_timestamp))  # 当天
    

# ======================================================================================================================

async def group_boss_pwd_status_get(user_tg_id):
    key = prefix + "group_boss_pwd" + str(user_tg_id)

    return conn.get(key)


async def group_boss_pwd_status_set(user_tg_id):
    key = prefix + "group_boss_pwd" + str(user_tg_id)

    conn.set(key, 9, 864000)  # 10天


async def group_boss_pwd_status_del(user_tg_id):
    key = prefix + "group_boss_pwd" + str(user_tg_id)

    conn.delete(key)
    

# ======================================================================================================================

async def group_word_get():
    key = prefix + "group_word"
    val = conn.get(key)
    if val is None:
        return None
    else:
        return json.loads(val)


async def search_sensitive_words():
    key = prefix + ":search:sensitive_words"
    val = conn.get(key)
    if val is None:
        return None
    else:
        return json.loads(val)


async def group_word_set(val):
    key = prefix + "group_word"

    conn.set(key, json.dumps(val), 300)  # 5分钟


async def search_sensitive_words_set(val):
    key = prefix + ":search:sensitive_words"

    conn.set(key, json.dumps(val), 300)  # 5分钟
    
    
async def group_word_white_get():
    key = prefix + "group_word_white"
    val = conn.get(key)
    if val is None:
        return None
    else:
        return json.loads(val)


async def group_word_white_set(val):
    key = prefix + "group_word_white"

    conn.set(key, json.dumps(val), 60)  # 1分钟
    
    
# ======================================================================================================================

async def search_word_get():
    key = prefix + "search_word"
    val = conn.get(key)
    if val is None:
        return None
    else:
        return json.loads(val)


async def search_word_set(val):
    key = prefix + "search_word"

    conn.set(key, json.dumps(val), 300)  # 5分钟
    

async def search_reply_word_get():
    key = prefix + "search_reply_word"
    val = conn.get(key)
    if val is None:
        return None
    else:
        return json.loads(val)


async def search_reply_word_set(val):
    key = prefix + "search_reply_word"

    conn.set(key, json.dumps(val), 300)  # 5分钟


async def search_like_word_get():
    key = prefix + "search_like_word"
    val = conn.get(key)
    if val is None:
        return None
    else:
        return json.loads(val)


async def search_like_word_set(val):
    key = prefix + "search_like_word"

    conn.set(key, json.dumps(val), 300)  # 5分钟
    

# ======================================================================================================================

async def user_at_official_get(group_tg_id, user_tg_id):
    key = prefix + str(group_tg_id) + str(user_tg_id) + "user_at_official"

    val = conn.get(key)
    if val is None:
        return None
    else:
        return json.loads(val)


async def user_at_official_set(group_tg_id, user_tg_id, val):
    key = prefix + str(group_tg_id) + str(user_tg_id) + "user_at_official"

    conn.set(key, json.dumps(val), 864000)  # 10天
    

# ======================================================================================================================

async def forward_user_info_get(user_tg_id):
    key = prefix + "forward_user_info" + str(user_tg_id)

    val = conn.get(key)
    if val is None:
        return None
    else:
        return val.decode('utf-8')


async def forward_user_info_set(user_tg_id, info):
    key = prefix + "forward_user_info" + str(user_tg_id)

    conn.set(key, info, 180)  # 3分钟
    

# ======================================================================================================================

async def check_user_status(user_id):
    key = prefix + "system_reply_user_redis1" + str(user_id)

    val = conn.exists(key)
    
    if not val:
        return False
    if val == 0:
        return False
    
    return True


async def set_user_status(user_id):
    key = prefix + "system_reply_user_redis1" + str(user_id)

    conn.set(key, "hwdb", 1800)
    

# ======================================================================================================================

async def hwdb_user_get(user_tg_id):
    key = prefix + "hwdb_user_" + str(user_tg_id)

    val = conn11.get(key)
    if val is None:
        return None
    else:
        return json.loads(val)


async def hwdb_user_set(user_tg_id, val):
    key = prefix + "hwdb_user_" + str(user_tg_id)

    conn11.set(key, json.dumps(val))  # forever
    

# ======================================================================================================================

async def at_official_set(data):
    key = prefix + "at_officialz"

    conn.rpush(key, json.dumps(data))
    

def msg_path10_status_get(group_tg_id, user_tg_id):
    key = prefix + "msg_path10_status" + str(group_tg_id) + str(user_tg_id)

    # conn = get_conn()

    val = conn.get(key)
    if val is None:
        return False
    else:
        return True


def msg_path10_status_set(group_tg_id, user_tg_id):
    key = prefix + "msg_path10_status" + str(group_tg_id) + str(user_tg_id)
    
    # conn = get_conn()

    conn.set(key, 1, 60 * 5)  # 5分钟


def setPrivateMode(userTgId, mode):
    key = prefix + ":private:mode:" + str(userTgId)

    conn.set(key, mode, ex=600)


def getPrivateMode(userTgId):
    key = prefix + ":private:mode:" + str(userTgId)

    val = conn.get(key)
    if val is None:
        return 'ss'
    else:
        return val.decode('utf-8')


def getHotWords():
    key = prefix + ":search:hotwords"

    data = conn.get(key)
    if data is None:
        data = db.getHotWords()
        conn.set(key, json.dumps(data), ex=3600)
    else:
        data = json.loads(data)

    return data


async def getTodayAdsData(position=1):
    key = prefix + ":today:ads:" + str(position)

    data = conn.get(key)
    if data is None:
        entries = await db.getTodayAdsData()
        if entries is None or len(entries) == 0:
            return []

        adsIds = []
        keywordIds = []
        for entry in entries:
            adsIds.append(entry['ads_id'])
            keywordIds.append(entry['keyword_id'])

        ads = await db.getAdsByIds(adsIds, position)
        keywords = await db.getKeywordByIds(keywordIds)

        data = {}
        for entry in entries:
            adsId = str(entry['ads_id'])
            keywordId = str(entry['keyword_id'])

            if adsId not in ads:
                continue

            if adsId not in data:
                data[adsId] = ads[adsId]
                data[adsId]['keywords'] = []

            data[adsId]['keywords'].append(keywords[keywordId]['name'])

        res = conn.set(key, json.dumps(data), ex=3600)
    else:
        data = json.loads(data)

    return data


async def getGroupBusiness(businessId):
    key = prefix + ":business:all"

    business = conn.get(key)
    if business is None:
        business = await db.getBusiness()

        res = conn.set(key, json.dumps(business), ex=3600)
    else:
        business = json.loads(business)

    if str(businessId) in business:
        return business[str(businessId)]

    return None


async def getGroupMangers(chatId):
    key = prefix + ":group:manage:" + str(chatId)

    manages = conn.get(key)
    if manages is None:
        manages = await db.getManages(chatId)

        res = conn.set(key, json.dumps(manages), ex=3600)
    else:
        manages = json.loads(manages)

    data = {'boss': None, 'trader': None}
    for manage in manages:
        if manage['custom_title'] == "本公群老板，小心骗子假冒":
            data['boss'] = manage
        elif manage['custom_title'] == "本公群业务员，小心骗子假冒":
            data['trader'] = manage

    return data


def updateFakeGroups(groupId, botId):
    key = prefix + ":fakeGroupIds"

    conn11.zadd(key, {groupId: botId})
