import os
from loguru import logger
from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot import get_bots
from nonebot.adapters.onebot.v11 import Event
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.adapters.onebot.v11.message import Message
from nonebot.adapters.onebot.v11.message import MessageSegment
from ..management_module.management_db_operations import is_function_enabled

dict = {
    "爱丽丝": "alice",
    "未花": "mika",
    "伊吕波": "iroha",
    "美游": "miyu",
    "梓": "azusa",
    "小梓": "azusa",
    "小桃": "momoi",
    "优香": "yuuka",
    "hina": "hina",
    "白子": "shiroko",
    "日奈": "hina",
    "星野": "hoshino",
    "伊织": "iori",
    "小狐狸": "izuna",
    "花凛": "karin"
}


def get_vits_have():
    result = "目前已经支持的有:\n"
    for key in dict.keys():
        result = result + key + "\n"
    return result


blue_vits = on_command("tts")


@blue_vits.handle()
async def work(event: Event, matcher: Matcher, args: Message = CommandArg()):
    _, group, qq = str(event.get_session_id()).split("_")
    text = args.extract_plain_text()
    # if is_function_enabled(group,"blue_vits") is None:
    #     await blue_vits.finish(None)
    logger.warning(text)
    if text:
        matcher.set_arg("vits_model", args)


@blue_vits.got("vits_model", prompt=get_vits_have())
async def del_model_choose(args: str = ArgPlainText("vits_model")):
    arg = str(args).split(" ",2)
    # logger.warning(test)
    logger.warning(arg)
    if len(arg) == 2:
        model, text = str(args).split(" ",1)
        model = dict[f"{model}"]
        logger.warning(f"{model} {text}")
        path = os.path.abspath(os.path.dirname(__file__))
        print(path)
        os.system(f"python {path}\\vits-models\\cli.py --text '{text}' --model_choose {model}")
        print(f"python {path}\\vits-models\\cli.py --text '{text}' --model_choose '{model}'")
        print(f"{text}")
        await blue_vits.send(
            MessageSegment.record(f"file:///D:/bot/awesomebot/awesomebot/plugins/blue_archive/vits-models/output.wav"))
    else:
        r, model, text = str(args).split(" ",2)
        model = dict[f"{model}"]
        logger.warning(f"{model} {text}")
        path = os.path.abspath(os.path.dirname(__file__))
        print(path)
        os.system(f"python {path}\\vits-models\\cli.py --text \"{text}\" --model_choose {model} --language 1")
        print(f"python {path}\\vits-models\\cli.py --text \"{text}\" --model_choose '{model}' --language 1")
        print(f"{text}")
        await blue_vits.send(
            MessageSegment.record(f"file:///D:/bot/awesomebot/awesomebot/plugins/blue_archive/vits-models/output.wav"))
