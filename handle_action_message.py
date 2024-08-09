import telethon.tl.types
from telethon.tl.functions.users import GetFullUserRequest

import tg
from assist import *
from config import *
from helpp import *


async def event_delete(event):
    try:
        await event.delete()
    except Exception:
        pass


async def index(bot, event, group, group_tg_id, action_message):
    if not hasattr(action_message, "action"):
        return

    action = action_message.action
    from_id = action_message.from_id

    if isinstance(action, telethon.tl.types.MessageActionChatAddUser):
        await event_delete(event)

        if not hasattr(from_id, "user_id"):
            return

        users = action.users
        for user_id in users:
            await handle_in(bot, event, group, group_tg_id, int(from_id.user_id), user_id)
    elif isinstance(action, telethon.tl.types.MessageActionChatJoinedByLink):
        await event_delete(event)

        user_id = from_id.user_id
        await handle_in(bot, event, group, group_tg_id, user_id, user_id)
    elif isinstance(action, telethon.tl.types.MessageActionChatDeleteUser):
        await event_delete(event)


async def handle_in(bot, event, group, group_tg_id, from_id, user_id):
    user_tg_id = int(user_id)

    print('user enter:', user_tg_id)

    if user_tg_id == ybjqr_bot_id or user_tg_id == bot_id:
        # 非官方人员拉机器人入群
        is_official = await db.official_one(from_id)
        if is_official is None:
            await kickSelf(bot, event, from_id, bot_id, group_tg_id, user_tg_id)
            return

        if group is not None and group['flag'] != 2 and group['flag'] != 4:
            await kickSelf(bot, event, from_id, bot_id, group_tg_id, user_tg_id)
            return

        # 群管里官方人员不足3个
        admins = tg.getChatAdmins(group_tg_id)
        officialCount = 0
        for userId in admins:
            if await db.official_one(userId) is not None:
                officialCount = officialCount + 1
        if officialCount < 3:
            await kickSelf(bot, event, from_id, bot_id, group_tg_id, user_tg_id)
            return

    is_official = await db.official_one(user_tg_id)
    if is_official is not None:
        print("%s is official" % user_tg_id)
        await tg.promote_admin(bot, group_tg_id, user_tg_id)

    newer = None
    try:
        newer = await bot.get_entity(user_tg_id)

        print(newer)
    except:
        return
    
    if newer is None:
        return
    is_bot = False
    if hasattr(newer, "bot") and newer.bot:
        is_bot = True

    newer = handle_sender(newer)

    if is_bot is False:
        result = await bot(GetFullUserRequest(
            id=newer['id'],
        ))
        newer['intro'] = result.full_user.about

    print(newer)
    
    await check_user(bot, event, group, newer)
    
    userr = newer
    sender = userr

    # 新用户是机器人
    if is_bot:
        if group["flag"] == 2:
            in_flag = False
            
            is_official_from = await db.official_one(from_id)
            if is_official_from is not None:
                is_white_bot = await db.white_user_bot_one(user_tg_id)
                if is_white_bot is not None:
                    in_flag = True
            
            if not in_flag:
                reason_log = "迎宾机器人用户进群(真公群)，非官方拉非白名单机器人进群"
                
                await tg.restrict(bot, group_tg_id, user_tg_id, 1, reason_log)
                await tg.kick(bot, group_tg_id, user_tg_id, reason_log)
                return
        else:
            is_admin = await db.group_admin_one(group_tg_id, from_id)

            if is_admin is None:
                reason_log = "迎宾机器人用户进群(游戏群)，非管理员拉机器人进群"
                
                await tg.restrict(bot, group_tg_id, user_tg_id, 1, reason_log)
                await tg.kick(bot, group_tg_id, user_tg_id, reason_log)
                return

    if is_official is not None:
        pass
    else:
        is_cheat = await db.cheat_one(user_tg_id)
        if is_cheat is not None:
            await tg.kick(bot, group_tg_id, user_tg_id, "迎宾机器人用户进群，骗子库用户")
            return

        is_general_user_flag = await is_general_user(group_tg_id, user_tg_id)
        if is_general_user_flag:
            if has_huione(sender["fullname"]):
                is_white = await db.white_one(user_tg_id)
                # 非白名单
                if is_white is None:
                    reason_log = "迎宾机器人用户进群，用户昵称中包含汇旺"
                    
                    await tg.kick(bot, group_tg_id, user_tg_id, reason_log)
                    await tg.delete_day(group_tg_id, user_tg_id, reason_log)
                    return

            # 新用户是机器人
            # if is_bot:
            #     is_admin = await db.group_admin_one(group_tg_id, from_id)
            #     if is_admin is None:
            #         await tg.restrict(bot, group_tg_id, user_tg_id, 1)
            #         await tg.kick(bot, group_tg_id, user_tg_id)
            #         return

            fullname_restrict_word = await has_fullname_restrict_word(sender["fullname"])
            if fullname_restrict_word is not None:
                is_white = await db.white_one(user_tg_id)
                if is_white is None:
                    reason_log = "迎宾机器人用户进群，昵称中包含违禁词：%s" % fullname_restrict_word["name"]
                    
                    if fullname_restrict_word["level"] == 1:
                        await tg.restrict(bot, group_tg_id, user_tg_id, 1, reason_log)

                    await tg.kick(bot, group_tg_id, user_tg_id, reason_log)
                    await db.cheat_save(user_tg_id, sender, reason_log)

                    return

            username_restrict_word = await has_username_restrict_word(sender["username"])
            if username_restrict_word is not None:
                is_white = await db.white_one(user_tg_id)
                if is_white is None:
                    reason_log = "迎宾机器人用户进群，用户名中包含违禁词：%s" % username_restrict_word["name"]
                    
                    if username_restrict_word["level"] == 1:
                        await tg.restrict(bot, group_tg_id, user_tg_id, 1, reason_log)
                    await tg.kick(bot, group_tg_id, user_tg_id, reason_log)
                    await db.cheat_save(user_tg_id, sender, reason_log)

                    return

            intro_restrict_word = await has_intro_restrict_word(sender["intro"])
            if intro_restrict_word is not None:
                is_white = await db.white_one(user_tg_id)
                if is_white is None:
                    reason_log = "迎宾机器人用户进群，用户简介中包含违禁词：%s" % intro_restrict_word["name"]

                    if intro_restrict_word["level"] == 1:
                        await tg.restrict(bot, group_tg_id, user_tg_id, 1, reason_log)
                    await tg.kick(bot, group_tg_id, user_tg_id, reason_log)
                    await db.cheat_save(user_tg_id, sender, reason_log)

                    return

            group_admin_like = await like_admin(group_tg_id, sender)
            if group_admin_like:
                reason_log = "迎宾机器人用户进群，用户名字和群内管理员相似，群名%s" % group["title"]
                
                await tg.kick(bot, group_tg_id, user_tg_id, reason_log)
                await tg.delete_day(group_tg_id, user_tg_id, reason_log)
                await db.cheat_save(user_tg_id, sender, reason_log)

                return

    await create_and_update_user(bot, group_tg_id, newer)

    # people_limit = 1 进群自动禁言入协议号库
    # people_limit = 3 开启入群验证
    # people_limit = 2 关闭
    if group["people_limit"] == 1:
        await tg.restrict(bot, group_tg_id, user_tg_id, 1, "迎宾机器人用户进群，进群自动禁言")
        await db.session_user_save(group_tg_id, user_tg_id)
    elif group["people_limit"] == 3:
        await tg.restrict(bot, group_tg_id, user_tg_id, 1, "迎宾机器人用户进群，进群验证禁言")
        await tg.send_cancel_restrict_button(bot, userr, group_tg_id, user_tg_id)

    group_title = group["title"]
    if group_title.find("已退押") >= 0:
        print("%s do not send welcome info" % group_title)
        return

    if group["welcome_status"] == 1 and group["open_status"] == 1:
        limit_one_time = group["limit_one_time"]
        last_welcome_message_id = await db_redis.last_welcome_message_id_get(group_tg_id)
        if last_welcome_message_id is None:
            m = await tg.send_welcome_info(bot, group, newer, group_tg_id)
            if m is not None and hasattr(m, "id"):
                await db_redis.last_welcome_message_id_set(group_tg_id, m.id, limit_one_time)
                await asyncio.sleep(120)
                await tg.delete_only(bot, group_tg_id, m.id)
