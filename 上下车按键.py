import threading
import hmbb
import time
import ctypes

def main(arg):
    try:
        if arg[2]:
            #按下
            print(f'按下-参数:{arg}')
            #按下开箱子
            hmbb.down(20,arg[0],arg[1])
            time.sleep(30/1000)
            hmbb.up(20,arg[0],arg[1])
            time.sleep(150/1000)
            
            #修复卡视角
            hmbb.resetCamera()
        else:
            #松开
            print(f'松开-参数:{arg}')
    except Exception as e:
        print(f"外部捕获到异常：{e}")
