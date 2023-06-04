import aiohttp
from nonebot.log import logger
import nonebot
my_cookie=nonebot.get_driver().config.my_cookie
class HttpFecher(object):
    default_timeout_time:int=10
    _default_headers: dict[str, str] = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,zh;q=0.9',
        'dnt': '1',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-gpc': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
        "cookie":"PHPSESSID="+my_cookie
    }
    _http_proxy_config="http://localhost:7890"
    def __init__(self,timeout,cookies:dict[str,str],headers:dict[str,str]) -> None:
        _headers=self._default_headers if headers is None else headers
        self.headers=_headers
        self.cookies=cookies
        self.timeout=timeout
    @classmethod
    def get_default_headers(cls) -> dict[str, str]:
        return cls._default_headers
    
    async def get_json_dict(self,url:str,params:dict[str,str]):
        async with aiohttp.ClientSession(timeout=20) as session:
            async with session.get(url=url,headers=self.headers,params=params,proxy=self._http_proxy_config,timeout=self.timeout) as rp:
                logger.warning(f"{rp.headers}")
                logger.warning(f"{self.headers}")
                # logger.warning(f"{await rp.text()}")
                # logger.info(f"{await rp.read()}")
                logger.error(f"{rp.status}")
                _json=await rp.json()
                _result={"status":rp.status,"headers":rp.headers,"cookies":rp.cookies,"result":_json}
                logger.info(f"data{rp.status}")
                return _result
    async def get_bytes(self,url: str,*,params: dict[str, str] | None = None):
        async with aiohttp.ClientSession(timeout=20) as session:
            async with session.get(url=url,params=params,headers=self.headers,cookies=self.cookies,proxy=self._http_proxy_config,timeout=self.timeout) as rp:
                _bytes = await rp.read()
                _result = {'status': rp.status, 'headers': rp.headers, 'cookies': rp.cookies, 'result': _bytes}
        return _result