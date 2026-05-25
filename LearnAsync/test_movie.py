import time
import random
from typing import Dict,List,Any
import requests
import csv

import ujson

from learn_pandas.LearnAsync.test import MovieContent, get_params_header_request

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


def movie_data_list() -> List[MovieContent]:
    '''
    获取所有电影数据的返回列表
    :return:
    '''
    movie_list:List[MovieContent] = []
    page_start = 0
    movie_data_dict = send_request(page_start)
    # 总数据量
    total_movie_num: int = movie_data_dict["total"]
    try:
        print("开始获取数据信息")
        print(f"获取到{total_movie_num}条数据")
    except Exception as e:
        print("错误信息：",e)


    while page_start < total_movie_num:
        movie_data_dict:Dict[str,Any] = send_request(page_start)
        for item in movie_data_dict["items"]:
            movie_content = parse_movie_content(item)
            print(movie_content)
            movie_list.append(movie_content)
        page_start += PAGE_SIZE
        time.sleep(random.randint(1,3))
    return movie_list


def send_request(page_start:int) -> Dict[str,Any]:
    '''
    获取请求的网页数据
    :param page_start: 更换请求网址参数来获取全部数据
    :return:
    '''
    cookies,headers,params = get_params_header_request()
    req_url = HOST + URL_API
    # 修改页码变动参数
    params['start'] = page_start

    response = requests.post(url=req_url,cookies=cookies,headers=headers,params=params)
    # data_dict = ujson.loads(response.text)
    # print("编码"+"*"*10)
    # print(type(data_dict))
    # print(data_dict)
    if response.status_code != 200:
        raise Exception("请求发生错误，原因：",response.text)

    try:
        response_data_dict = response.json()
        # print("json方法返回"+"="*10)
        # print(response_data_dict)
        return response_data_dict
    except Exception as e:
        raise e

def save_to_csv(file_name:str,movie_data_list:List[MovieContent]):
    '''
    保存数据列表为csv文件
    :param movie_data_list:
    :return:
    '''
    with open(file_name,mode='w',newline='',encoding='utf-8-sig') as file:
        write = csv.writer(file)
        # 写入标题行
        write.writerow(MovieContent.get_fields())
        for movie_data in movie_data_list:
            write.writerow([
                movie_data.id,
                movie_data.title,
                movie_data.rating,
                movie_data.card_subtitle
            ])

def main():
    movie_list = movie_data_list()
    save_to_csv("movie.csv",movie_list)

if __name__ == '__main__':
    main()

