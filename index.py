from telethon import TelegramClient, events

from telethon.tl.functions.users import GetFullUserRequest
import handle_danbao_message
import handle_action_message
import handle_group_message
import handle_private_message
from config import *
from helpp import create_and_update_group, create_and_update_user, check_user, handle_chat
from assist import handle_sender
import db
import tg
import handle_callback
import db_redis
from template import *
from img import download_image



bot = TelegramClient('welcomeAction', 27127438, 'a103aa33a68882267db12de32a2d9f86').start(
    bot_token=bot_token)


def need_replyer(text):
    flag = False
    if (text == "设置群老板") or (text == "设置业务员") or (text == "显示id") or (text == "显示ID") or (text == "id") or (text == "ID"):
        flag = True
    
    return flag
    
    
async def init(event, message, chat_id, sender_id, text, edit=False):
    pass
    # chat = await event.get_chat()
    # if chat is None:
    #     return
    
    # chat = handle_chat(chat_id, chat)
    
    # print(chat)
    
    # group_tg_id = chat["tg_id"]
    # group_title = chat["title"]
    
    # obj = await db.user_group_single(sender_id)
    # if obj is None:
    #      await db.user_group_save(chat_id, sender_id)   
        
    # user = await db.user_one(sender_id)

    # if sender is None:
    #     return
    # sender = handle_sender(sender)
    
    # await db.user_update_tgid(sender_id, sender)
    
    
    # if text == "真公群":
    #     group = await db.group_one(group_tg_id)
        
    #     if group is None:
    #         await db.group_save(group_tg_id, group_title)

    #     await db.group_set_flag(group_tg_id)
    #     await db.group_flush(group_tg_id)
    #     await tg.update_admins(group_tg_id)
        
    #     await event.reply(message="真公群设置成功")
        
    #     return
    
    # message_tg_id = message.id
    
    # await download_image(bot, event, message, group_tg_id, sender_id, message_tg_id)    
    # try:
    #     await download_image(bot, event, message, group_tg_id, sender_id, message_tg_id)
    # except:
    #     print("download_image exception...")
    
    # group = await db.group_one(group_tg_id)
    # if group is not None:
    #     await db.group_set_title(group_tg_id, group_title)
    
    # if text == "进群时间":
    #     obj = await db.user_group_single(sender_id)
    #     if obj is None:
    #         return
            
    #     await event.reply(message=str(obj["created_at"]))
        
    #     return
    
    # if text.find("进群时间") >= 0:
    #     created_at = text.replace("进群时间", "")
    #     # created_at = created_at.replace(" ", "")
        
    #     await db.user_group_set(chat_id, sender_id, created_at)
        
    #     await event.reply(message="设置成功")
        
    #     return
    
    
    
    
    # await handle_group_message.set_flag(bot, event, message, None, None, chat_id, sender_id, text, edit)
    
    
    
    # group = await create_and_update_group(chat_id, chat)
    # if group is None:
    #     return
    
    # if group is None:
    #     return
    
    # if group["flag"] == 1 or group["flag"] == 3:
    #     return

    # sender = await event.get_sender()
    # if sender is None:
    #     return
    # userr = await create_and_update_user(bot, group["tg_id"], sender)
    # if userr is None:
    #     return
    
    # await check_user(bot, event, group, userr)

    # reply_tg_id = None
    # if event.reply_to is not None:
    #     if need_replyer(text):
    #         reply_message_id = event.reply_to.reply_to_msg_id
    #         message = await db.message_one(chat_id, reply_message_id)
    #         if message is not None:
    #             reply_tg_id = message["user_tg_id"]
    
    # danbao_arr = [
    #     "担保开启",
    #     "担保刷新",
    #     "担保关闭",
    #     "月费已全部收取",
    #     "月费全部不收取",
    #     "月费已收取",
    #     "月费不收取",
    # ]
    # if text in danbao_arr or text.find("改月费") == 0:
    #     await handle_danbao_message.index(bot, event, message, group, userr, chat_id, sender_id, text, reply_tg_id)
        
    # await handle_group_message.index(bot, event, message, group, userr, chat_id, sender_id, text, reply_tg_id, edit)
    
    
    # check_flag = False
    # for check_word in check_words:
    #     if text.find(check_word) >= 0:
    #         check_flag = True
    #         break

    # print(check_flag)

    # if check_flag:
    #     status_check_group = await db_redis.status_check_group_get(group_tg_id)
        
    #     print(status_check_group)

    #     if status_check_group is None:
    #         group_official_admins = await db.get_group_official_admin(group_tg_id)
    #         group_official_admin_num = len(group_official_admins)
            
    #         print(group_official_admins)
            
    #         m = None
    #         if group_official_admin_num >= 2:
    #             chat = await bot.get_entity(group_tg_id)
    #             if chat is None:
    #                 return

    #             info = msg_notice_group_true(group_official_admins, chat.title)
    #             m = await event.reply(message=info)
    #         else:
    #             info = msg_notice_group_false()
    #             m = await event.reply(message=info)

    #         if m is not None:
    #             last_message_id = await db_redis.group_last_check_message_id_get(group_tg_id)
    #             if last_message_id is not None:
    #                 last_message_id = int(last_message_id)
    #                 await bot.delete_messages(group_tg_id, last_message_id)

    #             message_id = int(m.id)
    #             await db_redis.status_check_group_set(group_tg_id)
    #             await db_redis.group_last_check_message_id_set(group_tg_id, message_id)

    #     return
    


def is_private(chat_id, sender_id):
    flag = False
    if chat_id == sender_id and sender_id > 0:
        flag = True

    return flag


@bot.on(events.NewMessage(incoming=True))
async def new_message(event):
    chat_id = event.chat_id
    sender_id = event.sender_id

    if sender_id is None:
        return

    chat_id = int(chat_id)
    sender_id = int(sender_id)

    message = event.message
    text = message.message

    if is_private(chat_id, sender_id):
        pass
        # await handle_private_message.index(bot, event, chat_id, sender_id, text, message)
    else:
        await init(event, message, chat_id, sender_id, text)


@bot.on(events.MessageEdited(incoming=True))
async def message_edit(event):
    pass
    # chat_id = event.chat_id
    # sender_id = event.sender_id

    # if sender_id is None:
    #     return

    # chat_id = int(chat_id)
    # sender_id = int(sender_id)

    # message = event.message
    # text = message.message

    # if is_private(chat_id, sender_id):
    #     return
    # else:
    #     await init(event, message, chat_id, sender_id, text, True)


@bot.on(events.ChatAction())
async def chat_action(event):
    chat_id = event.chat_id
    chat_id = int(chat_id)

    action_message = event.action_message
    if action_message is None:
        return

    chat = await event.get_chat()
    if chat is None:
        return

    group = await create_and_update_group(chat_id, chat)
    if group is None:
        return

    await handle_action_message.index(bot, event, group, chat_id, action_message)


@bot.on(events.CallbackQuery())
async def callback(event):
    chat_id = event.chat_id
    sender_id = event.sender_id

    callback_data = event.query.data
    callback_data = callback_data.decode('utf-8')

    args = {}
    info = callback_data
    if callback_data.find("?") >= 0:
        arr = callback_data.split("?")
        if len(arr) == 2:
            info = arr[0]
            args_temp = arr[1]

            args_temp = args_temp.split("&")
            for item in args_temp:
                item = item.split("=")
                if len(item) == 2:
                    args[item[0]] = item[1]

    if info == "cancelRestrict":
        group_tg_id = int(args["group_tg_id"])
        user_tg_id = int(args["user_tg_id"])

        if (group_tg_id == chat_id) and (user_tg_id == sender_id):
            await event.delete()
            await bot.edit_permissions(group_tg_id, user_tg_id, 1, send_messages=True)
    else:
        msg_id = int(event.query.msg_id)
        
        await handle_callback.index(bot, event, chat_id, sender_id, msg_id, info, args)


def main():
    bot.run_until_disconnected()


if __name__ == '__main__':
    print("init...")

    main()
