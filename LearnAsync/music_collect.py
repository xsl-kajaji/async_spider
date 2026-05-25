import requests
import httpx

import asyncio
from parsel import Selector
from bs4 import BeautifulSoup
from lxml import etree
import ujson
import json


# # 解码
# ujson.loads()
# # 编码
# ujson.dumps()
async def send_async_requests(url:str):
    '''
    发送异步请求
    :return:
    '''

    async with httpx.AsyncClient() as client:
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.166 Safari/537.36'
        }
        response = await client.get(url=url,headers=headers,follow_redirects=True)
        # print(response.json()) # 返回json结果
        print(response.status_code)
        print(response.text) # 返回文本结果
        page_content = response.content.decode('utf-8')

        # 使用parsel创建选择器对象
        selector = Selector(page_content)

        # sentence = selector.xpath('//div[@class="left"]//div[@class="cont"]/a[1]/text()').extract()
        # source = selector.xpath('//div[@class="left"]//div[@class="cont"]/a[2]/text()').extract_first()
        # href = selector.xpath('//div[@class="left"]//div[@class="cont"]/a[1]/@href')

        sentence = selector.css('div.left div.cont > a:nth-of-type(1)::text').getall()
        source = selector.css('div.left div.cont > a:nth-of-type(2)::text').getall()
        href = selector.css('div.left div.cont > a:nth-of-type(1)::attr(href)').get()
        print(sentence)
        print(source)
        print(href)
        print(len(sentence))
        print(len(source))

def send_sync_requests(url:str):
    '''
    发送同步请求
    :return:
    '''

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.166 Safari/537.36'
    }
    response = requests.get(url=url,headers=headers)
    print(response.status_code)
    # print(response.json())
    print(response.text)
    page_content = response.content.decode('utf-8')

    # soup = BeautifulSoup(page_content,'lxml')
    # # content = soup.select('div.left  div.cont > a')[0].get_text().strip()
    # content = soup.select('div.left div.cont')
    # content_list = []
    # for item in content:
    #     sentence = item.find_all('a')[0].get_text()
    #     source = item.find_all('a')[1].get_text() if len(item.find_all('a')) > 1 else ''
    #     href = item.find_all('a')[0].get('href')
    #
    #     content_list.append([sentence,source,href])
    # print(content_list)

    html = etree.HTML(page_content)
    sentences = html.xpath('//div[@class="left"]//div[@class="cont"]/a[1]/text()')
    sources = html.xpath('//div[@class="left"]//div[@class="cont"]/a[2]/text()')
    hrefs = html.xpath('//div[@class="left"]//div[@class="cont"]/a[2]/@href')
    print(sentences)
    print(sources)
    print(hrefs)



if __name__ == '__main__':
    url = 'http://guwendao.net/mingjus/'
    # 协程调度器
    asyncio.run(send_async_requests(url))
    # send_sync_requests(url)
