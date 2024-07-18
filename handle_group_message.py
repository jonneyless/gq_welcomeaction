import telethon.tl.types
import asyncio

from config import check_words, ybjqr_bot_id
from helpp import *
from template import *
import tg
from assist import get_hour_int
import db_redis


async def index(bot, event, message, group, userr, group_tg_id, user_tg_id, text, reply_tg_id, edit=False):
    await handle_text(bot, event, message, group, userr, group_tg_id, user_tg_id, text, reply_tg_id)


async def set_flag(bot, event, message, group, userr, group_tg_id, user_tg_id, text, edit=False):
    if text == "真公群":
        is_official = await db.official_one(user_tg_id)
        if is_official is not None:
            await db.group_set_flag(group["id"])
            await db.group_flush(group_tg_id)
            await tg.update_admins(group_tg_id)
            
            await event.reply(message="真公群设置成功")
        
        return
    
    
async def get_user(chat_id, text, entities):
    user = None
    
    if entities is None:
        return None
    
    for entity in entities:
        if isinstance(entity, telethon.tl.types.MessageEntityMentionName):
            offset = entity.offset
            length = entity.length
            user_id = entity.user_id

            user = await db.user_one(user_id)
            break
            
        if isinstance(entity, telethon.tl.types.MessageEntityMention):
            offset = entity.offset
            length = entity.length
            end = offset + length
            name = text[offset:end]
            name_no_at = name[1:]

            user = await db.user_one_by_username(name_no_at)
            break
    
    return user
    
    
async def promote_admin_title(chat_id, user_tg_id, title):
    flag = False
    result_admin = await tg.promote_admin_short(chat_id, user_tg_id)
    if result_admin:
        result_admin_title = await tg.set_admin_title(chat_id, user_tg_id, title)
        if result_admin_title:
            flag = True
    
    return flag
    
    
async def handle_text(bot, event, message, group, userr, group_tg_id, user_tg_id, text, reply_tg_id):
    # if group["flag"] == 2:
    #     is_admin = await db.group_admin_one(group_tg_id, user_tg_id)
    #     if is_admin is None:
    #         is_message_first = await db.message_first(group_tg_id, user_tg_id)
    #         if is_message_first:
    #             await reply_and_delete_last(group_tg_id, "message_first", bot, event, msg_first_notice())
    #             await db_redis.message_first_set(group_tg_id, user_tg_id)
    #         else:
    #             pass
    
    
    entities = None
    if hasattr(message, "entities"):
        entities = message.entities
    
    if entities is not None:
        await send_night_close_msg(group_tg_id, user_tg_id, bot, event, entities, text, group)
    
    if text == "恢复权限":
        is_official = await db.official_one(user_tg_id)
        if is_official is not None:
            admins = await db.get_group_not_official_admin(group_tg_id)
            admins_empty_num = 0
            admins_empty_num_ok = 0
            
            for admin_item in admins:
                admins_empty_num = admins_empty_num + 1 
                
                flag = await tg.recover_admin(bot, group_tg_id, admin_item["tg_id"])
                if flag:
                    admins_empty_num_ok = admins_empty_num_ok + 1
                
            info = "恢复成功"
            if admins_empty_num != admins_empty_num_ok:
                info = "部分管理恢复失败，请重试"
                
            m = await event.reply(message=info)   
            await asyncio.sleep(3)
            if m is not None and hasattr(m, "id"):
                await tg.delete_only(bot, group_tg_id, m.id)
        return
    
    
    if text == "回收权限":
        is_official = await db.official_one(user_tg_id)
        if is_official is not None:
            admins = await db.get_group_not_official_admin(group_tg_id)
            admins_empty_num = 0
            admins_empty_num_ok = 0
            
            for admin_item in admins:
                admins_empty_num = admins_empty_num + 1 
                
                # custom_title = ""
                # if admin_item["custom_title"] is not None:
                #     custom_title = admin_item["custom_title"]
                # flag = False
                # if len(custom_title) > 0:
                
                flag = await tg.promote_empty_admin(bot, group_tg_id, admin_item["tg_id"])
                    
                if flag:
                    admins_empty_num_ok = admins_empty_num_ok + 1
                    
            if admins_empty_num == admins_empty_num_ok:
                await event.reply(message="回收成功")
            else:
                await event.reply(message="部分管理回收失败，请重试")
        return
    
    
    if text == "回收管理":
        user_official = await db.official_one(user_tg_id)
        if user_official is not None:
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
                print("remove admin %s %s" % (group_tg_id, admin_tg_id))
                tg_result = await tg.remove_admin(group_tg_id, admin_tg_id)
                if tg_result is not None:
                    if "ok" in tg_result and tg_result["ok"]:
                        admins_kick_num_ok = admins_kick_num_ok + 1
                        await db.group_admin_del(group_tg_id, admin_tg_id)
                
            msg = "回收管理成功"
            print("%s %s" % (admins_kick_num_ok, admins_kick_num))
            if admins_kick_num != admins_kick_num_ok:
                msg = "部分管理回收失败，请重试"
            m = await event.reply(message=msg)
            if m is not None and hasattr(m, "id"):
                await asyncio.sleep(3)
                try:
                    await bot.delete_messages(group_tg_id, m.id)
                except Exception:
                    pass
        return
    
    
    if text[0:5] == "设置群老板":
        if reply_tg_id is not None:
            user_official = await db.official_one(user_tg_id)
            if user_official is not None:
                flag = await promote_admin_title(group_tg_id, reply_tg_id, "本公群老板，小心骗子假冒")
    
                if flag:
                    await event.reply(message="设置成功")
                else:
                    await event.reply(message="设置失败，请重新操作")
        else:
            user = await get_user(group_tg_id, text, entities)
            if user is not None:
                user_official = await db.official_one(user_tg_id)
                if user_official is not None:
                    user_tg_id = int(user["tg_id"])
                    
                    flag = await promote_admin_title(group_tg_id, user_tg_id, "本公群老板，小心骗子假冒")
    
                    if flag:
                        await event.reply(message="设置成功")
                    else:
                        await event.reply(message="设置失败，请重新操作")
                return

    if text[0:5] == "设置业务员":
        if reply_tg_id is not None:
            user_official = await db.official_one(user_tg_id)
            if user_official is not None:
                flag = await promote_admin_title(group_tg_id, reply_tg_id, "本公群业务员，小心骗子假冒")
    
                if flag:
                    await event.reply(message="设置成功")
                else:
                    await event.reply(message="设置失败，请重新操作")
        else:
            user = await get_user(group_tg_id, text, entities)
            if user is not None:
                user_official = await db.official_one(user_tg_id)
                if user_official is not None:
                    user_tg_id = int(user["tg_id"])
                    
                    flag = await promote_admin_title(group_tg_id, user_tg_id, "本公群业务员，小心骗子假冒")
    
                    if flag:
                        await event.reply(message="设置成功")
                    else:
                        await event.reply(message="设置失败，请重新操作")
                return
    
    
    if text == "开启权限":
        is_official = await db.official_one(user_tg_id)
        if is_official is not None:
            print("%s is official" % user_tg_id)
            await tg.promote_admin(bot, group_tg_id, user_tg_id)
            m = await event.reply(message="开启成功")
            
            await asyncio.sleep(3)
            await tg.delete_only(bot, group_tg_id, message.id)
            if m is not None and hasattr(m, "id"):
                await tg.delete_only(bot, group_tg_id, m.id)
        return
    
    if text == "上课" or text == "开群":
        if group["flag"] == 2:
            is_admin = await db.group_admin_one(group_tg_id, user_tg_id)
            if is_admin is not None:
                group_title = group["title"]

                if group_title.find("暂停") >= 0 or group_title.find("纠纷") >= 0 or group_title.find("退押") >= 0 or group_title.find("转押") >= 0 or group_title.find("业务变更中") >= 0:
                    m = await bot.send_message(group_tg_id, msg_group_error())
                    if m is not None:
                        last_message_id = await db_redis.group_last_error_message_id_get(group_tg_id)
                        if last_message_id is not None:
                            last_message_id = int(last_message_id)
                            await tg.delete(bot, group_tg_id, last_message_id)
                            
                        message_id = int(m.id)
                        await db_redis.group_last_error_message_id_set(group_tg_id, message_id)
                else:
                    await db.group_set_open_status(group, 1)
                    await bot.send_message(group_tg_id, msg_group_open())
                    await change_group_permission_send(bot, group_tg_id, True)
    
    if text == "下课" or text == "关群":
        if group["flag"] == 2:
            is_admin = await db.group_admin_one(group_tg_id, user_tg_id)
            if is_admin is not None:
                await db.group_set_open_status(group, 2)
                await change_group_permission_send(bot, group_tg_id, False)
                
                m = await bot.send_message(group_tg_id, msg_group_close())
                if m is not None:
                    last_message_id = await db_redis.group_last_close_message_id_get(group_tg_id)
                    if last_message_id is not None:
                        last_message_id = int(last_message_id)
                        await tg.delete(bot, group_tg_id, last_message_id)
    
                    message_id = int(m.id)
                    await db_redis.group_last_close_message_id_set(group_tg_id, message_id)
        return
    
    if text[0:5] == "设置进群语":
        info = text[5:]
        if len(info) > 0:
            is_official = await db.official_one(user_tg_id)
            if is_official is not None:
                await db.group_set_welcome_info(group["id"], info)
                await bot.send_message(group_tg_id, msg_group_set_welcome_info(group["title"], info))
        return

    if text == "显示进群语":
        is_official = await db.official_one(user_tg_id)
        if is_official is not None:
            await bot.send_message(group_tg_id, msg_group_show_welcome_info(group["title"], group["welcome_info"]))
        return

    if text == "关闭进群语":
        is_official = await db.official_one(user_tg_id)
        if is_official is not None:
            await db.group_close_welcome_info(group["id"])
            await bot.send_message(group_tg_id, msg_group_close_welcome_info())
        return

    if text == "真假公群":
        if group["flag"] == 2 or group["flag"] == 4:
            await event.reply(msg_check_group_true())
        elif group["flag"] == 3:
            await event.reply(msg_check_group_false())
        return

    text_len = len(text)
    text_len_2 = text_len - 2
    text_len_4 = text_len - 4
    text_temp = text.lower()
    if text_temp[0:4] == "显示id" or text_temp[0:2] == "id" or text_temp[text_len_2:] == "id" or text_temp[text_len_4:] == "显示id":
        is_official = await db.official_one(user_tg_id)
        if is_official is not None:
            # if reply_tg_id is not None:
            #     info = "该用户tgid：%s" % reply_tg_id
            #     await event.reply(message=info)
            #     return
            
            if hasattr(message, "entities"):
                entities = message.entities
        
                info = ""
                for entity in entities:
                    if isinstance(entity, telethon.tl.types.MessageEntityMentionName):
                        offset = entity.offset
                        length = entity.length
                        user_id = entity.user_id
                        end = offset + length
                        name = text[offset:end]
        
                        if len(info) > 0:
                            info += "\n"
                        info = "%s，%s" % (name, user_id)
                    if isinstance(entity, telethon.tl.types.MessageEntityMention):
                        offset = entity.offset
                        length = entity.length
                        end = offset + length
                        name = text[offset:end]
                        name_no_at = name[1:]
        
                        user_welcome = await db.user_one_by_username(name_no_at)
                        if user_welcome is not None:
                            if len(info) > 0:
                                info += "\n"
                            info += "%s, %s" % (name, user_welcome["tg_id"])
        
                if len(info) > 0:
                    await event.reply(message=info)

        return
    
    if group["business_type"] == 10:
        user_lock_rtn = await db_redis.check_user_status(user_tg_id)
        
        if not user_lock_rtn:
            reply_data = await db.reply_text_get()
            if reply_data is not None:
                reply_data_key = reply_data["keyy"]
                reply_data_val = reply_data["val"]
                
                reply_data_key = reply_data_key.split(",")
                
                for item in reply_data_key:
                    if len(item) > 0:
                        if text.find(item) >= 0:
                            m = await event.reply(message=reply_data_val)
                            if m is not None:
                                last_message_id = await db_redis.group_last_si_message_id_get(group_tg_id)
                                if last_message_id is not None:
                                    last_message_id = int(last_message_id)
                                    await tg.delete(bot, group_tg_id, last_message_id)
                
                                message_id = int(m.id)
                                await db_redis.group_last_si_message_id_set(group_tg_id, message_id)
                                await db_redis.set_user_status(user_tg_id)
                            
                            break

    check_flag = False
    for check_word in check_words:
        if text.find(check_word) >= 0:
            check_flag = True
            break

    if check_flag:
        status_check_group = await db_redis.status_check_group_get(group_tg_id)

        if status_check_group is None:
            group_official_admins = await db.get_group_official_admin(group_tg_id)
            group_official_admin_num = len(group_official_admins)
            
            m = None
            if group_official_admin_num >= 2:
                chat = await bot.get_entity(group_tg_id)
                if chat is None:
                    return

                info = msg_notice_group_true(group_official_admins, chat.title)
                m = await event.reply(message=info)
            else:
                info = msg_notice_group_false()
                m = await event.reply(message=info)

            if m is not None:
                last_message_id = await db_redis.group_last_check_message_id_get(group_tg_id)
                if last_message_id is not None:
                    last_message_id = int(last_message_id)
                    await bot.delete_messages(group_tg_id, last_message_id)

                message_id = int(m.id)
                await db_redis.status_check_group_set(group_tg_id)
                await db_redis.group_last_check_message_id_set(group_tg_id, message_id)

        return


async def change_group_permission_send(bot, group_tg_id, send=True):
    await tg.setChatPermissions(group_tg_id, send)
    # try:
    #     await tg.setChatPermissions(group_tg_id, send)
    #     # await bot.edit_permissions(entity=group_tg_id, view_messages=True, send_messages=send, send_media=send, send_stickers=False, send_gifs=False, send_games=False, send_inline=False, embed_link_previews= False, send_polls=False, change_info=False, invite_users=False, pin_messages=False)
    # except:
    #     print("%s ChatNotModifiedError..." % group_tg_id)


async def send_night_close_msg(group_tg_id, user_tg_id, bot, event, entities, text, group):
    hour = get_hour_int()
    if hour >= 1 and hour < 9:
        print(hour)
        has_official = False
        for entity in entities:
            if isinstance(entity, telethon.tl.types.MessageEntityMention):
                offset = entity.offset
                length = entity.length
    
                username = text[(offset + 1):(offset + length)]
                
                obj = await db.official_one_by_username(username)
                if obj is not None:
                    has_official = True
                    
                    await db_redis.at_official_set({
                        "title": group["title"],
                        "group_tg_id": group_tg_id,
                        "username": username,
                        "text": text,
                        "user_tg_id": user_tg_id,
                    })
                    
                    break
                
        if has_official:
            await reply_and_delete_last(group_tg_id, "night_close_msg", bot, event, msg_night_close_msg())
    else:
        official_num = 0
        usernames = []
        
        for entity in entities:
            if isinstance(entity, telethon.tl.types.MessageEntityMention):
                offset = entity.offset
                length = entity.length

                username = text[(offset + 1):(offset + length)]
                
                if username not in usernames:
                    usernames.append(username)
                
                
        if len(usernames) == 0:
            return
        
        for username in usernames:
            obj = await db.official_one_by_username(username)
            if obj is not None:
                official_num = official_num + 1


        if official_num > 0:
            await user_at_official_set(group_tg_id, user_tg_id)

        at_official_num = await user_at_official_get_num(group_tg_id, user_tg_id)
        if at_official_num > 3:
            print("%s %s redis_at_official_num %s" % (group_tg_id, user_tg_id, at_official_num))
            
            await reply_and_delete_last(group_tg_id, "many_official_time", bot, event,
                                        "小二正在火速赶来，请客官稍安勿躁，不要短时间连续@。")

        if official_num >= 2:
            print("%s %s msg_official_num %s" % (group_tg_id, user_tg_id, official_num))
            
            await reply_and_delete_last(group_tg_id, "many_official", bot, event,
                                        "请只@一位负责处理该事务的工作人员，不要同时@多个工作人员，以免多个工作人员都前来围观，造成资源浪费。")
            
            