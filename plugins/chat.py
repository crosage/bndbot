from revChatGPT.V3 import Chatbot
import os
from PIL import Image
from nonebot.adapters.onebot.v11 import Bot
from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot import get_bots
from nonebot.adapters.onebot.v11 import Event
from nonebot.adapters.onebot.v11.message import MessageSegment
from .managementModule.isInGroup import isInGroup
from nonebot.log import logger
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11.message import Message

chat=on_command("c",aliases={"chat"})
@chat.handle()
async def work(event:Event,matcher:Matcher,args:Message=CommandArg()):
    text=str(args)
    chatbot=Chatbot(api_key="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",proxy="http://127.0.0.1:7890",engine="gpt-3.5-turbo")
    await chat.send(chatbot.ask(text))