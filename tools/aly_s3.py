# -*- coding: utf-8 -*-
"""
@Tool : PyCharm

@User : 21407

@File : aly_s3.py

@Email: yypqcaa@163.com

@Date : 2022/9/14 20:09

@Desc :
"""
# -*- coding: utf-8 -*-
import oss2
from pathlib import Path
from loguru import logger


class AlyS3:

    def __init__(self, str_name: str, str_pwd: str, str_bucket: str, str_url: str):
        self.str_name = str_name
        self.str_pwd = str_pwd
        self.bucket = str_bucket
        self.url = str_url

    def __login(self):
        auth = oss2.Auth(self.str_name, self.str_pwd)
        # 填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
        bucket = oss2.Bucket(auth, self.url, self.bucket)
        return bucket

    def push_file(self, str_path: str) -> int:
        int_ret = 0
        try:
            if Path(str_path).is_file():
                bucket = self.__login()
                # 必须以二进制的方式打开文件。
                # 填写本地文件的完整路径。如果未指定本地路径，则默认从示例程序所属项目对应本地路径中上传文件。
                with open(str_path, 'rb') as f:
                    # 填写Object完整路径。Object完整路径中不能包含Bucket名称。
                    bucket.put_object(Path(str_path).name, f)
                int_ret = 1
        except Exception as e:
            logger.error(f"{e.__traceback__.tb_lineno}:--:{e}")
        return int_ret

    def get_file(self, lst_filter: list = None) -> list:
        # 列举Bucket下的所有文件。
        lst_ret = []
        try:
            for obj in oss2.ObjectIteratorV2(self.__login()):
                if not lst_filter or Path(obj.key).name in lst_filter:
                    lst_ret.append({'name': obj.key, 'url': f'https://{self.bucket}.{self.url.split("//", 1)[-1]}/{obj.key}'})
        except Exception as e:
            logger.error(f"{e.__traceback__.tb_lineno}:--:{e}")
        return lst_ret

    def pull_file(self, str_path: str, str_file):
        # 填写Object完整路径，完整路径中不包含Bucket名称，例如testfolder/exampleobject.txt。
        # 下载Object到本地文件，并保存到指定的本地路径D:\\localpath\\examplefile.txt。如果指定的本地文件存在会覆盖，不存在则新建。
        int_ret = 0
        try:
            bucket = self.__login()
            bucket.get_object_to_file(str_path, Path.joinpath(str_file, str_path).__str__())
            if Path(str_file).is_file():
                int_ret = 1
        except Exception as e:
            logger.error(f"{e.__traceback__.tb_lineno}:--:{e}")
        return int_ret


