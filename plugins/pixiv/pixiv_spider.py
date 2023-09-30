from math import ceil
from PIL import ImageFont, Image, ImageDraw
from nonebot.adapters.onebot.v11 import MessageSegment
from .pixiv_fetcher import HttpFecher
from datetime import datetime
from nonebot.log import logger
import random
from io import BytesIO
import aiohttp
import requests
import re
from .model import PreviewImageModel, PreviewImageThumbs
from .model import PixivArtworkPreviewModel
from ..configs import pixiv_preview_path
from ..configs import pixiv_path, default_font_path
import datetime
from pymysql import *
import nonebot
from nonebot.plugin import on_command
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import Message
from ..management_module.management_db_operations import is_function_enabled
from nonebot.typing import T_State
from nonebot.params import CommandArg, ArgStr

threshold = 100
my_cookie = nonebot.get_driver().config.my_cookie


class Pixiv(object):
    _default_headers = HttpFecher._default_headers
    _api_fetcher = HttpFecher(timeout=10, headers=_default_headers, cookies={"cookies": my_cookie})


def resize_with_filling(preimage, size: tuple[int, int]):
    """在不损失原图长宽比的条件下, 使用透明图层将原图转换成指定大小"""
    _image = preimage
    # 计算调整比例
    width, height = _image.size
    rs_width, rs_height = size
    scale = min(rs_width / width, rs_height / height)

    _image = _image.resize((int(width * scale), int(height * scale)))
    box = (int(abs(width * scale - rs_width) / 2), int(abs(height * scale - rs_height) / 2))
    background = Image.new(mode="RGBA", size=size, color=(255, 255, 255, 0))
    background.paste(_image, box=box)

    preimage = background
    return preimage


async def generate_thumbs_preview_image(
        preview: PreviewImageModel,
        preview_size: tuple[int, int] = (512, 512),
        *,
        font_path: str = default_font_path,
        header_color: tuple[int, int, int] = (255, 255, 255),
        hold_ratio: bool = True,
        num_of_line: int = 5,
        limit: int = 1000
):
    """生成多个带说明的缩略图的预览图

    :param preview: 经过预处理的生成预览的数据
    :param preview_size: 单个小缩略图的尺寸
    :param font_path: 用于生成预览图说明的字体
    :param header_color: 页眉装饰色
    :param hold_ratio: 是否保持缩略图原图比例
    :param num_of_line: 生成预览每一行的预览图数
    :param limit: 限制生成时加载 preview 中图片的最大值
    :param output_folder: 输出文件夹
    """

    previews = preview.previews
    preview_name = preview.preview_name

    def _handle_preview_image() -> bytes:
        """用于图像生成处理的内部函数"""
        _thumb_w, _thumb_h = preview_size
        _font_path = default_font_path
        _font_main = ImageFont.truetype(_font_path, _thumb_w // 15)
        _font_title = ImageFont.truetype(_font_path, _thumb_w // 5)

        # 输出图片宽度
        _preview_w = _thumb_w * num_of_line

        # 标题
        _title = preview.preview_name
        # 计算标题尺寸
        _title_w, _title_h = _font_title.getsize_multiline(text=_title)

        # 根据缩略图计算标准间距
        _spacing_w = int(_thumb_w * 0.4)
        _spacing_title = _spacing_w if _title_h <= int(_spacing_w * 0.75) else int(_title_h * 1.5)

        _background = Image.new(
            mode="RGB",
            size=(_preview_w, (_thumb_h + _spacing_w) * ceil(len(previews) / num_of_line) + _spacing_title),
            color=(255, 255, 255))

        # 画一个装饰性的页眉
        # 处理颜色
        light = tuple(z if z > 0 else 0 for z in (y if y < 255 else 255 for y in (int(x / 0.9) for x in header_color)))
        dark = tuple(z if z > 0 else 0 for z in (y if y < 255 else 255 for y in (int(x * 0.9) for x in header_color)))

        ImageDraw.Draw(_background).polygon(
            xy=[(0, 0), (0, _title_h), (_title_h, 0)],
            fill=dark
        )  # 左上角下层小三角形
        ImageDraw.Draw(_background).polygon(
            xy=[(0, 0), (_preview_w, 0), (_preview_w, int(_title_h / 8)), (0, int(_title_h / 8))],
            fill=header_color
        )  # 页眉横向小蓝条
        ImageDraw.Draw(_background).polygon(
            xy=[(0, 0), (0, int(_title_h * 5 / 6)), (int(_title_h * 5 / 6), 0)],
            fill=light
        )  # 左上角最上层小三角形

        # 写标题
        ImageDraw.Draw(_background).multiline_text(
            xy=(_preview_w // 2, int(_title_h / 3)), text=_title, font=_font_title,
            align='center', anchor='ma', fill=(0, 0, 0))

        # 处理拼图
        _line = 0
        for _index, _preview in enumerate(previews):
            with BytesIO(_preview.preview_thumb) as bf:
                _thumb_img: Image.Image = Image.open(bf)
                _thumb_img.load()
            # 调整图片大小
            if hold_ratio:
                _thumb_img = resize_with_filling(_thumb_img, preview_size)
            h = _thumb_img.height
            w = _thumb_img.width
            bili: float = 0
            if h >= w:
                bili = preview_size[0] / h
            else:
                bili = preview_size[1] / w
            if _thumb_img.size != preview_size:
                _thumb_img = _thumb_img.resize(size=(int(w * bili), int(h * bili)))

            # 确认缩略图单行位置
            seq = _index % num_of_line
            # 能被整除说明在行首要换行
            if seq == 0:
                _line += 1
            logger.info(f"{seq * _thumb_h}      {seq * _thumb_w + _thumb_w / 2}")
            # 按位置粘贴单个缩略图
            _background.paste(_thumb_img, box=(seq * _thumb_w, (_thumb_h + _spacing_w) * (_line - 1) + _spacing_title))
            ImageDraw.Draw(_background).multiline_text(
                xy=(seq * _thumb_w + _thumb_w // 2,
                    (_thumb_h + _spacing_w) * (_line - 1) + _spacing_title + _thumb_h + _spacing_w // 10),
                text=_preview.desc_text, font=_font_main,
                align='center', anchor='ma', fill=(0, 0, 0))
        # 生成结果图片
        with BytesIO() as _bf:
            _background.save(_bf, 'JPEG')
            _content = _bf.getvalue()
        return _content

    image_content = _handle_preview_image()
    image_file_name = f"preview_{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.jpg"
    newpath = pixiv_preview_path + "\\" + image_file_name
    logger.warning(f"{newpath}")
    with open(pixiv_preview_path + "\\" + image_file_name, "wb") as f:
        f.write(image_content)
    return pixiv_preview_path + "\\" + image_file_name


async def fetch_image(session, imgurl, new_header, proxys, illust_id, rank, user_name):
    try:
        logger.info(f"async url={imgurl}")
        async with session.get(url=imgurl, headers=new_header, cookies={"cookies": my_cookie}, proxy=proxys) as resp:
            if resp.status == 200:
                img = await resp.read()
                return {"img": img, "illust_id": illust_id, "rank": rank, "user_name": user_name}
            else:
                imgurl = imgurl.replace("jpg", "png")
                async with session.get(url=imgurl, headers=new_header, cookies={"cookies": my_cookie},
                                       proxy=proxys) as resp2:
                    if resp2.status == 200:
                        img = await resp.read()
                        return await {"img": img, "illust_id": illust_id, "rank": rank, "user_name": user_name}
    except Exception as e:
        logger.error(f"{e}")


import asyncio


class PixivRanking(Pixiv):
    ranking_url: str = "https://www.pixiv.net/ranking.php"

    @classmethod
    async def query_ranking(cls, mode="daily", content="illust", page: int = 1):
        params = {"format": "json", "mode": mode, "p": page, "content": content}
        logger.warning("开始")
        ranking_data = await cls._api_fetcher.get_json_dict(url=cls.ranking_url, params=params)
        if ranking_data["status"] != 200:
            print(f"FATAL status={ranking_data.result}")
        logger.warning("1234654")
        ranking_data = ranking_data["result"]

        preview = PreviewImageModel()
        preview.preview_name = f"Pixiv Daily Ranking {datetime.datetime.now().strftime('%Y-%m-%d')}"
        async with aiohttp.ClientSession() as session:
            cnt = 0
            task = []
            for content in ranking_data["contents"]:
                cnt = cnt + 1
                imgurl = content["url"]
                new_headers = HttpFecher.get_default_headers()
                new_headers.update({"Referer": "https://www.pixiv.net/artworks/" + str(content["illust_id"])})
                task.append(
                    fetch_image(session, imgurl, new_headers, "http://localhost:7890", illust_id=content['illust_id'],
                                rank=content["rank"], user_name=content["user_name"]))
            results = await asyncio.gather(*task)
            for imgs in results:
                logger.error(f"Pid:{imgs['illust_id']}\n[No.{imgs['rank']}]\nAuther:{imgs['user_name']}")
                preview.previews.append(
                    PreviewImageThumbs(f"Pid:{imgs['illust_id']}\n[No.{imgs['rank']}]\nAuther:{imgs['user_name']}",
                                       imgs["img"]))
        returnpath = await generate_thumbs_preview_image(preview=preview)
        return returnpath
        # logger.info("结束")
    @classmethod
    async def get_ranking_with_images(cls, mode="daily", content="illust", page: int = 1):
        pass
    @classmethod
    async def get_by_id(cls, id, allow_18=1, need_threshold=0):
        _headers = HttpFecher.get_default_headers()
        _headers.update({"referer": "https://www.pixiv.net"})
        imgurl = f"https://www.pixiv.net/artworks/{id}"
        logger.error(f"{imgurl}")
        async with aiohttp.ClientSession() as session:
            async with session.get(url=imgurl, headers=_headers, cookies={"cookies": my_cookie},
                                   proxy="http://localhost:7890") as resp:
                result = await resp.text()
            if resp.status != 200:
                return "error"
            pattern = re.compile(r'\"https://i.pximg.net/img-original/img.*?\"')
            patterns = re.compile(r'R-18')
            newurl = pattern.search(result).group()
            newurl = newurl.replace("\\", "")
            newurl = newurl.replace("\"", "")
            if allow_18 == 0:
                try:
                    patterns.search(result).group()
                    return "R-18"
                except:
                    logger.info("非R-18")
            async with session.get(url=newurl, headers=_headers, cookies={"cookies": my_cookie},
                                   proxy="http://localhost:7890") as resp2:
                result2 = await resp2.read()
                new_path = pixiv_path + f"\\{id}"
                imgtype = str(newurl.split(".")[-1])
                with open(new_path + f"_p{0}." + imgtype, "wb") as f:
                    f.write(result2)
                return new_path + f"_p{0}." + imgtype


# loop=asyncio.get_event_loop()
# res=loop.run_until_complete((PixivRanking.query_ranking(mode="daily")))
# loop.close()
# async def depend():

def deal_unable(path, filename):  # 图库地址和文件名
    img = Image.open(path + filename)
    h = img.height
    w = img.width
    img = img.resize(size=(int(w * 0.9), int(h * 0.9)))
    # img=img.rotate(180)
    logger.error(path + f"/tmp.png")
    img.save(path + f"/tmp.png")


async def get_ranking(r18_flag, ranking_type, page):
    if not page:
        page = 1
    logger.error(f"r:{r18_flag} type:{ranking_type} page:{page}")
    # logger.info(f"r{r18_flag} {ranking_type} {page}")
    if r18_flag == "r":
        if ranking_type == "日":
            path = await PixivRanking.query_ranking(mode="daily_r18", page=page)
        elif ranking_type == "周":
            path = await PixivRanking.query_ranking(mode="weekly_r18", page=page)
        elif ranking_type == "月":
            path = await PixivRanking.query_ranking(mode="monthly_r18", page=page)
        return path

    else:
        if ranking_type == "日":
            path = await PixivRanking.query_ranking(mode="daily", page=page)
        elif ranking_type == "周":
            path = await PixivRanking.query_ranking(mode="weekly", page=page)
        elif ranking_type == "月":
            path = await PixivRanking.query_ranking(mode="monthly", page=page)
        return path


pixiv = on_command("pixiv", aliases={"pi"}, priority=20, block=True)


@pixiv.handle()
async def pixiv_handle(bot: Bot, event: Event, state: T_State, cmd_arg: Message = CommandArg()):
    _, group, qq = str(event.get_session_id()).split("_")
    # if isInGroup(group,"pixiv")==0:
    #     return 
    args = cmd_arg.extract_plain_text().strip()
    pattern = r"(r)?([月周日]?)(\d*)"
    match = re.match(pattern, args)
    if match:
        r18_flag = match.group(1)
        ranking_type = match.group(2)
        page = match.group(3)

        try:
            path =await get_ranking(r18_flag, ranking_type, page)
            await pixiv.send(MessageSegment.image("file:///" + path))
        except:
            await pixiv.send("发送失败")

        # 进行根据pid搜图，或根据tag搜图


pixiv_id = on_command("pixiv搜图", aliases={"pis"}, priority=30, block=True)


@pixiv_id.handle()
async def pixiv_id_handle(bot: Bot, event: Event, state: T_State, cmd_arg: Message = CommandArg()):
    _, group, qq = str(event.get_session_id()).split("_")
    logger.info("被pixiv接收到")
    pid = cmd_arg.extract_plain_text().strip()
    flag = 1
    logger.warning(f"{pid}")
    if pid.isdigit():
        path = await PixivRanking.get_by_id(pid, flag)
        logger.info(path)
        logger.warning("********")
        if path == "R-18":
            await pixiv.finish(f"这个群没有开启18+")
        if path == "error":
            await pixiv.send(f"没有这个图QAQ {pid}")
        else:
            try:
                await pixiv.send(MessageSegment.image("file:///" + path))
            except:
                deal_unable(path[0:path.rfind("\\") + 1], path[path.rfind("\\") + 1:])
                await pixiv.send(f"这个图被吞了，对不起喵{pid}")
                await pixiv.send(MessageSegment.image("file:///" + path[0:path.rfind("\\") + 1] + "tmp.png"))
    else:
        tag = pid
        pixiv_url = 'http://127.0.0.1:8000/api/image'
        data = {'offset': 0, 'limit': 10000, "tag": [tag]}
        response = requests.post(pixiv_url, json=data)
        result = response.json()
        illusts = result["images"]
        illust = illusts[random.randint(0, illusts.__len__() - 1)]
        print(illust)
        await pixiv.send(f"pid:{illust['pid']}  author:{illust['author']}")
        logger.info("file:///" + illust["path"] + "\\" + illust["name"])
        try:
            await pixiv.send(MessageSegment.image("file:///" + illust["path"] + "\\" + illust["name"]))
        except:
            deal_unable(illust["path"] + "\\", illust["name"])
            await pixiv.send(f"这个图被吞了，对不起喵{illust['pid']}")
            await pixiv.send(MessageSegment.image("file:///" + illust["path"] + "\\" + "tmp.png"))

from nonebot.adapters.onebot.v11 import MessageSegment
import nonebot
from nonebot import require

from nonebot.log import  logger
test = require("nonebot_plugin_apscheduler").scheduler

@test.scheduled_job("cron", hour='12', minute='10', id="test")
async def testt():
    (bot,) = nonebot.get_bots().values()
    logger.warning("running")
    await bot.send(
        message_type="group",
        group_id=int(602683715),
        message="也许会推送日榜"
    )
    path=await get_ranking("r","日",1)
    logger.warning(f"path={path}")

    await bot.send(
        message_type="group",
        group_id=int(602683715),
        message=MessageSegment.image("file:///" + path)
    )

