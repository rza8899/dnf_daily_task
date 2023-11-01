# coding: utf-8
# !/usr/bin/python
from utils.base import *


common_path = 'imgs/{}_{}/{}'.format(b.app_width, b.app_height, '{}')

chat1_path = common_path.format('chat1.png') # 普通或者频道聊天任务
chat2_path = common_path.format('chat2.png') # 公会聊天任务
no_money_path = common_path.format('no_money.png')
refresh_path = common_path.format('refresh.png')
take_reward_path = common_path.format('take_reward.png')
select_role_path = common_path.format('select_role.png')
start_game_path = common_path.format('start_game.png')


def find_chat_img(times: int=2) -> int:
    """
    统计聊天任务的数量，包括普通聊天和工会聊天任务
    :param times:
    :return:
    """
    no_money = b.find_img(no_money_path, times=times)
    # 提示金币不足时，返回-1
    if no_money:
        b.press_key('esc')
        return -1
    chat1 = b.find_img(chat1_path, times=times)
    chat2 = b.find_img(chat2_path, times=times)
    chat_count = len(chat1) + len(chat2)
    return chat_count


def refresh_daily_task(refresh_abs_pos: Tuple[int, int], target: int, times: int=50) -> int:
    """
    刷新日常任务
    :param refresh_abs_pos: 刷新按钮的绝对坐标
    :param target: 预计找到几个刷新按钮
    :param times: 刷新次数
    :return:
    """
    if target < 0:
        raise Exception('目标值不能小于0')
    for _ in range(times):
        b.click_left(refresh_abs_pos)
        b.press_key('space')
        time.sleep(0.8)
        chat_count = find_chat_img()
        # 如果为-1，表示金币不足，如果等于目标值，就正常返回
        if chat_count == -1 or chat_count == target:
            return chat_count
    # 循环{times}次，未匹配，返回异常
    return -9999


def switch_role() -> None:
    """
    切换当前角色右边的一个角色
    :return:
    """
    time.sleep(1)
    b.press_key('esc')
    select_role_info = b.find_img(select_role_path)
    if len(select_role_info) != 1:
        raise Exception('未找到选择角色按钮')
    select_role_abs_pos = b.get_abs_pos(select_role_info)
    select_role_abs_pos = select_role_abs_pos[0]
    b.click_left(select_role_abs_pos)

    # 进入选择角色界面
    time.sleep(1)
    start_game_info = b.find_img(start_game_path)
    if len(start_game_info) != 1:
        raise Exception('进入选择角色界面失败')
    b.press_key('right')
    time.sleep(0.5)
    b.press_key('space')
    time.sleep(2)


def daily_task(refresh_times: int) -> None:
    """
    日常任务
    :param refresh_times: 刷新次数
    :return:
    """
    # m键为日常任务列表快捷键
    b.press_key(TASK_KEY)
    # 找刷新按钮
    btns: list = b.find_img(refresh_path)
    if len(btns) != 3:
        raise Exception('未找到刷新按钮')
    btns_abs_pos: list = b.get_abs_pos(btns)
    # 排序，根据y坐标从小到大排序，从上到下
    btns_abs_pos.sort(key=lambda x: x[1])
    # 第一个和第二个任务是杀怪任务，找到聊天任务>1，说明玩家刷新过任务，可能手动完成了任务，跳过该角色
    chat_count = find_chat_img()
    if chat_count > 1:
        b.press_key('esc')
        return

    # {chat_count}为0说明第三个每日任务不是聊天任务，刷新它
    if chat_count == 0:
        btn_abs_pos = btns_abs_pos[2]
        refresh_result = refresh_daily_task(btn_abs_pos, 1, refresh_times)
        # 如果刷新{refresh_times}次，还没完成，跳过后续的流程，切换角色
        if refresh_result < 0:
            b.press_key('esc')
            return

    # 刷新第一个任务
    btn_abs_pos = btns_abs_pos[0]
    refresh_result = refresh_daily_task(btn_abs_pos, 2, refresh_times)
    # 如果刷新{refresh_times}次，还没完成，切换角色
    if refresh_result != 2:
        b.press_key('esc')
        return

    # 刷新第二个任务
    btn_abs_pos = btns_abs_pos[1]
    refresh_result = refresh_daily_task(btn_abs_pos, 3, refresh_times)
    # 如果刷新{refresh_times}次，还没完成，切换角色
    if refresh_result != 3:
        b.press_key('esc')
        return

    # /a切换普通聊天，输入两次1
    time.sleep(2)
    chat_keys = ['enter', '/', 'a', 'space', '1', 'enter', 'enter', '1', 'enter']
    for item_key in chat_keys:
        b.press_key(item_key)

    # /g切换公会聊天，输入两次1
    time.sleep(5)
    chat_keys = ['enter', '/', 'g', 'space', '1', 'enter', 'enter', '1', 'enter']
    for item_key in chat_keys:
        b.press_key(item_key)

    # 领取奖励
    time.sleep(1)
    rewards = b.find_img(take_reward_path)
    rewards_abs_pos = b.get_abs_pos(rewards)
    # 页面会找到所有的领取按钮，包括周常任务，全部点击一遍。
    for reward_pos in rewards_abs_pos:
        b.click_left(reward_pos)
    time.sleep(1)
    # 领取完成后esc关闭界面
    b.press_key('esc')
