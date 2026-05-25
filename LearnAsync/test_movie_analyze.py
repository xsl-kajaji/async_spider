import pandas as pd
from pandas import DataFrame
import numpy as np


def read_data(file_name:str)->DataFrame:
    '''
    读取路径文件信息
    :param path:
    :return:
    '''
    df = pd.read_csv(file_name)
    # 查看数据基本信息
    print(df.info())
    print(df.head())
    return df

def check_process_unique(df:DataFrame) -> DataFrame:
    '''
    检查处理数据重复
    :param movie_data_list:
    :return:
    '''
    df_duplicate = df.duplicated().sum()
    print(f"数据重复值情况:\n{df_duplicate}")
    if df_duplicate != 0:
        df.drop_duplicates(inplace=True, keep=False)

    print(f"去重后数据情况：\n{df.duplicated().sum()}")

    return df

def check_process_null(df:DataFrame) -> DataFrame:
    '''
    检查处理数据空值
    :param df:
    :return:
    '''
    df_null = df.isna().sum()
    print(f"数据缺失值情况:\n{df_null}")
    # id列直接删除
    df.dropna(subset=['id'])
    # 名称列改为无资源
    df['title'].fillna('未知', inplace=True)
    # 对年份,国家，剧情类型改为未知
    df['movie_year'].fillna('未知', inplace=True)
    df['movie_country'].fillna('未知', inplace=True)
    df['movie_type'].fillna('未知', inplace=True)

    print(f"处理缺失值后数据情况:\n{df.isnull().sum()}")

    return df

def split_process_data(df:DataFrame) -> DataFrame:
    '''
    分割和处理数据
    :param df:
    :return:
    '''

    # 对card_subtitle列进行分割处理，得到年份，国家，剧情，演员
    movie_year_list = []
    movie_country_list = []
    movie_type_list = []
    movie_actor_list = []
    for movie_data in df['card_subtitle']:
        length = len(movie_data.split('/'))
        movie_year = movie_data.split('/')[0].strip() if length > 1 else ''
        movie_country = movie_data.split('/')[1].strip() if length > 2 else ''
        movie_type = movie_data.split('/')[2].strip() if length > 3 else ''
        movie_actor = movie_data.split('/')[3].strip() if length >= 4 else ''
        # 对类型列进行处理
        if '剧情' in movie_type:
            movie_type = movie_type.replace('剧情','').strip()
        # 对演员列处理
        if length == 5:
            movie_actor += movie_data.split('/')[4].strip()

        movie_year_list.append(movie_year)
        movie_country_list.append(movie_country)
        if movie_type != '':
            movie_type_list.append(movie_type)
        else:
            movie_type_list.append(None)
        movie_actor_list.append(movie_actor)

    # 将分割后的数据加入dataframe中
    df['movie_year'] = movie_year_list
    df['movie_country'] = movie_country_list
    df['movie_type'] = movie_type_list
    df['movie_actor'] = movie_actor_list

    # 删除原先的列
    df.drop('card_subtitle', axis=1, inplace=True)

    return df

def save_to_csv(file_name:str, df:DataFrame) -> None:
    '''
    经处理后的数据保存到新的文件中
    :param file_name:
    :param df:
    :return:
    '''
    df.to_csv(file_name, index=False,columns=df.columns)

def main():
    df = read_data('async_movie.csv')
    split_df = split_process_data(df)
    drop_duplicate_df = check_process_unique(split_df)
    drop_na_df = check_process_null(drop_duplicate_df)
    save_to_csv("hand_async_movie.csv", drop_na_df)

if __name__ == '__main__':
    main()



