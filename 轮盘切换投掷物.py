import threading
import hmbb
import time
def main(arg):
    try:
        mouseid = hmbb.get_mouseId()
        if arg[2]:
            #首先松开视角
            hmbb.up(mouseid,arg[0],arg[1])
            time.sleep(30/1000)
            
            #移动到轮盘
            hmbb.move(mouseid,arg[0],arg[1])
            time.sleep(30/1000)
            #按下切雷
            hmbb.down(mouseid,arg[0],arg[1])
            time.sleep(30/1000)
            
        else:
            #松开
            print(f'松开-参数:{arg}')
            #松开投掷轮盘
            hmbb.up(mouseid,arg[0],arg[1])
            time.sleep(30/1000)
            #重置鼠标
            hmbb.resetCamera()
            
    except Exception as e:
        print(f"外部捕获到异常：{e}")
