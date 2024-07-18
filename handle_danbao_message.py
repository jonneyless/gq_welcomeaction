import telethon.tl.types
import asyncio

import db
from helpp import respond_and_delete, has_yuefei, remove_not_official_admin, yuefei_sava_all
from assist import get_danbao_opened_day


async def index(bot, event, message, group, userr, group_tg_id, user_tg_id, text, reply_tg_id):
    if text == "担保开启":
        is_official = await db.official_one(user_tg_id)
        if is_official is not None:
            log_danbao = await db.danbao_one(group_tg_id)
            if log_danbao is not None:
                await respond_and_delete(bot, event, group_tg_id, "开启中")
                return
            
            admins = await db.group_admin_get_now(group_tg_id)
            await db.danbao_save(group, admins)
                
            await respond_and_delete(bot, event, group_tg_id, "担保开启成功")
            
            return
    
    if text == "担保刷新":
        is_official = await db.official_one(user_tg_id)
        if is_official is not None:
            log_danbao = await db.danbao_one(group_tg_id)
            if log_danbao is None:
                await respond_and_delete(bot, event, group_tg_id, "担保未开启")
                return
            
            admins = await db.group_admin_get_now(group_tg_id)

            await db.danbao_update(log_danbao, group, admins)
            
            await respond_and_delete(bot, event, group_tg_id, "担保刷新成功")

            return

    if text == "担保关闭":
        is_official = await db.official_one(user_tg_id)
        if is_official is not None:
            log_danbao = await db.danbao_one(group_tg_id)
            if log_danbao is None:
                await respond_and_delete(bot, event, group_tg_id, "担保未开启")
                return
            
            msg = ""
            opened_day = get_danbao_opened_day(log_danbao["created_at"])
            if opened_day > 30:
                flag, text_arr = await has_yuefei(log_danbao)
                if not flag:
                    msg = "开群时间：%s\n" % log_danbao["created_at"]
                    msg += "以下月费还未收取\n"
                    for text_item in text_arr:
                        msg += text_item
                        msg += "\n"
                    await respond_and_delete(bot, event, group_tg_id, msg, 5)
                    return
                
                yuefei = log_danbao["yuefei"]
                if yuefei is None:
                    await respond_and_delete(bot, event, group_tg_id, "还未设置月费")
                    return
                if float(yuefei) <= 0:
                    await respond_and_delete(bot, event, group_tg_id, "月费必须大于0")
                    return
                
                yuefei_day = log_danbao["yuefei_day"]
                if yuefei_day is None:
                    await respond_and_delete(bot, event, group_tg_id, "还未设置月费收取日")
                    return
                if int(yuefei_day) < 1 or int(yuefei_day) > 31:
                    await respond_and_delete(bot, event, group_tg_id, "月费收取日必须大于0小于等于31")
                    return
            else:
                msg = "公群开启不到一个月，不收取月费\n"
        
            title_after = "公群%s 已退押" % group["group_num"]
            changeTitleFlag = await tg.setChatTitle(group_tg_id, title_after)
            if not changeTitleFlag:
                await respond_and_delete(bot, event, group_tg_id, "群名更改失败，请重试", 5)
                return
            await db.group_init(group["id"], title_after)
            
            await db.danbao_over(log_danbao["id"])
            
            unpinAllFlag = await tg.unpinAllChatMessages(group_tg_id)
            descEmptyFlag = await tg.setChatDescriptionEmpty(group_tg_id)
            remove_not_official_admin_msg = await remove_not_official_admin(bot, group_tg_id)
            
            if unpinAllFlag:
                msg += "所有置顶已成功下掉\n"
            else:
                msg += "所有置顶下掉失败，请重试\n"
            if descEmptyFlag:
                msg += "群简介删除成功\n"
            else:
                msg += "群简介删除失败\n"
            msg += "\n"
            msg += remove_not_official_admin_msg
            
            await respond_and_delete(bot, event, group_tg_id, msg, 5)
                
            
    if text.find("改月费") == 0:
        text_temp = text.lower()
        text_temp = text_temp.replace("改月费", "")
        if is_number(text_temp) and float(text_temp) > 0:
            is_official = await db.official_one(user_tg_id)
            if is_official is not None:
                log_danbao = await db.danbao_one(group_tg_id)
                if log_danbao is None:
                    await respond_and_delete(bot, event, group_tg_id, "担保未开启")
                    return
                
                await db.danbao_update_yuefei(log_danbao["id"], text_temp)
                
                await respond_and_delete(bot, event, group_tg_id, "月费修改成功")
                return
                
                
    if text == "月费已全部收取":
        is_official = await db.official_one(user_tg_id)
        if is_official is not None:
            log_danbao = await db.danbao_one(group_tg_id)
            if log_danbao is None:
                await respond_and_delete(bot, event, group_tg_id, "担保未开启")
                return
            yuefei = log_danbao["yuefei"]
            if yuefei is None:
                await respond_and_delete(bot, event, group_tg_id, "还未设置月费")
                return
            if float(yuefei) <= 0:
                await respond_and_delete(bot, event, group_tg_id, "月费必须大于0")
                return
            
            await yuefei_sava_all(group, log_danbao, message_tg_id, userr)
            await respond_and_delete(bot, event, group_tg_id, "月费全部已收取")
            
            return
            
            
    if text == "月费全部不收取":
        is_official = await db.official_one(user_tg_id)
        if is_official is not None:
            log_danbao = await db.danbao_one(group_tg_id)
            if log_danbao is None:
                await respond_and_delete(bot, event, group_tg_id, "担保未开启")
                return
            yuefei = log_danbao["yuefei"]
            if yuefei is None:
                await respond_and_delete(bot, event, group_tg_id, "还未设置月费")
                return
            if float(yuefei) <= 0:
                await respond_and_delete(bot, event, group_tg_id, "月费必须大于0")
                return
            
            await yuefei_sava_all(group, log_danbao, message_tg_id, userr, 2)
            await respond_and_delete(bot, event, group_tg_id, "月费全部已收取")
            
            return
    
    if text == "月费已收取":
        is_official = await db.official_one(user_tg_id)
        if is_official is not None:
            log_danbao = await db.danbao_one(group_tg_id)
            if log_danbao is None:
                await respond_and_delete(bot, event, group_tg_id, "担保未开启")
                return
            yuefei = log_danbao["yuefei"]
            if yuefei is None:
                await respond_and_delete(bot, event, group_tg_id, "还未设置月费")
                return
            if float(yuefei) <= 0:
                await respond_and_delete(bot, event, group_tg_id, "月费必须大于0")
                return
             
            await db.danbao_yuefei_save(group, log_danbao, message_tg_id, userr, None)
            await respond_and_delete(bot, event, group_tg_id, "月费已收取")
            
            return
    
    if text == "月费不收取":
        is_official = await db.official_one(user_tg_id)
        if is_official is not None:
            log_danbao = await db.danbao_one(group_tg_id)
            if log_danbao is None:
                await respond_and_delete(bot, event, group_tg_id, "担保未开启")
                return
            yuefei = log_danbao["yuefei"]
            if yuefei is None:
                await respond_and_delete(bot, event, group_tg_id, "还未设置月费")
                return
            if float(yuefei) <= 0:
                await respond_and_delete(bot, event, group_tg_id, "月费必须大于0")
                return
             
            await db.danbao_yuefei_save_no(group, log_danbao, message_tg_id, userr, None)
            await respond_and_delete(bot, event, group_tg_id, "当月月费已设置不收取")
            
            return