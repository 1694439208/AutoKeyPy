import threading
import hmbb
import time
import ctypes

# 获取屏幕分辨率
def get_screen_resolution():
    width = ctypes.windll.user32.GetSystemMetrics(0)  # SM_CXSCREEN
    height = ctypes.windll.user32.GetSystemMetrics(1)  # SM_CYSCREEN
    return width, height

# 设置鼠标到屏幕中心
def set_mouse_to_center():
    # 获取屏幕分辨率
    width, height = get_screen_resolution()
    
    # 计算屏幕中心坐标
    center_x = width // 2
    center_y = height // 2
    
    # 设置鼠标位置
    ctypes.windll.user32.SetCursorPos(center_x, center_y)


# 设置鼠标到按键位置
def set_mouse_to_center(x,y):
    # 将按键归一化坐标转为桌面屏幕坐标
    center_x, center_y = hmbb.RelativeToScreen(x,y)
    # 设置鼠标位置
    ctypes.windll.user32.SetCursorPos(center_x, center_y)
