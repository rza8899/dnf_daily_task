# coding: utf-8
# !/usr/bin/python
import win32gui
from loguru import logger

def find_app(app_title: str) -> tuple:
    """
    :param app_title:地下城与勇士：创新世纪
    :return: 返回handle、app左上角坐标、右下角坐标、宽、高。eg: (328518, (49, 69), (1009, 669), 960, 600)
    """
    hwnd_title = {}

    def get_all_hwnd(hwnd, nothing):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})

    win32gui.EnumWindows(get_all_hwnd, 0)
    handle = 0
    for handle_item, title_item in hwnd_title.items():
        logger.info('窗口title：{}'.format(title_item))
        if title_item == app_title:
            handle = handle_item
            break
    if handle == 0:
        raise Exception('未找到窗口')
    rect = win32gui.GetWindowRect(handle)

    app_head: tuple = (rect[0], rect[1])
    app_tail: tuple = (rect[2], rect[3])
    app_width: int = rect[2] - rect[0]
    app_height: int = rect[3] - rect[1]
    logger.info(f'起点坐标：{app_head}，终点坐标：{app_tail}')
    logger.info(f'宽：{app_width}，高：{app_height}')

    return handle, app_head, app_tail, app_width, app_height
