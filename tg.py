import asyncio
import json

import requests
from telethon import Button

import db
import db_redis
from assist import handle_user_arr
from config import bot_url
from helpp import get_config_welcome_true_status, get_config_welcome_false_status, get_config_welcome_true_info, get_config_welcome_false_info


async def setChatPermissions(group_tg_id, send=True):
    tg_url = bot_url + "setChatPermissions"
    headers = {
        "Content-Type": "application/json",
    }
    
    permissions = {
        "can_send_messages": send,
        "can_send_audios": False,
        "can_send_documents": False,
        "can_send_photos": send,
        "can_send_videos": send,
        "can_send_video_notes": False,
        "can_send_voice_notes": False,
        "can_send_polls": False,
        "can_send_other_messages": False,
        "can_add_web_page_previews": False,
        "can_change_info": False,
        "can_invite_users": False,
        "can_pin_messages": False,
        "can_manage_topics": False,
    }

    data = {
        "chat_id": group_tg_id,
        "permissions": json.dumps(permissions),
    }
    try:
        response = requests.post(tg_url, json=data, headers=headers, timeout=5)
    except:
        print("requests error...")
    
    
    
async def update_admins(group_tg_id):
    tg_url = bot_url + "getChatAdministrators"
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "chat_id": group_tg_id,
    }
    response = requests.post(tg_url, json=data, headers=headers, timeout=5)

    if response is not None:
        response = json.loads(response.text)
        if ("ok" in response) and ("result" in response):
            admins = response["result"]
            
            admins_tgid_old_temp = await db.group_admin_get_now(group_tg_id)
            admins_tgid_old_arr = []
            for item in admins_tgid_old_temp:
                admins_tgid_old_arr.append(int(item["user_tg_id"]))
                
            admins_tgid_now_arr = []
            for admin in admins:
                adminUser = admin["user"]
                adminUserStatus = admin["status"]
                adminUser = handle_user_arr(adminUser)
                
                admins_tgid_now_arr.append(int(adminUser["tg_id"]))
                
                obj = await db.group_admin_one_now(group_tg_id, adminUser["tg_id"])
                if obj is not None:
                    await db.group_admin_update(obj["id"], adminUser)
                else:
                    await db.group_admin_save(group_tg_id, adminUser, adminUserStatus)
                    
            for admins_tgid_old in admins_tgid_old_arr:
                if admins_tgid_old not in admins_tgid_now_arr:
                    await db.group_admin_delete(group_tg_id, admins_tgid_old)


async def promote_admin(bot, group_tg_id, user_tg_id):
    tg_url = bot_url + "promoteChatMember"
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "chat_id": group_tg_id,
        "user_id": user_tg_id,
        # "can_manage_chat" => true,
        # "can_post_messages" => true,
        # "can_edit_messages" => true,
        "can_delete_messages": True,
        # "can_manage_voice_chats": True,
        "can_restrict_members": True,
        # "can_promote_members": True,
        # "can_change_info": True,
        "can_invite_users": True,
        "can_pin_messages": True,
    }
    response = requests.post(tg_url, json=data, headers=headers, timeout=5)

    if response is not None:
        response_text = json.loads(response.text)
        print("%s %s %s" % (group_tg_id, user_tg_id, response_text))
    else:
        print("%s %s %s" % (group_tg_id, user_tg_id, response))


async def promote_super_admin(bot, group_tg_id, user_tg_id):
    tg_url = bot_url + "promoteChatMember"
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "chat_id": group_tg_id,
        "user_id": user_tg_id,
        # "can_manage_chat" => true,
        # "can_post_messages" => true,
        # "can_edit_messages" => true,
        "can_delete_messages": True,
        "can_manage_voice_chats": True,
        "can_restrict_members": True,
        "can_promote_members": True,
        "can_change_info": True,
        "can_invite_users": True,
        "can_pin_messages": True,
    }
    response = requests.post(tg_url, json=data, headers=headers, timeout=5)

    if response is not None:
        response_text = json.loads(response.text)
        print("%s %s %s" % (group_tg_id, user_tg_id, response_text))
    else:
        print("%s %s %s" % (group_tg_id, user_tg_id, response))


async def kick(bot, group_tg_id, user_tg_id, reason):
    try:
        await bot.edit_permissions(group_tg_id, user_tg_id, view_messages=False)
    except Exception:
        pass
    
    await db.log_kick_save(group_tg_id, user_tg_id, reason)
    await db.user_group_kick(group_tg_id, user_tg_id)


async def delete_only(bot, group_tg_id, message_tg_id):
    try:
        await bot.delete_messages(group_tg_id, message_tg_id)
    except Exception:
        pass


async def delete(bot, group_tg_id, message_tg_id):
    try:
        await bot.delete_messages(group_tg_id, message_tg_id)
    except Exception:
        pass


async def delete_day(group_tg_id, user_tg_id, reason):
    await db_redis.middleware_delete_day_set({
        "group_tg_id": group_tg_id,
        "user_tg_id": user_tg_id,
        "reason": reason,
    })


async def restrict(bot, group_tg_id, user_tg_id, until_date, reason):
    # view_messages: bool = True,
    # send_messages: bool = True,
    # send_media: bool = True,
    # send_stickers: bool = True,
    # send_gifs: bool = True,
    # send_games: bool = True,
    # send_inline: bool = True,
    # embed_link_previews: bool = True,
    # send_polls: bool = True,
    # change_info: bool = True,
    # invite_users: bool = True,
    # pin_messages: bool = True
    
    try:
        await bot.edit_permissions(entity=group_tg_id, user=user_tg_id, until_date=until_date,
                                   send_messages=False, send_media=False, send_stickers=False, send_gifs=False,
                                   send_games=False, send_inline=False, embed_link_previews=False, 
                                   send_polls=False, change_info=False, invite_users=False, pin_messages=False
                                   )
    except Exception:
        print("tg restrict Exception")
        pass
    
    await db.log_restrict_save(group_tg_id, user_tg_id, until_date, reason)
    # await db.user_group_restrict(group_tg_id, user_tg_id)


async def send(bot, group_tg_id, msg):
    try:
        group_tg_id = int(group_tg_id)
        await bot.send_message(group_tg_id, msg)
    except Exception:
        pass


async def send_cancel_restrict_button(bot, userr, group_tg_id, user_tg_id):
    buttons = [
        [
            Button.inline(text="自主解封",
                          data="cancelRestrict?group_tg_id=%s&user_tg_id=%s" % (group_tg_id, user_tg_id)),
        ],
    ]

    info = "%s 欢迎来到汇旺担保群，点击下方验证，证明你不是机器人，可以自动解除禁言，60秒后自毁" % userr["fullname"]

    m = None

    try:
        m = await bot.send_message(entity=group_tg_id, message=info, buttons=buttons, parse_mode="html")
    except Exception:
        pass

    if m is not None:
        await asyncio.sleep(60)
        try:
            await bot.delete_messages(group_tg_id, m.id)
        except Exception:
            pass


async def send_welcome_info(bot, group, newer, group_tg_id):
    config_welcome_true_status = await get_config_welcome_true_status()
    config_welcome_false_status = await get_config_welcome_false_status()

    welcome_true_status = group["welcome_true_status"]
    welcome_false_status = group["welcome_false_status"]

    title = group["title"]
    welcome_info = group["welcome_info"]

    if welcome_info is None or len(welcome_info) == 0:
        welcome_info = ""

    if group["flag"] == 2 or group["flag"] == 4:
        if config_welcome_true_status == 1 and welcome_true_status == 1:
            welcome_true_info = await get_config_welcome_true_info()
            welcome_info += "\n\n"
            welcome_info += "<b>%s</b>" % welcome_true_info
    elif group["flag"] == 3:
        if config_welcome_false_status == 1 and welcome_false_status == 1:
            welcome_false_info = await get_config_welcome_false_info()
            welcome_info += "\n\n"
            welcome_info += "<b>%s</b>" % welcome_false_info

    info = "欢迎 %s 加入 %s %s" % (newer["fullname"], title, welcome_info)

    buttons = [
        [
            Button.url(text="供求信息", url="https://t.me/gongqiu"),
            Button.url(text="公群导航", url="https://t.me/hwgq"),
        ],
    ]

    m = None
    try:
        m = await bot.send_message(entity=group_tg_id, message=info, buttons=buttons, parse_mode="html")
    except Exception:
        pass

    return m


async def promote_admin_short(group_tg_id, user_tg_id):
    tg_url = bot_url + "promoteChatMember"
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "chat_id": group_tg_id,
        "user_id": user_tg_id,
        "is_anonymous": False,
        "can_manage_chat": False,
        "can_post_messages": False,
        "can_edit_messages": False,
        "can_delete_messages": False,
        "can_manage_voice_chats": False,
        "can_restrict_members": False,
        "can_promote_members": False,
        "can_change_info": False,
        "can_invite_users": True,
        "can_pin_messages": True,
        "can_manage_topics": False,
    }
    response = requests.post(tg_url, json=data, headers=headers, timeout=5)

    flag = False
    if response is not None:
        response_text = json.loads(response.text)
        print(response_text)

        if ("result" in response_text) and response_text["result"]:
            flag = True
    
    return flag
    
    
async def set_admin_title(group_tg_id, user_tg_id, title):
    tg_url = bot_url + "setChatAdministratorCustomTitle"
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "chat_id": group_tg_id,
        "user_id": user_tg_id,
        "custom_title": title
    }
    response = requests.post(tg_url, json=data, headers=headers, timeout=5)

    flag = False
    if response is not None:
        response_text = json.loads(response.text)
        print(response_text)

        if ("result" in response_text) and response_text["result"]:
            flag = True
    
    return flag
    

async def remove_admin(group_tg_id, user_tg_id):
    tg_url = bot_url + "promoteChatMember"
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "chat_id": group_tg_id,
        "user_id": user_tg_id,
        # "can_manage_chat" => true,
        # "can_post_messages" => true,
        # "can_edit_messages" => true,
        "can_delete_messages": False,
        "can_manage_voice_chats": False,
        "can_restrict_members": False,
        "can_promote_members": False,
        "can_change_info": False,
        "can_invite_users": False,
        "can_pin_messages": False,
    }
    response = requests.post(tg_url, json=data, headers=headers, timeout=5)

    if response is not None:
        return json.loads(response.text)
    else:
        return None


async def recover_admin(bot, group_tg_id, user_tg_id):
    tg_url = bot_url + "promoteChatMember"
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "chat_id": group_tg_id,
        "user_id": user_tg_id,
        "is_anonymous": False,
        "can_manage_chat": False,
        "can_post_messages": False,
        "can_edit_messages": False,
        "can_delete_messages": True,
        "can_manage_voice_chats": False,
        "can_restrict_members": True,
        "can_promote_members": False,
        "can_change_info": False,
        "can_invite_users": True,
        "can_pin_messages": True,
        "can_manage_topics": False,
    }
    response = requests.post(tg_url, json=data, headers=headers, timeout=5)

    flag = False
    if response is not None:
        response_text = json.loads(response.text)
        print(response_text)

        if ("result" in response_text) and response_text["result"]:
            flag = True
    
    return flag
    
    # try:
    #     await bot.edit_admin(int(group_tg_id), int(user_tg_id),
    #         change_info = False,
    #         post_messages = True,
    #         edit_messages = True,
    #         delete_messages = True,
    #         ban_users = True,
    #         invite_users = True,
    #         pin_messages = True,
    #         add_admins = False,
    #         manage_call = False,
    #         anonymous = False,
    #         is_admin = True,
    #         title = title)
    # except:
    #     pass
    
    
async def promote_empty_admin(bot, group_tg_id, user_tg_id, title = ""):
    tg_url = bot_url + "promoteChatMember"
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "chat_id": group_tg_id,
        "user_id": user_tg_id,
        "is_anonymous": False,
        "can_manage_chat": True,
        "can_post_messages": False,
        "can_edit_messages": False,
        "can_delete_messages": False,
        "can_manage_voice_chats": False,
        "can_manage_video_chats": False,
        "can_restrict_members": False,
        "can_promote_members": False,
        "can_change_info": False,
        "can_invite_users": False,
        "can_pin_messages": False,
        "can_post_stories": False,
        "can_edit_stories": False,
        "can_delete_stories": False,
        "can_manage_topics": False,
    }
    response = requests.post(tg_url, json=data, headers=headers, timeout=5)
    
    flag = False
    if response is not None:
        response_text = json.loads(response.text)
        print(response_text)

        if ("result" in response_text) and response_text["result"]:
            flag = True

    return flag
    
    
async def createBotApproveLink(group_tg_id):
    tg_url = bot_url + "createChatInviteLink"
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "chat_id": group_tg_id,
        "name": "qunguanApproveLink",
        "creates_join_request": True,
    }
    response = requests.post(tg_url, json=data, headers=headers, timeout=10)

    link = None
    if response is not None:
        response_text = json.loads(response.text)
        if ("result" in response_text) and response_text["result"]:
            link = response_text["result"]["invite_link"]

    return link
    
    
# ======================================================================================================================


# async def setChatTitle(group_tg_id, title):
#     tg_url = bot_url + "setChatTitle"
#     headers = {
#         "Content-Type": "application/json",
#     }
#     data = {
#         "chat_id": group_tg_id,
#         "title": title,
#     }
#     response = requests.post(tg_url, json=data, headers=headers, timeout=10)

#     flag = False
#     if response is not None:
#         response_text = json.loads(response.text)
#         if ("result" in response_text) and response_text["result"]:
#             flag = True
      
#     return flag
    
    
# async def unpinAllChatMessages(group_tg_id):
#     tg_url = bot_url + "unpinAllChatMessages"
#     headers = {
#         "Content-Type": "application/json",
#     }
#     data = {
#         "chat_id": group_tg_id,
#     }
#     response = requests.post(tg_url, json=data, headers=headers, timeout=10)

#     flag = False
#     if response is not None:
#         response_text = json.loads(response.text)
#         if ("result" in response_text) and response_text["result"]:
#             flag = True
      
#     return flag
    

# async def setChatDescriptionEmpty(group_tg_id):
#     tg_url = bot_url + "setChatDescription"
#     headers = {
#         "Content-Type": "application/json",
#     }
#     data = {
#         "chat_id": group_tg_id,
#         "description": "",
#     }
#     response = requests.post(tg_url, json=data, headers=headers, timeout=10)

#     flag = False
#     if response is not None:
#         response_text = json.loads(response.text)
#         if ("result" in response_text) and response_text["result"]:
#             flag = True
      
#     return flag
    
    