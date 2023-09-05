import os
import random
import nonebot
from nonebot import on_regex
from nonebot.matcher import Matcher
from nonebot import get_bots
from nonebot.adapters.onebot.v11 import Event
from nonebot.params import CommandArg,RegexDict
from nonebot.adapters.onebot.v11.message import Message
from nonebot.adapters.onebot.v11.message import MessageSegment
from ..management_module.is_in_group import isInGroup

reply=on_regex(rf"cesh1",)
@reply.handle()
async def keyword_response(msg:dict=RegexDict()):
    print(msg)