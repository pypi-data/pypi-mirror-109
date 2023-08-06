#!/usr/bin/env python
# coding: utf-8
from os import PathLike
from .path import FSPath

class NotFileError(Exception): ...

class LockedFileError(Exception): ...

class File(FSPath):

    def __init__(self, x: PathLike) -> None:
        super().__init__(x)
        if self.exists and self.is_not_file:
            raise NotFileError(self.posix)
        self.locked = False

    def iterator(self, chunk_size=512):
        """
        按块读取文件，防止文件过大导致内存溢出
        :param file_path: 文件路径
        :param chunk_size: 每次读取的块大小
        :return: 一个生成器
        """
        self.check_lock()
        self.locked = True
        with open(self.posix, 'r') as reader:
            while True:
                chunk = reader.read(chunk_size)
                if chunk:
                    yield chunk
                else:
                    break
        self.locked = False

    def check_lock(self) -> None:
        if self.locked:
            raise LockedFileError(self.posix)


def write_once(fp: PathLike, data):
        """
        写入一个数据到一个文件，然后关闭文件
        :param fp:
        :param data: 任意类型的数据
        :param data_type: 数据的类型，与Python3的类型注解一致
            支持的类型有:
            1. str 写入一个字符串
            2. List[str] 写入一个字符串数组
        :return:
        """

        text = None
        if isinstance(data, str):
            text = data
        elif isinstance(data, list):
            if any([isinstance(i, str) for i in data]):
                text = '\n'.join(data)
            elif any([isinstance(i, int) for i in data]):
                text = '\n'.join([int(i) for i in data])
        
        if text is None:
            raise ValueError('Not supported type')

        with open(fp, 'w') as writer:
            writer.write(text)
