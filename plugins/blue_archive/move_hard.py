import os
from loguru import logger
from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import Event
from nonebot.params import Arg,CommandArg,ArgPlainText
from nonebot.adapters.onebot.v11.message import Message
from nonebot.adapters.onebot.v11.message import MessageSegment
from ..management_module.management_db_operations import is_function_enabled

move_hard=on_command("困难关卡查询", aliases={"困难查询","move_hard"})
@move_hard.handle()
async def work(event:Event,matcher:Matcher,args:Message=CommandArg()):
    _,group,qq=str(event.get_session_id()).split("_")
    text=args.extract_plain_text()
    logger.warning(text)
    if text :
        matcher.set_arg("level",args)

@move_hard.got("level", prompt="你要查询的困难关卡？")
async def del_model_choose(level: str = ArgPlainText("level")):
    path=os.path.abspath(os.path.dirname(__file__))
    levels=os.listdir(path+"\\move_hard")
    logger.warning(levels)
    if level+".png" in levels:
        await  move_hard.finish(MessageSegment.image("file:///"+path+f"\\move_hard\\{level}.png"))