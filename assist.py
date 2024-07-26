import html
import random
import re
import string
import time


# ======================================================================================================================

def htmlspecialchars_php(temp):
    return html.escape(temp)


def isEmoji(content):
    if not content:
        return False
    if u"\U0001F600" <= content and content <= u"\U0001F64F":
        return True
    elif u"\U0001F300" <= content and content <= u"\U0001F5FF":
        return True
    elif u"\U0001F680" <= content and content <= u"\U0001F6FF":
        return True
    elif u"\U0001F1E0" <= content and content <= u"\U0001F1FF":
        return True
    else:
        return False


def is_number(s):
    if s is None:
        return False
    
    if len(s) == 0:
        return False

    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        for i in s:
            unicodedata.numeric(i)
        return True
    except (TypeError, ValueError):
        pass
    return False


def to_num(num, temp=0):
    try:
        if int(num) == float(num):
            return int(num)
    
        if temp == 0:
            return round(num, 1)
        else:
            num = float(num)
            return round(num, temp)
    except:
        pass
    
    return num


def to_num2(num):
    num = float(num)
    return round(num, 2)


def get_num_len(num):
    num = float(num)
    if int(num) == num:
        return 0

    num = str(num)
    temp = num.find(".")
    if temp > -1:
        return len(num[(temp + 1):])
    else:
        return 0


def get_current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def get_hour_int():
    hour = time.strftime("%H", time.localtime())
    return int(hour)
    

def get_day_int():
    hour = time.strftime("%d", time.localtime())
    return int(hour)


def get_today_time():
    return time.strftime("%Y-%m-%d", time.localtime())


def get_today_timestamp():
    return time2timestamp(get_today_time(), False)


def get_current_timestamp():
    return int(time.time())


def get_tomorrow_timestamp():
    today_timestamp = get_today_timestamp()
    return int(today_timestamp) + 86400
    
    
def time2timestamp(t, flag=True):
    if flag:
        return int(time.mktime(time.strptime(t, '%Y-%m-%d %H:%M:%S')))
    else:
        return int(time.mktime(time.strptime(t, '%Y-%m-%d')))


def timestamp2time(t):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))


def get_simple_time(created_at):
    created_at = str(created_at)
    space = created_at.find(" ")
    return created_at[(space + 1):]


def get_simple_day(created_at):
    created_at = str(created_at)
    space = created_at.split(" ")
    return space[0]
    
    
# ======================================================================================================================

def has_special_text(text):
    return has_bank(text), has_coin(text), has_zhifubao(text)


def is_url(text):
    pattern = re.compile(r"^([a-zA-z]+:\/\/[^\s]*)$")
    result = re.search(pattern, text)

    if result is None:
        return False
    else:
        return True


def has_bank(text):
    pattern = re.compile(r"([1-9])(\d{15}|\d{18})")
    result = re.search(pattern, text)

    if result is None:
        return False
    else:
        return True


def has_coin(text):
    pattern = re.compile(r"T[A-Za-z0-9]{20,}")
    result = re.search(pattern, text)
    if result is None:
        return False
    else:
        return True


def has_zhifubao(text):
    if has_email(text) or has_phone(text):
        return True
    else:
        return False


def has_email(text):
    pattern_email = re.compile(r"\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*")
    result_email = re.search(pattern_email, text)

    if result_email is None:
        return False
    else:
        return True


def has_phone(text):
    pattern_phone = re.compile(
        r"(?:\+?86)?1(?:3\d{3}|5[^4\D]\d{2}|8\d{3}|7(?:[235-8]\d{2}|4(?:0\d|1[0-2]|9\d))|9[0-35-9]\d{2}|66\d{2})\d{6}")
    result_phone = re.search(pattern_phone, text)

    if result_phone is None:
        return False
    else:
        return True


def has_huione(text):
    flag = False
    if text.find("汇旺") >= 0:
        flag = True

    return flag


# ======================================================================================================================

def handle_chat(chat_id, chat):
    obj = {
        "id": chat_id,
        "tg_id": chat_id,
        "group_tg_id": chat_id,
        "title": "",
    }

    if hasattr(chat, "title") and chat.title is not None:
        obj["title"] = chat.title

    return obj


# 处理从bot接口中获得数据
def handle_user_arr(user_temp):
    user = {
        "id": user_temp["id"],
        "tg_id": user_temp["id"],
        "user_tg_id": user_temp["id"],
        "username": "",
        "firstname": "",
        "lastname": "",
    }

    if "username" in user_temp:
        user["username"] = user_temp["username"]
    if "first_name" in user_temp:
        user["firstname"] = user_temp["first_name"]
    if "last_name" in user_temp:
        user["lastname"] = user_temp["last_name"]

    firstname = user["firstname"]
    lastname = user["lastname"]

    firstname = firstname.replace("'", "")
    lastname = lastname.replace("'", "")
    
    firstname = firstname.replace("\\", "")
    lastname = lastname.replace("\\", "")

    firstname = htmlspecialchars_php(firstname)
    lastname = htmlspecialchars_php(lastname)

    fullname = firstname + lastname

    user["firstname"] = firstname
    user["lastname"] = lastname
    user["first_name"] = firstname
    user["last_name"] = lastname

    return user
    
    
def handle_sender(sender):
    obj = {
        "id": sender.id,
        "tg_id": sender.id,
        "user_tg_id": sender.id,
        "username": "",
        "firstname": "",
        "lastname": "",
        "fullname": "",
        "first_name": "",
        "last_name": "",
        "full_name": "",
        "intro": "",
    }

    if hasattr(sender, "username") and sender.username is not None:
        obj["username"] = sender.username

    if hasattr(sender, "first_name") and sender.first_name is not None:
        obj["firstname"] = sender.first_name

    if hasattr(sender, "last_name") and sender.last_name is not None:
        obj["lastname"] = sender.last_name

    firstname = obj["firstname"]
    lastname = obj["lastname"]

    firstname = firstname.replace("'", "")
    lastname = lastname.replace("'", "")
    
    firstname = firstname.replace("\\", "")
    lastname = lastname.replace("\\", "")

    firstname = htmlspecialchars_php(firstname)
    lastname = htmlspecialchars_php(lastname)

    fullname = firstname + lastname

    obj["firstname"] = firstname
    obj["lastname"] = lastname
    obj["first_name"] = firstname
    obj["last_name"] = lastname
    
    obj["fullname"] = fullname
    obj["full_name"] = fullname

    return obj


# ======================================================================================================================

def is_right_pwd(text):
    text_len = len(text)
    
    if text_len < 8 or text_len > 18:
        return False
    
    pattern = re.compile(r"^[0-9a-zA-Z]*$")
    result = re.search(pattern, text)
    
    if result is None:
        return False
        
    return True
    
    
def replace_string_en(text):
    punctuation_str = string.punctuation
    for i in punctuation_str:
        text = text.replace(i, "")
    
    # punctuation_str = punctuation
    # for i in punctuation_str:
    #     text = text.replace(i, "")
        
    return text
    

def has_prev(page):
    flag = False
    if page > 1:
        flag = True

    return flag


def has_next(page, count, page_len):
    flag = False
    if page * page_len < count:
        flag = True

    return flag
    
    
def get_max_page(count, page_len):
    page_temp = count / page_len
    page = int(page_temp)
    
    if page_temp > page:
        page = page + 1
        
    return page
    
    
def get_danbao_opened_day(created_at):
    now_timestamp = get_current_timestamp()
    created_at_timestamp = time2timestamp(str(created_at))
    
    return int((now_timestamp - created_at_timestamp) / 86400)
    

def get_media_dir(chat_id, message_tg_id, media_path):

    media_name = get_random_file_name(message_tg_id)
    media_dir = media_path + media_name

    return media_dir, media_name


def get_file_dir_name():
    return str(time.strftime("%Y_%m_%d", time.localtime()))


def get_random_file_name(message_tg_id):
    return str(int(time.time())) + str(random.randint(0, 99)) + str(message_tg_id)
    
    
async def download_media(bot, event, chat_id, message_tg_id, media_path):
    media_dir, media_name = get_media_dir(chat_id, message_tg_id, media_path)

    media_dir_full = await bot.download_media(event.message, media_dir)
    
    media_type = media_dir_full.replace(media_dir, "")

    media_name_full = media_dir + media_type

    return media_name_full
    
    