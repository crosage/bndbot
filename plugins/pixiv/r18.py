import os
import random
import nonebot
from PIL import Image
from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import Event
from nonebot.adapters.onebot.v11.message import MessageSegment
from ..management_module.management_db_operations import is_function_enabled
from nonebot.log import logger

lib_path=nonebot.get_driver().config.r18_lib_path
mylib=os.listdir(lib_path)
sz=len(mylib)

def deal_unable(path,filename):#图库地址和文件名
    img=Image.open(path+filename)
    h=img.height
    w=img.width
    img=img.resize(size=(int(w*0.9),int(h*0.9)))
    img=img.rotate(180)
    logger.error(path+f"/tmp.png")
    img.save(path+f"/tmp.png")


pixiv_18_from_lib=on_command("18")
@pixiv_18_from_lib.handle()
async def work(event:Event,matcher:Matcher):
    image_id=random.randint(0,sz-1)
    _,group,qq=str(event.get_session_id()).split("_")
    if is_function_enabled(group, "18") is None:
        await pixiv_18_from_lib.finish(None)
    try :
        await pixiv_18_from_lib.send(mylib[image_id])
        await pixiv_18_from_lib.send(MessageSegment.image("file:///"+lib_path+f"/{mylib[image_id]}"))
    except :        
        await pixiv_18_from_lib.send(MessageSegment.text(f"图片发送失败，可能因为被吞{mylib[image_id]}\n稍后可能发一张处理过的图"))
        deal_unable(lib_path,f"/{mylib[image_id]}")
        await pixiv_18_from_lib.send(MessageSegment.image("file:///"+lib_path+f"/tmp.png"))
