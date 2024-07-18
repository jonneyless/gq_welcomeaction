import asyncio
import json
import os
import db
import tg
from assist import *
import db_redis
from nsfw_detector import predict
from celery_task import app

# 验证包路径
load_model_path = '/public/file/nsfw_mobilenet2.224x224.h5'
# 图片校验删除边界值
image_boundary_val = 0.5


@app.task
def image_filter(params):
    params = json.loads(params)

    loop = asyncio.get_event_loop()

    loop.run_until_complete(media_image_filter(params['chat_id'], params['user_tg_id'], params['message_tg_id'], params['image_path'], params['root_dir']))


# 图片校验逻辑
async def media_image_filter(chat_id, user_tg_id, message_tg_id, image_path, root_dir):
    path = root_dir + load_model_path
    print('media_image_filter path', path)
    # 获取内容
    model = predict.load_model(path)
    # 匹配校验
    result = predict.classify(model, image_path)

    # 删除系统上图片文件
    if os.path.exists(image_path):
        os.remove(image_path)

    if result is not None:

        for val in result.values():

            # hentai 卡通  porn 色情  sexy 性感  > 50% 定义为色情
            if (
                    val['hentai'] >= image_boundary_val
                    or val['porn'] >= image_boundary_val
                    or val['sexy'] >= image_boundary_val):
                # 删除用户消息
                await tg.api_delete_messages(chat_id, message_tg_id)
                # 记录删除日志
                await db.log_delete_save(chat_id, user_tg_id, message_tg_id, '检测到色情图片删除')

                # 用户缓存禁言操作
                key = 'media_image_filter_' + str(chat_id) + '_' + str(user_tg_id)
                # 记录违规+1
                num = await db_redis.incrby(key)

                if num is not None and int(num) >= 3:  # 用户5分钟内发送三个及以上数量的色图，则禁言该用户一天
                    # 删除redis缓存
                    await db_redis.delete(key)
                    # 禁言时间
                    data_time = int(time.time()) + 86400
                    # 请求tg禁言用户
                    await tg.api_ban_chat_user(chat_id, user_tg_id, data_time)
                    # 写入日志
                    await db.log_restrict_save(chat_id, user_tg_id, data_time, '发送黄色图片')
                    # 更新用户表用户权限
                    await db.user_group_restrict(chat_id, user_tg_id)
                return True

    return False
