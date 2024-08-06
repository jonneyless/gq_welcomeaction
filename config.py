from environs import Env

env = Env()
env.read_env()

mysqlInfo = {
    "host": env.str("DB_HOST", "127.0.0.1"),
    "db": env.str("DB_DATABASE", "welcome"),
    "user": env.str("DB_USER", "root"),
    "passwd": env.str("DB_PASS", "7a89afd87c0cd015"),
    "port": env.int("DB_PORT", 3306),
}

redisInfo = {
    "host": env.str("REDIS_HOST", "127.0.0.1"),
    "port": env.int("REDIS_PORT", 6379),
}

bot_token = env.str('BOT_TOKEN', "5759299188:AAHSTq6xbLEb9oWFBkLonFtn3nDLzLkR_EE")
bot_id = env.int('BOT_ID', 5759299188)
bot_url = "https://api.telegram.org/bot%s/" % bot_token

ybjqr_bot_token = env.str('BOT_TOKEN', "5759299188:AAHSTq6xbLEb9oWFBkLonFtn3nDLzLkR_EE")
ybjqr_bot_id = env.int("WELCOME_BOT_ID", 2094467068)
hwjzbot_id = 5217006539
EVE9529_bot_id = 1909582409

check_words = ["验群", "担保信息", "群信息", "验下群", "验证", "驗群"]

limit_text_len = 120
limit_text_len_bank = 400

limit_time = 1
limit_num = 20

limit_all_time = 60
limit_all_group_num = 10
limit_cancel_restrict = 365  # 天

welcome_true_status = 2
welcome_false_status = 2

welcome_true_info = ""
welcome_false_info = ""

photo_limit_type_num = 3
photo_limit_time = 20
photo_limit_day = 10

media_path = "/images/"