import sqlite3
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot,Event
from nonebot.adapters import Message
from nonebot.matcher import Matcher #matcher 匹配器
from nonebot.params import Arg,CommandArg,ArgPlainText #param 参数，对参数的操作
from .management_db_operations import is_function_exist,add_permission
from nonebot.log import  logger

setGroup=on_command("add",aliases={"添加"},priority=10,block=True)
@setGroup.handle()
async def setGroup_handle(matcher:Matcher,event:Event,args:Message=CommandArg()):
    text=args.extract_plain_text()
    if text :
        matcher.set_arg("functions",args)

@setGroup.got("functions",prompt="你想添加什么功能？")
async def handle_functions(event:Event,functions:Message=Arg(),name: str = ArgPlainText("functions")):
    _,group,qq=str(event.get_session_id()).split("_")
    logger.debug(f"in set_functions:{is_function_exist(name)}")
    add_permission(group,name)

