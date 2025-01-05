import threading
import hmbb
import time

#创建一个喜欢的按键映射，开启全局绑定，把这段代码复制进去即可，想绑定任何键都可以  hmbb.relativeMouseMode()
def main(arg):
    try:
        if arg[2]:
            #按下
            hmbb.relativeMouseMode()
            print(f'按下-参数:{arg}')
        else:
            #松开
            print(f'松开-参数:{arg}')
    except Exception as e:
        print(f"外部捕获到异常：{e}")
