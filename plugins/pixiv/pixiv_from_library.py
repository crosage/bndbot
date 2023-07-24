import os
import random
import nonebot
from PIL import Image
from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot import get_bots
from nonebot.adapters.onebot.v11 import Event
from nonebot.adapters.onebot.v11.message import MessageSegment
from ..management_module.is_in_group import isInGroup
from nonebot.log import logger


lib_path=nonebot.get_driver().config.pixiv_lib_path
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



pixiv_from_lib=on_command("来张",aliases={"随机萌图","色图","涩图","不色图","laizhang","唻仧","lz","来点"})
@pixiv_from_lib.handle()
async def work(event:Event,matcher:Matcher):

    bot,=get_bots().values()
    image_id=random.randint(0,sz-1)
    _,group,qq=str(event.get_session_id()).split("_")
    if isInGroup(group,"pixiv_from_library")==0:
        await pixiv_from_lib.finish(None)
    try :
        await pixiv_from_lib.send(mylib[image_id])
        await pixiv_from_lib.send(MessageSegment.image("file:///"+lib_path+f"\\{mylib[image_id]}"))
        logger.error(f"{mylib[image_id]}")
    except :
        
        await pixiv_from_lib.send(MessageSegment.text(f"图片发送失败，可能因为被吞{mylib[image_id]}\n稍后可能发一张处理过的图"))
        deal_unable(lib_path,f"/{mylib[image_id]}")
        await pixiv_from_lib.send(MessageSegment.image("file:///"+lib_path+f"/tmp.png"))
