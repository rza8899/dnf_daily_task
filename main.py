# coding: utf-8
# !/usr/bin/python
from utils.api import *

# 角色数
roles = 20
# 每个任务刷新次数，超过N次没刷出喊话任务就切换下一个角色
refresh_times = 30


time.sleep(2)
for i in range(roles):
    logger.info(f'当前第{i + 1}个角色')
    time.sleep(2)
    # 刷新日常任务
    daily_task(refresh_times)
    # 切换角色
    switch_role()

