import requests

class MovieContent:
    id:str = "" # 影片id
    title:str = "" # 影片名称
    rating:int = 0 # 影片评分
    card_subtitle:str = "" # 影片信息

    @classmethod
    def get_fields(cls):
        '''
        获取数据的键值
        :return:
        '''
        return [key for key in cls.__dict__.keys() if not key.startswith("__") and key != 'get_fields']


    def __str__(self):
        '''
        重写__str__方法，打印对象信息
        :return:
        '''
        return f'''
            "id":{self.id},
            "title":{self.title},
            "rating":{self.rating},
            "card_subtitle":{self.card_subtitle}
        '''
def get_params_header_request():
        '''
        获取爬取电影网址的必要参数
        :return:
        '''
        cookies = {
            'll': '"118239"',
            'bid': 'oWg8Gp19APA',
            '_vwo_uuid_v2': 'D345AB71E1F9275B0EE713C8BAFB64CF1|72a87c1f6f2aa91a382fb3d8393938ea',
            'Hm_lvt_6d4a8cfea88fa457c3127e14fb5fabc2': '1758869774',
            '_ga': 'GA1.1.1167380508.1758869774',
            '_ga_Y4GN1R87RG': 'GS2.1.s1758869774$o1$g1$t1758869846$j60$l0$h0',
            '_ga_RXNMP372GL': 'GS2.1.s1762161773$o1$g0$t1762161774$j59$l0$h0',
            '__utmz': '30149280.1779276082.28.11.utmcsr=baidu|utmccn=(organic)|utmcmd=organic',
            'viewed': '"2995812_6113840_33415617_35044046_26980487"',
            '__utmc': '30149280',
            'ap_v': '0,6.0',
            '__utma': '30149280.1385649044.1758809853.1779354192.1779365549.31',
            '__utmb': '30149280.0.10.1779365549',
            'RT': 'nu=https%3A%2F%2Fmovie.douban.com%2Freview%2Fbest%2F&cl=1779366734242&r=https%3A%2F%2Fmovie.douban.com%2Fchart&ul=1779366734244&hd=1779366734408',
        }

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'origin': 'https://movie.douban.com',
            'priority': 'u=1, i',
            'referer': 'https://movie.douban.com/explore',
            'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
            # 'cookie': 'll="118239"; bid=oWg8Gp19APA; _vwo_uuid_v2=D345AB71E1F9275B0EE713C8BAFB64CF1|72a87c1f6f2aa91a382fb3d8393938ea; Hm_lvt_6d4a8cfea88fa457c3127e14fb5fabc2=1758869774; _ga=GA1.1.1167380508.1758869774; _ga_Y4GN1R87RG=GS2.1.s1758869774$o1$g1$t1758869846$j60$l0$h0; _ga_RXNMP372GL=GS2.1.s1762161773$o1$g0$t1762161774$j59$l0$h0; __utmz=30149280.1779276082.28.11.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; viewed="2995812_6113840_33415617_35044046_26980487"; __utmc=30149280; ap_v=0,6.0; __utma=30149280.1385649044.1758809853.1779354192.1779365549.31; __utmb=30149280.0.10.1779365549; RT=nu=https%3A%2F%2Fmovie.douban.com%2Freview%2Fbest%2F&cl=1779366734242&r=https%3A%2F%2Fmovie.douban.com%2Fchart&ul=1779366734244&hd=1779366734408',
        }

        params = {
            'start': '0',
            'limit': '20',
            'category': '最新',
            'type': '全部',
        }

        response = requests.get(
            'https://m.douban.com/rexxar/api/v2/subject/recent_hot/movie',
            params=params,
            cookies=cookies,
            headers=headers,
        )

        return cookies,headers,params






