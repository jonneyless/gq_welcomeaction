from assist import is_url, is_number, to_num, is_right_pwd, replace_string_en
import db
import db_redis
import template
from assist import handle_sender
from helpp import check_user
import tg



async def index(bot, event, chat_id, sender_id, text, message):
    # await db.user_set_private(sender_id)
    
    sender = await event.get_sender()
    
    print(sender)
    
    if sender is None:
        return
    sender = handle_sender(sender)
    userr = await db.user_one(sender_id)
    if userr is None:
        await db.user_save(sender)
    else:
        await db.user_update(userr["id"], sender)
        
    fwd_from = event.fwd_from
    if fwd_from is not None:
        await handle_forward(bot, event, chat_id, sender_id, text, message, fwd_from)
        return

    if text == "/start":
        await event.respond(template.msg_start_text())
        return

    if text == "/验证":
        group_admin_boss = await db.group_admin_boss_one(sender_id)
        if group_admin_boss is None:
            await event.reply("无权进行此操作")
        else:
            group_boss_pwd = await db.group_boss_pwd_one(sender_id)
            if group_boss_pwd is not None:
                await event.reply("您已经设置过密码")
            else:
                await event.reply(message=template.msg_boss_pwd(), buttons=template.button_cancel_boss_pwd())
                await db_redis.group_boss_pwd_status_set(sender_id)
        return
            
    group_boss_pwd_status = await db_redis.group_boss_pwd_status_get(sender_id)
    if group_boss_pwd_status is not None:
        if is_right_pwd(text):
            try:
                await event.delete()
            except:
                print("delete error")
            await event.respond(message="请检查您输入的内容，是否确认设置为此密码", buttons=template.button_sure_boss_pwd(text))
        else:
            await event.reply(message="输入内容有误，请重新输入，或点击【取消】放弃设置", buttons=template.button_cancel_boss_pwd())
    else:
        text_original = text
        
        text_no_blank = text.replace(" ", "")
        text_no_blank = text.replace("公群", "")
        
        if is_number(text_no_blank):
            await db.log_search_save(sender_id, text, text_original, 0, 2)
            
            num = to_num(text_no_blank)
            
            data = await db.reply_one(num)
            if data is not None:
                reply_val = data["val"]
                if reply_val.find("vip公群") >= 0:
                    in_val = "进群后请联系官方客服 @hwdb 自助验群后再交易，如因客户不验群产生的一切后果自负。"
                    reply_val = reply_val.replace(in_val, "")
                    await event.reply(reply_val)
                    m = await event.reply(in_val)
                    if m is not None and hasattr(m, "id"):
                        await db.log_yanzheng_vip_save(sender_id, m.id, num, reply_val)
                else:
                    await event.reply(data["val"])
            else:
                if num < 90000 and num > 0:
                    group_by_num = await db.group_one_by_num(num)
                    if group_by_num is None:
                        await event.reply("不存在该编号公群，切勿上当受骗。请联系客服核实 @kefu。")
                    else:
                        if group_by_num["bot_approve_link"] is not None:
                            await event.reply(group_by_num["bot_approve_link"])
                        else:
                            link = await tg.createBotApproveLink(group_by_num["chat_id"])
                            if link is None:
                                await event.reply("请稍后重试")
                            else:
                                await db.group_set_bot_link(group_by_num["id"], link)
                                await event.reply(link)
                else:
                    await event.reply("不存在该编号公群，切勿上当受骗。请联系客服核实 @kefu。")
        else:
            # if text_no_blank == "验群" or text_no_blank == "验证":
            #     await db.log_search_save(sender_id, text, text_original, 0)
            #     await event.reply(template.msg_private_yanzheng())
            #     return
            
            # if text_no_blank == "拉群" or text_no_blank == "担保" or text_no_blank == "hwdb":
            #     await db.log_search_save(sender_id, text, text_original, 0)
            #     await event.reply("拉群请联系客服 @hwdb")
            #     return

            await handle_search(bot, event, chat_id, sender_id, text_original, message)

    # text_no_blank = text.replace(" ", "")
    # text_no_blank = text.replace("公群", "")
    
    # if is_number(text_no_blank):
    #     num = to_num(text_no_blank)
        
    #     data = await db.reply_one(num)
    #     if data is not None:
    #         await event.reply(data["val"])
    #     else:
    #         if num < 90000:
    #             await event.reply("不存在该编号公群，切勿上当受骗。请联系客服核实 @kefu。")

    # if is_url(text_no_blank):
    #     group = await db.group_one_by_url(text_no_blank)
    #     if group is not None:
    #         if group["flag"] == 2 or group["flag"] == 4:
    #             await event.reply("这是真汇旺担保公群，可以放心交易。")
    #         elif group["flag"] == 3:
    #             await event.reply("这是骗子建立的假公群，切勿上当受骗，并联系汇旺担保官方举报。")
    # else:
    #     await event.respond("请发送公群链接")


async def handle_search(bot, event, chat_id, sender_id, text, message):
    text_original = text
    text_no_blank = text.replace(" ", "")
    
    search_reply_words = await db.search_reply_word_get()
    if search_reply_words is not None:
        for search_reply_word in search_reply_words:
            keyy = search_reply_word["keyy"]
            vall = search_reply_word["vall"]
            if keyy == text_no_blank:
                await db.log_search_save(sender_id, text, text_original, 1)
                await event.reply(vall)
                return
            
    
    names = await db.group_word_get()
    
    has_restrict_word = False
    for item in names:
        name = item["name"]
        
        if text.find(name) >= 0:
            has_restrict_word = True
        
        text = text.replace(name, "")
        
    text_temp = text.replace("gq", "")
    text_temp = replace_string_en(text_temp)
    text_temp_len = len(text.encode("utf-8"))
    
    
    if text_temp_len < 6:
        name_white = await db.group_word_white_one(text)
        if name_white is not None:
            text_temp_len = 9
        else:
            search_like_words = await db.search_like_word_get()
            for search_like_word in search_like_words:
                search_like_word = search_like_word["name"]
                
                search_like_word_arr = search_like_word.split(",")
                for search_like_word_text in search_like_word_arr:
                    if len(search_like_word_text) > 0 and search_like_word_text == text_no_blank:
                        text_temp_len = 9
                        break
                    
            
    if text_temp_len < 6:
        await db.log_search_save(sender_id, text, text_original, 0)
        
        if has_restrict_word:
            msg = await db.search_reply_word_one("无搜索结果")
            if msg is not None:
                msg = msg["vall"]
            else:
                msg = "该内容无搜索结果，请重新输入"
            await event.reply(msg)
            return
        else:
            msg = await db.search_reply_word_one("至少两个汉字")
            if msg is not None:
                msg = msg["vall"]
            else:
                msg = "搜索至少两个汉字，请重新输入"
            await event.reply(msg)
            return
    
    typee = 1
    groups = None
    groups_count = 0
    
    if text[0:2] == "qg":
        typee = 2
        text = text.replace("qg", "")
        groups = await db.groups_search_by_rules(text, 1)
        groups_count = await db.groups_search_count_by_rules(text)
        
        data_count = 0
        if groups_count is not None:
            groups_count = groups_count["count_num"]
            data_count = groups_count
        await db.log_search_save(sender_id, text, text_original, data_count)
        
    else:
        groups = await db.groups_search_by_title(text, 1)
        groups_count = await db.groups_search_count_by_title(text)
        data_count = 0
        if groups_count is not None:
            groups_count = groups_count["count_num"]
            data_count = groups_count
        
        if groups_count == 0:
            groups = []
        
        if groups_count < 10:
            page_len = 20 - groups_count
            groups_rule = await db.groups_search_by_rules_limit(text, page_len)
            if groups_rule is not None:
                for item in groups_rule:
                    groups.append(item)
            
            groups_count = len(groups)
            data_count = groups_count
                    
        await db.log_search_save(sender_id, text, text_original, data_count)
        
        
    if groups == None or len(groups) == 0:
        msg = await db.search_reply_word_one("无搜索结果")
        if msg is not None:
            msg = msg["vall"]
        else:
            msg = "该内容无搜索结果，请重新输入"
        await event.reply(msg)
        return
    else:
        is_province_or_ka = False
        
        if text_no_blank[0:2] == "qg":
            text_no_blank = text_no_blank.replace("qg", "")
        
        
        is_province = await db.word_province_one(text_no_blank)
        if is_province is not None:
            is_province_or_ka = True
        else:
            is_ka = await db.word_ka_one(text_no_blank)
            if is_ka is not None:
                is_province_or_ka = True
        
        
        await event.reply(message=template.msg_search_get(groups, 1, groups_count, 20, is_province_or_ka), buttons=template.button_search_get(text, 1, groups_count, typee), parse_mode="html", link_preview=False)
        
        # try:
        #     await event.reply(message=template.msg_search_get(groups, 1, groups_count), buttons=template.button_search_get(text, 1, groups_count, typee), parse_mode="html", link_preview=False)
        # except:
        #     print("reply error")
        
        
async def handle_forward(bot, event, chat_id, sender_id, text, message, fwd_from):
    is_user = True
    is_secret = None
    is_official = None
    is_cheat = None
    is_cheat_special = None
    admins = []
    if hasattr(fwd_from, "from_id"):
        from_id = fwd_from.from_id
        if hasattr(from_id, "user_id"):
            is_secret = from_id.user_id
            
            msg = await db_redis.forward_user_info_get(is_secret)
            if msg is not None and False:
                print("%s load redis" % is_secret)
                await event.reply(msg, parse_mode="html")
                return

            is_official = await db.official_one(from_id.user_id)
            
            is_cheat = await db.cheat_one_no_cache(is_secret)
            is_cheat_special = await db.cheat_special_one_no_cache(is_secret)
            admins = await db.group_admin_get_no_cache(is_secret)

        elif hasattr(from_id, "channel_id"):
            is_user = False
            is_secret = from_id.channel_id
            is_official = await db.official_one(from_id.channel_id)
            
    if is_user:
        if is_secret is not None:
            msg = "user_id: %s\n" % is_secret
            if is_official is not None:
                msg += "该用户为汇旺担保官方人员"
            else:
                if is_cheat_special is not None:
                    msg += "是否在骗子库：<b>是</b>\n"
                else:
                    msg += "是否在骗子库：否\n"
                    
                if is_cheat is not None:
                     msg += "是否在黑名单：<b>是</b>\n"
                else:
                    msg += "是否在黑名单：否\n"
                    
                admins_len = len(admins)
                if admins is not None and admins_len > 0:
                    if admins_len > 50:
                        msg += "是否为群管理：是"
                    else:
                        admin_groups = []
                        
                        for item in admins:
                            group = await db.group_one(item["group_tg_id"])
                            if group is not None:
                                admin_groups.append(group)
                            
                        msg += "是否为群管理："
                        if len(admin_groups) > 0:
                            for admin_group in admin_groups:
                                title = admin_group["title"]
                                
                                if "group_num" in admin_group:
                                    group_num = int(admin_group["group_num"])
                                    
                                    title = title.replace(" ", "")
                                    title = title.upper()
                                    
                                    if group_num > 0:
                                        if title.find("VIP公群") >= 0:
                                            msg += "VIP公群%s、" % group_num
                                        elif title.find("公群") >= 0:
                                            msg += "公群%s、" % group_num
                                        
                            if msg[(len(msg) - 1):] == "、":
                                msg += "(注意:本功能只为验证真假群之用,必须在公群内交易,私聊交易导致的纠纷不受理,后果自负。如有群管理诱导私聊交易，请联系 @hwdb 举报。)"
                        else:
                            msg += "是"
                else:
                     msg += "是否为群管理：否"
            
            await event.reply(msg, parse_mode="html")
            await db_redis.forward_user_info_set(is_secret, msg)
        else:
            msg = "对方设置了隐藏转发权限，无法获取id。"
            await event.reply(msg)
    else:
        if is_secret is not None:
            if is_official is None:
                await event.reply("channel_id: %s" % is_secret)
            else:
                await event.reply("channel_id: %s，是官方频道" % is_secret)
        else:
            await event.reply("该频道设置了隐藏转发权限，无法获取id。")