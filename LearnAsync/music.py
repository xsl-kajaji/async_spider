
from typing import List

class MusicContent:
    name:str = "" # 音乐名称
    author:str = "" # 音乐作者
    time:str = "" # 出版时间
    varity:str = "" # 音乐类型

    # 类方法
    @classmethod
    def get_fields(cls) -> List[str]:
        '''
        获取类的属性
        :return:
        '''
        print(cls.__dict__)
        return [key for key in cls.__dict__.keys() if not key.startswith("__") and key != "get_fields"]

    def __str__(self):
        '''
        重写__str__方法，用于打印对象的信息
        :return:
        '''
        return f"""
            Name: {self.name}
            Author: {self.author}
            Time: {self.time}
            Varity: {self.varity}"""

def get_req_params_and_headers():
    '''
    用于获取请求网页的响应参数
    :return:
    '''
    pass
