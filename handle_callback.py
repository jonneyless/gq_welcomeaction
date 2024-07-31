import db
import db_redis
import template
from assist import handle_sender


async def index(bot, event, chat_id, sender_id, msg_id, info, args):
    if chat_id == sender_id:
        if info == "cancel_boss_pwd":
            try:
                await event.delete()
            except:
                print("delete error")
            await db_redis.group_boss_pwd_status_del(sender_id)
            
        elif info == "sure_boss_pwd":
            pwd = args["pwd"]
            
            group_admin_boss = await db.group_admin_boss_one(sender_id)
            if group_admin_boss is None:
                await db_redis.group_boss_pwd_status_del(sender_id)
                await event.answer(message="无权进行此操作", alert=True)
                return
            
            group_boss_pwd = await db.group_boss_pwd_one(sender_id)
            if group_boss_pwd is not None:
                await db_redis.group_boss_pwd_status_del(sender_id)
                await event.answer(message="您已经设置过密码", alert=True)
                return
            
            sender = await event.get_sender()
            if sender is not None:
                sender = handle_sender(sender)
            else:
                sender = {
                    "id": sender_id,
                    "tg_id": sender_id,
                    "user_tg_id": sender_id,
                }
            
            await db.group_boss_pwd_set(sender, pwd)
            await db_redis.group_boss_pwd_status_del(sender_id)
            await event.answer(message="设置成功", alert=True)
            try:
                await event.delete()
            except:
                print("delete error")
        elif info == "search":
            text = args["k"]
            page = args["p"]
            type = args["t"]
            sort = args["s"]

            ads = await template.ads_top_position(text)

            page = int(page)
            type = int(type)
            
            groups = None
            groups_count = 0
            if type == 2:
                groups = await db.groups_search_by_rules(text, page, sort)
                groups_count = await db.groups_search_count_by_rules(text)
                if groups_count is not None:
                    groups_count = groups_count["count_num"]
            else:
                groups = await db.groups_search_by_title(text, page, sort)
                groups_count = await db.groups_search_count_by_title(text)
                if groups_count is not None:
                    groups_count = groups_count["count_num"]
                
            if groups == None:
                await bot.edit_message(entity=chat_id, message=msg_id, text="该内容无搜索结果，请重新输入")
            else:
                try:
                    buttons = template.button_search_get(text, page, groups_count, type, sort)
                    buttons = await template.ads_bottom_position(buttons, text)
                    await bot.edit_message(entity=chat_id, message=msg_id, text=ads + template.msg_search_get(groups, page, groups_count), buttons=buttons, parse_mode="html", link_preview=False)
                except:
                    print("reply error")
