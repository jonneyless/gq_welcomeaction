import time

from telethon import Button

import db_redis
from assist import has_prev, has_next, get_max_page


def no_search():
    msg = """该内容无搜索结果，请重新输入！ 
请关注 @hwgq 从这个频道可以进入所有汇旺担保公群！
你也可以试试超级搜索 @chaoji 。"""

    return msg
    

def msg_private_yanzheng():
    msg = """1、 验证公群请发群编号（群编号是公群两个字后面带的数字序号，如果公群123，123就是群编号），机器人会自动发送群链接，看看和自己所在的是不是同一个群可以自助验群；
2、验证专群给 @he444bot 这个机器人发专群群编号(专群群编号为一个字母加5个数字)，看和交易员的共同群验群；
3、如果不会自助验群，请联系客服 @hwdb 进行人工验群。
"""

    return msg


def msg_notice_group_true(group_admins, title):
    msg = "汇旺担保官方人员 "

    for index in range(len(group_admins)):
        group_admin = group_admins[index]

        msg += "%s " % group_admin["username"]

    msg += "在本群，本群是真群。"
    # msg += "在本群，本群《%s》是真群。" % title
    
    # msg = """有本机器人在群，此群是真群！请注意看我的用户名是 @qunguan (群管拼音)，谨防假机器人。私聊我输入词语可以搜索真公群,如：卡商、白资、承兑等。请找有头衔的人在群内交易，切勿相信主动私聊你的，都是骗子。非群内交易没有任何保障。客服频道 @kefu 汇旺公群 @hwgq"""

    return msg


def msg_notice_group_false():
    return "本群少于两个官方人员疑似假群，请通过公群导航 @hwgq 核对。"


def msg_check_group_true():
    return "这是真汇旺担保公群，可以放心交易。"


def msg_check_group_false():
    return "这是骗子建立的假公群，切勿上当受骗，并联系汇旺担保官方举报。"


def msg_group_set_welcome_info(title, info):
    return "欢迎语设置成功，当前欢迎语是：欢迎***加入 %s %s" % (title, info)


def msg_group_show_welcome_info(title, info):
    if info is None:
        info = ""
    
    return "当前欢迎语是：欢迎***加入 %s %s" % (title, info)


def msg_group_close_welcome_info():
    return "欢迎语已关闭"


def msg_send_cheat_bank(userr, cheat_bank):
    return "%s使用骗子银行卡账号%s" % (userr["fullname"], cheat_bank)


def msg_send_cheat_coin(userr, cheat_coin):
    return "%s使用骗子虚拟币地址%s" % (userr["fullname"], cheat_coin)


def msg_send_has_huiwang(userr):
    return "%s疑似冒充汇旺官方人员，已自动将其踢出群组" % userr["fullname"]


def msg_send_has_special_text():
    return "xxx并非群管理，所发地址/账号无效，请提高警惕，小心被骗。"
    
    
def msg_start_text():
    # text = "您好，这里是汇旺公群机器人\n"
    # text += "公群导航 @hwgq 避免进假群\n"
    # text += "公群流程 @gongqunLC 了解公群交易注意事项\n"
    # text += "客服频道 @kefu 可以快速分辨工作人员\n"
    # text += "另外可以私聊我发送公群编号直接获取进群方式，请输入精确的公群编号，例如【123】\n"
    
    text = """您好，这里是汇旺公群机器人
公群导航 @hwgq 避免进假群
公群流程 @gongqunLC 了解公群交易注意事项
客服频道 @kefu 可以快速分辨工作人员
另外可以私聊我发送公群编号直接获取进群方式，例如【123】；也可以输入词语进行搜索，如 卡商、代收、白资"""
    
    return text


def msg_group_close():
    text = "本公群今日已下课，\n"
    text += "如需交易，请在该群恢复营业后在群内交易！ 切勿私下交易！！！\n"
    text += "如有业务咨询请联系群老板/业务员\n"
    text += "如有纠纷请联系纠纷专员 @hwdb\n"
    
    return text
    
    
def msg_group_open():
    return "群已开，群内可以正常营业"
    
    
def msg_group_error():
    return "当前公群处于暂停交易状态，擅自交易后果自负，请群老板或业务员处理完相关事务后再重新开群"
    
    
def msg_night_close_msg():
    return "尊敬的客户您好，当前时间已暂停受理业务，请在金边时间 8:00～2:00 与工作人员联系"
    
    
def msg_first_notice():
    return "私下交易没有安全保障，出现纠纷平台概不负责，所有交易请在公群内进行，并及时入账，切勿私下交易！"
    
    
def msg_boss_pwd():
    msg = "请输入8-18位的密码，密码只能由字母和数字组成，字母区分大小写，放弃请点击【取消】\n"
    msg += "注：密码仅对本账号有效，一经设置无法修改，请牢记您的密码，任何担保工作人员不会主动向您索要密码，此密码仅作为找回身份使用，谨防泄漏"
    
    return msg


def msg_ss():
    return "请通过输入群编号或关键词搜索对应公群"


def msg_cx():
    return "请输入您要查询人员的tgid，或转发此人的发言记录给我"


def msg_ad():
    return "请联系客服 @hwdb 点击【买广告】按钮办理相关业务"


def msg_mb():
    return "已切换至密码功能模式"
    
    
def button_sure_boss_pwd(pwd):
    sure_data = "sure_boss_pwd?pwd=%s" % pwd
    
    return [
        [
            Button.inline(text="确定", data=sure_data),
            Button.inline(text="取消", data="cancel_boss_pwd"),
        ],
    ]


def button_cancel_boss_pwd():
    return [
        [
            Button.inline(text="取消", data="cancel_boss_pwd"),
        ],
    ]


def button_ss_hot_words():
    buttons = []
    rows = []

    words = db_redis.getHotWords()
    for index in words:
        word = words[index]
        buttons.append(Button.inline(text=word, data="search?text=" + word + "&page=1&typee=1"))
        if index % 5 == 4:
            rows.append(buttons)
            buttons = []

    if len(buttons) > 0:
        rows.append(buttons)

    return rows


def button_service():
    return [
        [
            Button.url(text="联系客服 @hwdb", url="https://t.me/hwdb"),
        ],
    ]


async def ads_top_position(keyword):
    data = await db_redis.getTodayAdsData(1)

    msg = ""
    for index in data:
        datum = data[index]
        if keyword in datum['keywords']:
            msg += "<a href=\"%s\">%s</a>\n" % (datum['url'], datum['name'])

    if msg != "":
        msg += "\n"

    return msg


async def ads_bottom_position(buttons: list, keyword):
    data = await db_redis.getTodayAdsData(2)

    for index in data:
        datum = data[index]
        if keyword in datum['keywords']:
            buttons.append([Button.url(text=datum['name'], url=datum['url'])])

    return buttons


async def get_group_info(group, link):
    msg = ""

    if "flag" in group and group["flag"] == 4:
        if "title" in group:
            msg += group['title'] + "\n\n"
    else:
        if "opening_at" in group and group['opening_at'] is not None:
            msg += "开群日期：" + time.strftime("%Y.%m.%d", time.strptime(str(group['opening_at']), "%Y-%m-%d %H:%M:%S")) + "\n"

        business = await db_redis.getGroupBusiness(group['business_type'])
        if business is not None:
            msg += "业务类型：" + business + "\n"

        manages = await db_redis.getGroupMangers(group['chat_id'])
        if manages['boss'] is not None:
            msg += "当前群老板： @" + manages['boss']['username'] + "\n"

        if manages['trader'] is not None:
            msg += "群内交易员： @" + manages['trader']['username'] + "\n"

        recent_dispute = 0
        if "recent_dispute" in group and group["recent_dispute"] is not None:
            recent_dispute = group["recent_dispute"]

        msg += "近期群内纠纷数：" + str(recent_dispute) + "\n"

    msg += link

    return msg


async def get_vip_group_info(group, notice):
    msg = ""

    if "title" in group:
        msg += group['title'] + "\n\n"

    msg += await get_group_info(group, notice)

    return msg

def msg_search_get(groups, page, count, page_len=20, is_province_or_ka=False):
    max_page = get_max_page(count, page_len)
    
    msg = ""
    if is_province_or_ka:
        msg = "<b>按地区查找卡商公群 @dunka\n</b>"
        msg += "\n"
        
    for key in range(len(groups)):
        group = groups[key]
        title = group["title"]
        link = group["link"]
        open_status = int(group["open_status"])
        flag = int(group["flag"])
        
        title = title.replace("\n", "")
        title = title.replace("\r", "")
        title = title.replace("\u2028", "")
        
        link = link.replace("\n", "")
        link = link.replace("\r", "")
        link = link.replace("\u2028", "")

        msg += "%s. " % (page_len * (page - 1) + key + 1)
        
        if title.find("VIP公群") >= 0 or title.find("vip公群") >= 0:
            link = link.replace(" ", "")
            link = link.replace(",", "")
            link = link.replace("，", "")
            link = link.replace(":", "")
            link = link.replace("：", "")
            link = link.replace("群老板", "")
            link = link.replace("业务员", "")
            link = link.replace("该群为vip公群暂不公布链接请联系", "")
            link = link.replace("进群进群后请联系官方人员验证@kefu", "")
            boss_username = link.replace("@", "")
            
            if open_status == 1:
                pass
            else:
                if flag == 2:
                    title = "(已下课)%s" % title
                else:
                    title = title
            
            msg += '%s 群老板：@%s' % (title, boss_username)
        else:
            if open_status == 1:
                msg += '<a href="%s">%s</a>' % (link, title)
            else:
                if flag == 2:
                    msg += '(已下课)<a href="%s">%s</a>' % (link, title)
                else:
                    msg += '<a href="%s">%s</a>' % (link, title)
            
        msg += "\n"
        
    msg += "\n"
    
    if msg.find("VIP公群") >= 0 or msg.find("vip公群") >= 0:
        msg += "提示：vip公群进群后请联系官方客服 @hwdb 自助验群后再交易,如因客户不验群产生的一切后果自负。\n"
        msg += "\n"
    
    if is_province_or_ka:
        msg += "<b>提示：可以通过搜索地区查找对应地区的卡商公群，如：“重庆” “天津”</b>\n"
        msg += "\n"
    
    msg += "客服频道 @kefu 供求频道 @gongqiu\n"
    msg += "📢查看今天新开公群 @xinqun\n"
    msg += "第 %s 页，共 %s 页" % (page, max_page)
    
    return msg


def button_search_get(text, page, count, type, sort=None, page_len=20):
    max_page = get_max_page(count, page_len)

    sortfield = sort
    sortMode = ""
    sortReversal = '-'

    if sort is not None:
        sortMode = "⬆️"
        if sort[0:1] == '-':
            sortfield = sort[1:len(sort)]
            sortMode = "⬇️"
            sortReversal = ''
    else:
        sort = ""

    sortFieldMaps = {
        'yajin': '押金金额',
        'opening_at': '开群日期',
        'trade_volume': '交易量',
        'recent_dispute': '近期纠纷'
    }
    
    buttons = []

    buttons_row = []
    for field in sortFieldMaps:
        buttonText = sortFieldMaps[field]
        if sortfield == field:
            buttonText += sortMode
        buttons_row.append(Button.inline(text=buttonText, data="search?k=%s&p=%s&t=%s&s=%s" % (text, 1, type, sortReversal + field)))
    buttons.append(buttons_row)

    buttons_row_page_one = []
    buttons_row_page_two = []
    
    if page != 1:
        buttons_row_page_one.append(Button.inline(text="首页", data="search?k=%s&p=%s&t=%s&s=%s" % (text, 1, type, sort)))
    
    if page - 2 > 0:
        # 3 4 5...
        
        # 当前第三页
        # 首页 1, 2, (3)
        
        # 当前第四页
        # 首页 ... 2, 3, (4)
        
        # 当前第五页
        # 首页 ... 3, 4, (5)
        
        if page == 3:
            page1 = str(page - 2)
            page2 = str(page - 1)
            buttons_row_page_one.append(Button.inline(text=page1, data="search?k=%s&p=%s&t=%s&s=%s" % (text, (page - 2), type, sort)))
            buttons_row_page_one.append(Button.inline(text=page2, data="search?k=%s&p=%s&t=%s&s=%s" % (text, (page - 1), type, sort)))
        else:
            page1 = "..."
            page2 = str(page - 2)
            page3 = str(page - 1)
            buttons_row_page_one.append(Button.inline(text=page1, data="search?k=%s&p=%s&t=%s&s=%s" % (text, (page - 3), type, sort)))
            buttons_row_page_one.append(Button.inline(text=page2, data="search?k=%s&p=%s&t=%s&s=%s" % (text, (page - 2), type, sort)))
            buttons_row_page_one.append(Button.inline(text=page3, data="search?k=%s&p=%s&t=%s&s=%s" % (text, (page - 1), type, sort)))
    else:
        # 1 2
        if page == 2:
            buttons_row_page_one.append(Button.inline(text="1", data="search?k=%s&p=%s&t=%s&s=%s" % (text, 1, type, sort)))

    if max_page > 1:
        page_current = "(%s)" % page
        buttons_row_page_one.append(Button.inline(text=page_current, data="search?k=%s&p=%s&t=%s&s=%s" % (text, page, type, sort)))

    show_last_page = page
    for i in range(7):
        i = i + 1
        if page + i <= max_page:
            pagei = str(page + i)
            
            show_last_page = int(pagei)
            
            if len(buttons_row_page_one) < 8:
                buttons_row_page_one.append(Button.inline(text=pagei, data="search?k=%s&p=%s&t=%s&s=%s" % (text, pagei, type, sort)))
            else:
                buttons_row_page_two.append(Button.inline(text=pagei, data="search?k=%s&p=%s&t=%s&s=%s" % (text, pagei, type, sort)))
    
    if show_last_page < max_page:
        # 最大页 10
        # 8, ..., 尾页
        if len(buttons_row_page_one) < 8:
            buttons_row_page_one.append(Button.inline(text="...", data="search?k=%s&p=%s&t=%s&s=%s" % (text, (show_last_page + 1), type, sort)))
        else:
            buttons_row_page_two.append(Button.inline(text="...", data="search?k=%s&p=%s&t=%s&s=%s" % (text, (show_last_page + 1), type, sort)))

    if page != max_page:
        if len(buttons_row_page_one) < 8:
            buttons_row_page_one.append(Button.inline(text="尾页", data="search?k=%s&p=%s&t=%s&s=%s" % (text, max_page, type, sort)))
        else:
            buttons_row_page_two.append(Button.inline(text="尾页", data="search?k=%s&p=%s&t=%s&s=%s" % (text, max_page, type, sort)))

    if len(buttons_row_page_one) > 0:
        buttons.append(buttons_row_page_one)
        
    if len(buttons_row_page_two):
        buttons.append(buttons_row_page_two)

    buttons_row = []
    if has_prev(page):
        buttons_row.append(Button.inline(text="上一页⬅️", data="search?k=%s&p=%s&t=%s&s=%s" % (text, (page - 1), type, sort)))
    if has_next(page, count, page_len):
        buttons_row.append(Button.inline(text="下一页➡️️", data="search?k=%s&p=%s&t=%s&s=%s" % (text, (page + 1), type, sort)))
        
    if len(buttons_row) > 0:
        buttons.append(buttons_row)
        
    if len(buttons) > 0:
        return buttons
    else:
        return None