import os
import json
from assist import download_media
import telethon.tl.types
import db_redis
import db
import tg
from config import media_path
from PIL import Image
import imagehash


async def is_same_image(image1_path, image2_path):
    flag = False
    
    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)
    
    hash1 = imagehash.average_hash(image1)
    hash2 = imagehash.average_hash(image2)
    
    if hash1 == hash2:
        print("%s %s same" % (image1_path, image2_path))
        flag = True
        
    return flag
    

async def download_image(bot, event, message, group_tg_id, user_tg_id, message_tg_id):
    message_date = message.date
    created_at_timestamp = int(message_date.timestamp())
    
    media = event.message.media
    if media is not None:
        if (isinstance(media, telethon.tl.types.MessageMediaPhoto) or isinstance(media, telethon.tl.types.MessageMediaDocument)):
            media_type = 1
            # 1文本2图片3表情包4音频5视频6文件
            if isinstance(media, telethon.tl.types.MessageMediaPhoto):
                media_type = 2
            elif isinstance(media, telethon.tl.types.MessageMediaDocument):
                mime_type = media.document.mime_type
                if mime_type.find("image") >= 0:
                    media_type = 2

            if media_type == 2:
                root_dir = os.path.dirname(os.path.abspath(__file__))
                path = root_dir + media_path

                image_path = await download_media(bot, event, group_tg_id, message_tg_id, path)
                
                await db.log_msg_path10_save(group_tg_id, user_tg_id, message_tg_id, image_path, created_at_timestamp)
                
                msg10_status = db_redis.msg_path10_status_get(group_tg_id, user_tg_id)
                if msg10_status:
                    msg_paths = await db.log_msg_path10_get4(group_tg_id, user_tg_id)
                    
                    print(msg_paths)
                    
                    if len(msg_paths) == 4:
                        flag = False
                        msg_path_0 = msg_paths[0]["info"]
                        msg_path_1 = msg_paths[1]["info"]
                        msg_path_2 = msg_paths[2]["info"]
                        msg_path_3 = msg_paths[3]["info"]
                        
                        if (await is_same_image(msg_path_0, msg_path_1)) and (await is_same_image(msg_path_0, msg_path_2)) and (await is_same_image(msg_path_0, msg_path_3)):
                            
                            
                            print("10分钟内发送的图片4次：%s" % msg_path_0)
                            
                            await tg.restrict(bot, group_tg_id, user_tg_id, -1, ("10分钟内发送的图片4次：%s" % msg_path_0))
                            
                            # db_redis.tgData_set({
                            #     "typee": "restrict",
                            #     "group_tg_id": group_tg_id,
                            #     "user_tg_id": user_tg_id,
                            #     "reason": "10分钟内发送的图片4次：%s" % msg_path_0,
                            # })
                        
                # 只要有信息就要重新录入，重制时间的
                db_redis.msg_path10_status_set(group_tg_id, user_tg_id)
                
                val = {
                    'group_tg_id': group_tg_id,
                    'user_tg_id': user_tg_id,
                    'message_tg_id': message_tg_id,
                    'image_path': image_path,
                    'root_dir': root_dir,
                    "created_at_timestamp": created_at_timestamp,
                }
                
                # await db_redis.adult_pic_set(val)
                