import os
import random
import nonebot
from PIL import Image
from loguru import logger
from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot import get_bots
from nonebot.adapters.onebot.v11 import Event
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11.message import Message
from nonebot.adapters.onebot.v11.message import MessageSegment
from ..management_module.management_db_operations import is_function_enabled


blue_vits=on_command("vits",aliases={"爱丽丝"})
@blue_vits.handle()
async def work(event:Event,matcher:Matcher,args:Message=CommandArg()):
    # bot,=get_bots().values()
    # _,group,qq=str(event.get_session_id()).split("_")
    # if isInGroup(group,"capoo")==0:
    #     await blue_vits.finish(None)
    text=str(args)
    path=os.path.abspath(os.path.dirname(__file__))
    print(path)
    os.system(f"python {path}\\vits-models\\cli.py --text '{text}'")
    print(f"python {path}\\vits-models\\cli.py --text '{text}'")
    print(f"{text}")
    await blue_vits.send(MessageSegment.record(f"file:///D:/bot/awesomebot/awesomebot/plugins/blue_archive/vits-models/output.wav"))
