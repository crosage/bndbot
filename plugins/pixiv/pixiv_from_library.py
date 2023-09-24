import os,re
import random
from PIL import Image,ImageFilter
import nonebot
from PIL import Image
from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot import get_bots
from nonebot.adapters.onebot.v11 import Event
from nonebot.adapters.onebot.v11.message import MessageSegment
from ..management_module.management_db_operations import is_function_enabled
from nonebot.log import logger
import requests

lib_path=nonebot.get_driver().config.pixiv_lib_path
mylib=os.listdir(lib_path)
sz=len(mylib)


def deal_unable(path,filename):#图库地址和文件名
    """
    处理发送不能发送的图片，绕过腾讯检测
    """
    img=Image.open(path+filename)
    h=img.height
    w=img.width
    img=img.resize(size=(int(w*0.9),int(h*0.9)))
    img=img.rotate(180)
    logger.error(path+f"/tmp.png")
    img.save(path+f"/tmp.png")

def gaussian_blur(path,filename):
    """
    为图片添加高斯模糊
    """
    img=Image.open(path+filename)
    blurred_image=img.filter(ImageFilter.GaussianBlur(radius=10))
    blurred_image.save(path+f"\\blurred_image.png")


pixiv_from_lib=on_command("来张",aliases={"色图","涩图","laizhang","setu","lz"})
@pixiv_from_lib.handle()
async def work(event:Event,matcher:Matcher):

    bot,=get_bots().values()
    image_id=random.randint(0,sz-1)
    _,group,qq=str(event.get_session_id()).split("_")
    if is_function_enabled(group,"lz") is None:
        await pixiv_from_lib.finish(None)
    pattern=r"(\d+)_"
    match=re.search(pattern,mylib[image_id])
    # print(match.group(1))
    logger.error(mylib[image_id])
    pixiv_url = f'http://127.0.0.1:8000/api/image/{match.group(1)}'
    response = requests.get(pixiv_url)
    logger.warning(response.json())
    result=response.json()
    tags=result["tags"]
    try :
        if "R-18" in tags:
            gaussian_blur(lib_path+"\\",f"{mylib[image_id]}")
            await pixiv_from_lib.send(mylib[image_id]+"\n"+f"tags:{tags}")
            await pixiv_from_lib.send(MessageSegment.image("file:///"+lib_path+f"\\blurred_image.png"))
            logger.error("R-18 lz")
        else :
            await pixiv_from_lib.send(mylib[image_id]+"\n"+f"tags:{tags}")
            await pixiv_from_lib.send(MessageSegment.image("file:///"+lib_path+f"\\{mylib[image_id]}"))
            logger.error(f"{mylib[image_id]}")
    except :
        
        await pixiv_from_lib.send(MessageSegment.text(f"图片发送失败，可能因为被吞{mylib[image_id]}\n稍后可能发一张处理过的图"))
        gaussian_blur(lib_path+"\\",f"{mylib[image_id]}")
        # deal_unable(lib_path,f"/{mylib[image_id]}")
        await pixiv_from_lib.send(MessageSegment.image("file:///"+lib_path+f"\\blurred_image.png"))
