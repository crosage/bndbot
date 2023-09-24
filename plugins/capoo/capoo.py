import os
import random
import nonebot
from PIL import Image
from loguru import logger
from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot import get_bots
from nonebot.adapters.onebot.v11 import Event
from nonebot.adapters.onebot.v11.message import MessageSegment
from ..management_module.management_db_operations import is_function_enabled

capoo_path=nonebot.get_driver().config.capoo_path
mylib=os.listdir(capoo_path)
sz=len(mylib)

capoo=on_command("猫猫虫",aliases={"蓝皮猪","capoo"})
@capoo.handle()
async def work(event:Event,matcher:Matcher):
    bot,=get_bots().values()
    image_id=random.randint(0,sz-1)
    _,group,qq=str(event.get_session_id()).split("_")
    if is_function_enabled(group, "capoo") is None:
        await capoo.finish(None)
    logger.info(f"file:///"+capoo_path+f"\{mylib[image_id]}")
    await capoo.send(MessageSegment.image("file:///"+capoo_path+f"\{mylib[image_id]}"))
