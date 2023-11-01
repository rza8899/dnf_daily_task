# coding: utf-8
# !/usr/bin/python
import random
from utils.app import find_app
from config.key_codes import CODES
from config.cfg import *
import time
import ctypes
from typing import List, Tuple
from airtest.core import api as air
import logging
from loguru import logger


class Base:
    def __init__(self, app_title: str):
        self.dll = ctypes.windll.LoadLibrary(MY_DLL)
        self.hdl = self.dll.M_Open(1)
        # 返回值如果是-10，表示该盒子不支持绝对移动功能。返回 0 表示执行正确
        logger.info('适用结果：{}'.format(self.dll.M_ResolutionUsed(self.hdl, WIDTH, HEIGHT)))
        # 获取app信息
        handle, self.app_head, self.app_tail, self.app_width, self.app_height = find_app(app_title)
        air.connect_device(f"Windows:///{handle}")
        logger.info('连接成功')
        # 关闭debug日志
        _log = logging.getLogger("airtest")
        _log.setLevel(logging.INFO)

    def __del__(self):
        if self.dll and self.hdl != -1:
            logger.info('关闭盒子')
            self.dll.M_Close(self.hdl)

    def click(self, mode: str, pointer: Tuple[int, int]) -> None:
        """
        鼠标点击
        :param mode: left左击，right右击
        :param pointer: 点击的坐标(x, y)
        :return:
        """
        logger.info('点击{}'.format(pointer))
        self.dll.M_MoveTo3(self.hdl, pointer[0], pointer[1])
        time.sleep(0.1)
        if mode.lower() == 'left':
            self.dll.M_LeftClick(self.hdl, 1)
        else:
            self.dll.M_RightClick(self.hdl, 1)
        time.sleep(0.1)

    def click_left(self, pointer: Tuple[int, int]) -> None:
        '''
        鼠标左键单击
        :param pointer: 绝对坐标
        :return:
        '''
        self.click('left', pointer)

    def click_right(self, pointer: Tuple[int, int]) -> None:
        '''
        鼠标右键单击
        :param pointer: 绝对坐标
        :return:
        '''
        self.click('right', pointer)

    def press_key(self, key: str, gap_time: float=0) -> None:
        '''
        模拟按键
        :param key:
        :param gap_time: 按下和释放按键间隔时间
        :return:
        '''
        key_code = CODES[key.lower()]
        if gap_time == 0:
            # 50-80ms的随机间隔时间
            self.dll.M_KeyPress(self.hdl, key_code, 1)
        else:
            self.dll.M_KeyDown(self.hdl, key_code)
            time.sleep(gap_time)
            self.dll.M_KeyUp(self.hdl, key_code)
        time.sleep(random.randint(10, 15)/100)

    def find_img(self, filepath: str, times: int=10, wait_time: float=0.3) -> list:
        """
        默认找10次，每次0.3秒
        :param filepath:
        :param times:
        :param wait_time:
        :return: [{'result': (85, 59), 'rectangle': ((52, 40), (52, 78), (118, 78), (118, 40)), 'confidence': 0.99}]
        """
        filename = filepath.split(os.sep)[-1]
        for i in range(times):
            file_info = air.find_all(air.Template(filepath))
            logger.info(f'第{i + 1}次查结果查找结果：{file_info}')
            if file_info:
                logger.info(f'第{i + 1}次存在{filename}')
                return file_info
            else:
                time.sleep(wait_time)
        logger.info(f'不存在{filename}')
        return []

    def get_abs_pos(self, pos: List[tuple or dict]) -> list:
        '''
        获取一个或多个坐标的绝对位置，原坐标加上app_head的x和y坐标
        :param pos:
        :return:
        '''
        abs_pos_list = []
        for pos_item in pos:
            if isinstance(pos_item, dict):
                pos_tuple = pos_item['result']
            elif isinstance(pos_item, tuple):
                pos_tuple = pos_item
            else:
                raise Exception('坐标类型为：{}，不正确'.format(type(pos_item)))
            abs_pos = tuple(map(lambda x, y: x + y, pos_tuple, self.app_head))
            abs_pos_list.append(abs_pos)
        return abs_pos_list


b = Base(APP_TITLE)
