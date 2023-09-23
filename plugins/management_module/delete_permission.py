from re import fullmatch
from pymysql import *
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot,Event
from nonebot.adapters import Message
from nonebot.matcher import Matcher #matcher 匹配器
from nonebot.params import Arg,CommandArg,ArgPlainText #param 参数，对参数的操作
from nonebot.log import logger
from .management_db_operations import is_function_enabled
from .management_db_operations import delete_permission


delFunctions=on_command("del",aliases={"删除"},priority=10,block=True)
@delFunctions.handle()
async def delFunctions_handle(matcher:Matcher,event:Event,args:Message=CommandArg()):
    text=args.extract_plain_text()
    _,group,qq=str(event.get_session_id()).split("_")
    if text :
        matcher.set_arg("functions",args)

@delFunctions.got("functions",prompt="你要删除哪个功能？")
async def handle_del(event:Event,functions:Message=Arg(),name: str = ArgPlainText("functions")):
    _,group,qq=str(event.get_session_id()).split("_")
    if is_function_enabled(group,name):
        delete_permission(group,name)
        await delFunctions.finish("删除成功")
    else :
        await delFunctions.finish("删除失败,该群好像没有这个功能")