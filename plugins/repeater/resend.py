from nonebot import on_message
from nonebot.adapters import Bot, Event
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.log import logger
from nonebot.params import CommandArg
import requests
from nonebot.typing import T_State

group_chat = on_message(priority=5)
downloadPath = "D:\\bot\\awesomebot\\awesomebot\\plugins\\assets\\imagetmp\\"


@group_chat.handle()
async def forward_to_another_group(bot: Bot, event: Event, state: T_State):
    # 获取要监听的目标群的群号
    target_group_id = '602683715'
    people = "3408476436"
    _, group, qq = str(event.get_session_id()).split("_")
    logger.warning(f"target_group_id:{target_group_id}    {event.get_user_id()} {event.get_session_id()}")
    logger.warning(f"{event.get_message()}  {event.get_type()}")
    if group == target_group_id and qq == people:
        if "image" in event.get_message():
            logger.warning("进入条件")
            target_group_id = '850921821'
            await bot.send_msg(group_id=target_group_id,
                           message=Message(event.get_message()))
    # else:
    #     # 如果不是图片消息，获取消息内容并发送到另一个群
    #     message = event.get_plaintext()
    #     target_group_id = '850921821'
    #     await bot.send_group_msg(group_id=target_group_id, message=message)
