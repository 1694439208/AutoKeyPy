import threading
import hmbb
import time
def main(arg):
    try:
        if arg[2]:
            #按下
            hmbb.down(20,arg[0],arg[1])
            time.sleep(30/1000)
            hmbb.up(20,arg[0],arg[1])
            
            x,y = 0.44597534445250187,0.821759447445182
            hmbb.down(20,x,y)
            time.sleep(30/1000)
            hmbb.up(20,x,y)
            print(f'按下-参数:{arg}')
        else:
            #松开
            print(f'松开-参数:{arg}')
    except Exception as e:
        print(f"外部捕获到异常：{e}")
