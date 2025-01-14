import threading
import hmbb
import time

ya = False
#按下调用
def main(arg):
    global ya
    if arg[2]:
        #按下
        ya = True
        print(f'按下-参数:{arg}')
        hmbb.down(120,arg[0],arg[1])
        while ya:
          hmbb.motton(hmbb.get_mouseId(),0,1) #每次压枪 x不动，y压1像素
          time.sleep(50/1000) #压枪间隔50ms
          print(f'压枪00中.')
        print(f'压枪完毕.')
    else:
        #松开
        ya = False
        print(f'松开-参数:{arg}，停止压枪')
        hmbb.up(120,arg[0],arg[1])
