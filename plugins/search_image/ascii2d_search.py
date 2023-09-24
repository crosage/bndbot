from nonebot import on_command
from nonebot.adapters.onebot.v11.message import Message,MessageSegment
from nonebot.params import CommandArg
import requests
from nonebot.adapters.onebot.v11 import Bot,Event
from bs4 import BeautifulSoup
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import Bot
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/99.0.4844.82 Safari/537.36"
    )
}


class Ascii2dImg:
    def __init__(self,name,thumbUrl,url,source) :
        self.name=name
        self.thumbUrl=thumbUrl
        self.url=url
        self.source=source
        

def dealer(data):
    infos=data.find("div",{"detail-box gray-link"})
    thumbUrl=data.find("img")
    thumbUrl="https://ascii2d.net"+thumbUrl["src"]
    if infos:
        logger.info(infos)
        h6=infos.find("h6")
        external=infos.find("div",{"external"})
        if h6:
            # 图片来源
            small=h6.find("small")
            # 图片来源链接
            links=h6.find("a")
            name=links.string
            return Ascii2dImg(name,thumbUrl,links["href"],small.string)
        elif external:
            links=external.find("a")
            name=links.string
            logger.warning("********")
            logger.warning(links)
            logger.warning(name)
            return Ascii2dImg(name,thumbUrl,links["href"],"\ntwitter\n")

            
search_image=on_command("搜图")
@search_image.handle()
async def search_image_handler(bot:Bot,event:Event, args:Message=CommandArg()): 
    _,group,qq=str(event.get_session_id()).split("_")
    ascii2d_url="https://ascii2d.net/search/uri"
    data={
    }
    logger.debug("搜图")
    for arg in args:
        if arg.type!="image":
            await search_image.finish("你没有发送图片")
        data.update({"uri":arg.data["url"]})
        resp=requests.post(
            url=ascii2d_url,
            data=data,
            proxies={
                "http":"http://127.0.0.1:7890",
                "https":"http://127.0.0.1:7890"
            },
        headers=DEFAULT_HEADERS)
        bovw=requests.get(
            resp.url.replace("color","bovw"),
            proxies={
                "http":"http://127.0.0.1:7890",
                "https":"http://127.0.0.1:7890"
            },
            headers=DEFAULT_HEADERS
        )
        print(bovw.url)
        soup=BeautifulSoup(bovw.text,features="html.parser")
        print(bovw.text)
        blocks=soup.find_all("div",{'class': 'row item-box'})
        msgs=[]
        try:
            cnt=0
            for i in blocks:
                cnt=cnt+1
                if cnt==6:
                    break
                logger.warning("开始处理")
                logger.error("i=***********")
                logger.warning(i)
                logger.error("i=************")
                ascii2dImg=dealer(i)
                logger.warning("处理结束")
                if ascii2dImg==None:
                    continue

                msg=(
                    MessageSegment.text("标题:"+ascii2dImg.name)+
                    MessageSegment.image(ascii2dImg.thumbUrl)+
                    MessageSegment.text("来源:"+ascii2dImg.source)+
                    MessageSegment.text(ascii2dImg.url)
                )
                logger.error(type(msg))
                tmp={
                        "type":"node",
                        "data":{
                            "name":"测试",
                            "uin":3408476436,
                            "content":msg
                        }
                    }
                msgs.append(tmp)
        finally:
            logger.debug(msgs)
            await bot.send_group_forward_msg(group_id=group,messages=msgs)

