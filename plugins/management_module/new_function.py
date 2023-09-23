import sqlite3
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot,Event
from nonebot.adapters import Message
from nonebot.matcher import Matcher #matcher 匹配器
from nonebot.params import Arg,CommandArg,ArgPlainText #param 参数，对参数的操作
from .management_db_operations import add_function,get_all_functions
from nonebot.log import logger

addNewFunction=on_command("add_new",aliases={"功能新增"},priority=10,block=True)
@addNewFunction.handle()
async def setGroup_handle(matcher:Matcher,event:Event,args:Message=CommandArg()):
    text=args.extract_plain_text()
    if text :
        matcher.set_arg("functions",args)

@addNewFunction.got("functions",prompt="你想添加什么功能？")#设置参数functions 用Message存储Message类型的functions 用str存储字符串类型的name
async def handle_functions(event:Event,functions:Message=Arg(),name: str = ArgPlainText("functions")):
    _,group,qq=str(event.get_session_id()).split("_")
    add_function(name)
    r=get_all_functions()
    result="现在有的功能有:\n"
    for item in r:
        logger.debug(item[1])
        result=result+f"{item[1]}\n"
    await addNewFunction.finish(result)

