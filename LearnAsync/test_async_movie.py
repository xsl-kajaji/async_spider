import requests
import httpx
import asyncio

import aiofiles
import csv
from typing import List,Dict,Any


from learn_pandas.LearnAsync.test import MovieContent, get_params_header_request
import random


HOST = "https://m.douban.com"
URL_API = "/rexxar/api/v2/subject/recent_hot/movie"
PAGE_SIZE = 20


def parse_movie_content(item:Dict) -> MovieContent:
    '''
    提取返回的json数据
    :param item: 获取的单个电影对象
    :return:
    '''
    movie_content = MovieContent()
    movie_content.id = item["id"] if item.get('id') is not None else ""
    movie_content.title = item["title"] if item.get('title') is not None else ""
    movie_content.rating = item["rating"]["value"] if item['rating'].get('value') is not None else ""
    movie_content.card_subtitle = item["card_subtitle"] if item.get('card_subtitle') is not None else ""

    return movie_content



async def signal_movie_data(page_start:int) -> List[MovieContent]:
    '''
    并发协程需要
    获取单个页面电影列表
    :return:
    '''

    try:
        response_data:Dict = await send_request(page_start)
        # print(response_data['items'])
        # for item in response_data['items']:
        #     print(item)
        single_movie_data = [parse_movie_content(item) for item in response_data['items']]
        print(f"开始获取{int(page_start/PAGE_SIZE)+1}页数据")
        return single_movie_data
    except Exception as e:
        print(f"获取{int(page_start/PAGE_SIZE + 1)}页数据错误",e)
        return []

async def movie_data_list() -> List[MovieContent]:
    '''
    获取所有电影数据的返回列表
    :return:
    '''
    # movie_list:List[MovieContent] = []
    # page_start = 0
    # movie_data_dict = await send_request(page_start)
    # # 总数据量
    # total_movie_num: int = movie_data_dict["total"]
    # try:
    #     print("开始获取数据信息")
    #     print(f"获取到{total_movie_num}条数据")
    # except Exception as e:
    #     print("错误信息：",e)
    #
    #
    # while page_start < total_movie_num:
    #     movie_data_dict:Dict[str,Any] = await send_request(page_start)
    #     for item in movie_data_dict["items"]:
    #         movie_content = parse_movie_content(item)
    #         print(movie_content)
    #         movie_list.append(movie_content)
    #     page_start += PAGE_SIZE
    #     await asyncio.sleep(random.randint(1,3))
    # return movie_list

    # 并发协程
    try:
        page_start = 0
        movie_dict = await send_request(page_start)
        total_movie_num:int = movie_dict["total"]
        page_starts = list(range(page_start,total_movie_num,PAGE_SIZE))
        print(f"共发起{len(page_starts)}条网络请求")

        tasks = [signal_movie_data(page_start) for page_start in page_starts]
        results = await asyncio.gather(*tasks)
        return [item for data in results for item in data]
    except Exception as e:
        print("发起请求失败",e)
    return []

async def send_request(page_start:int) -> Dict[str,Any]:
    '''
    获取请求的网页数据
    :param page_start: 更换请求网址参数来获取全部数据
    :return:
    '''
    cookies,headers,params = get_params_header_request()
    req_url = HOST + URL_API
    # 修改页码变动参数
    params['start'] = page_start

    # 同步
    # response = requests.post(url=req_url,cookies=cookies,headers=headers,params=params)

    # 异步
    async with httpx.AsyncClient() as client:
        response = await client.post(url=req_url,cookies=cookies,headers=headers,params=params)
    if response.status_code != 200:
        raise Exception("请求发生错误，原因：",response.text)

    try:
        response_data_dict:Dict[str,Any] = response.json()
        return response_data_dict
    except Exception as e:
        raise e

async def save_to_csv(file_name:str,movie_data_list:List[MovieContent]):
    '''
    保存数据列表为csv文件
    :param movie_data_list:
    :return:
    '''
    # async with aiofiles.open(file_name,mode='w',newline='',encoding='utf-8') as file:
    #     write = csv.writer(file)
    #     # 写入标题行
    #     await write.writerow(MovieContent.get_fields())
    #     for movie_data in movie_data_list:
    #         await write.writerow([
    #             movie_data.id,
    #             movie_data.title,
    #             movie_data.rating,
    #             movie_data.card_subtitle
    #         ])

    # 并发协程
    async with aiofiles.open(file_name,mode='w',encoding='utf-8-sig') as file:
        await file.write(",".join(MovieContent.get_fields())+"\n")
        for movie_data in movie_data_list:
            await file.write(
                f"{movie_data.id},{movie_data.title},{movie_data.rating},{movie_data.card_subtitle}\n"
            )

async def main():
    movie_list = await movie_data_list()
    await save_to_csv("async_movie.csv",movie_list)

if __name__ == '__main__':
    asyncio.run(main())




