import httpx
from loguru import logger
from ujson import loads
from package.Config.config import Proxy
from package.Config.config import User


def get_self_pp_plus():
    """
    从pp+网站获取pp+
    :return: pp+的用户信息['user_data']
    """
    proxyS = Proxy()
    httpP = proxyS.httpProxy()
    user = User()
    userid = user.userid()
    if proxyS.switch_ppPlus():
        if httpP is not None:
            logger.info(f'代理已开启{httpP}')
            url = 'https://syrin.me/pp+/api/user/' + userid + '/'
            with httpx.Client(proxies=httpP) as client:
                index = client.get(url=url, timeout=30)
        else:
            url = 'https://syrin.me/pp+/api/user/' + userid + '/'
            with httpx.Client() as client:
                index = client.get(url=url, timeout=30)
    else:
        url = 'https://syrin.me/pp+/api/user/' + userid + '/'
        with httpx.Client() as client:
            index = client.get(url=url, timeout=30)
    pp_plus = loads(index.text)
    return pp_plus['user_data']
