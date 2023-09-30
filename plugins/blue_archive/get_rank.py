from playwright.async_api import async_playwright
from nonebot import on_command
import requests
import datetime
import os
from loguru import logger
from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import Event
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.adapters.onebot.v11.message import Message, MessageSegment

path = os.path.abspath(os.path.dirname(__file__))
async def get_screenshot(season):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(f"http://ba.gamerhub.cn/#/raid-rank-data/s{season}")
        await page.wait_for_timeout(3000)
        page_height = await page.evaluate('(document.body.scrollHeight)')
        await page.set_viewport_size({"width": 1280, "height": page_height})
        logger.error(path+"screenshot.png")
        await page.screenshot(path=path+"\\screenshot.png")
        await browser.close()


def get_values(season):
    url = f"http://ba.gamerhub.cn/api/get_ba_raid_ranking_data?season={season}"
    resp = requests.get(url)
    json_data = resp.json()
    data = json_data["data"]
    data_bilibili=json_data["data_bilibili"]
    g = {}  # 官服
    b = {}  # b服
    # print(data)
    for ranking, time in data.items():
        dt = datetime.datetime.fromtimestamp(time[-2][0] / 1000)
        formatted_date = dt.strftime('%Y-%m-%d %H:%M:%S')
        # print(formatted_date)
        g.update({f"{ranking}": {
            "time": formatted_date,
            "score": time[-2][1]
        }})
    for ranking, time in data_bilibili.items():
        dt = datetime.datetime.fromtimestamp(time[-2][0] / 1000)
        formatted_date = dt.strftime('%Y-%m-%d %H:%M:%S')
        # print(formatted_date)
        b.update({f"{ranking}": {
            "time": formatted_date,
            "score": time[-2][1]
        }})
    # print(g)
    return g, b
    # logger.warning(data["1"])


get_rank = on_command("榜单查询")


@get_rank.handle()
async def get_ranking(event: Event, matcher: Matcher, args: Message = CommandArg()):
    await get_screenshot(4)
    g, b = get_values(4)
    str_g = "官服总力战数据"
    str_b = "b服总力战数据"
    for ranking, result in g.items():
        if str_g == "官服总力战数据":
            str_g = str_g + f"(更新时间:{result['time']})\n"
        str_g = str_g + f"{ranking}: " + f"分数{result['score']}\n"
    await get_rank.send(str_g)
    for ranking, result in b.items():
        if str_b == "b服总力战数据":
            str_b = str_b + f"(更新时间:{result['time']})\n"
        str_b = str_b + f"{ranking}: " + f"分数{result['score']}\n"
    await get_rank.send(str_b)
    await get_rank.send(MessageSegment.image("file:///"+path+"\\screenshot.png"))
