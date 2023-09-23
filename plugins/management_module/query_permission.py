from pymysql import *
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import Bot,Event
from nonebot.matcher import Matcher
from PIL import Image,ImageDraw,ImageFont
#获取参数 对参数操作
from nonebot.params import Arg,CommandArg,ArgPlainText
from nonebot.adapters.onebot.v11.message import MessageSegment
from .create_database import db_file
from PIL import ImageDraw
import os

queryGroup=on_command("功能",aliases={"功能查询"},priority=20)
@queryGroup.handle()
async def queryGroup_handle(matcher:Matcher,state:T_State,event:Event,width:int=1024):

    await queryGroup.send(MessageSegment.image())