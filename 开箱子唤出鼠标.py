
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

def main(arg):
    try:
        if arg[2]:
            #按下
            print(f'按下-参数:{arg}')
            #按下开箱子
            hmbb.down(20,arg[0],arg[1])
            time.sleep(30/1000)
            hmbb.up(20,arg[0],arg[1])
            time.sleep(30/1000)
            
            #鼠标脱离
            hmbb.relativeMouseMode()
            time.sleep(50/1000)
            #鼠标移动到屏幕中心
            set_mouse_to_center()
        else:
            #松开
            print(f'松开-参数:{arg}')
    except Exception as e:
        print(f"外部捕获到异常：{e}")
