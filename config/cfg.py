# coding: utf-8
#!/usr/bin/python
import os

# dll文件
_config_path = os.path.dirname(__file__)
_idx = _config_path.rfind(os.sep)
MY_DLL = os.path.join(_config_path[:_idx], 'dll', 'msdk_32.dll')

# 电脑的分辨率，主要用于鼠标移动判定
WIDTH, HEIGHT = 1920, 1080

# 每日任务的快捷键，可根据自己游戏的按键设置来修改
TASK_KEY = 'f8'

# 应用title
APP_TITLE = '地下城与勇士：创新世纪'

from airtest.core.settings import Settings as ST
# ST.THRESHOLD = 0.5  # 识别图片默认阈值

