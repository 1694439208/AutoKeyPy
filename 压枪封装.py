
import threading
import hmbb
import time
import logging

# 配置日志格式
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(threadName)s - %(message)s')

# 武器配置字典
WEAPON_CONFIG = {
    'AK': {
        'recoil_down_step': 30,
        'recoil_motton_param1': 2,
        'recoil_sleep_time': 0.02,  
        'fire_rate': 30, 
    },
    'M4': {
        'recoil_down_step': 15, 
        'recoil_motton_param1': 1,
        'recoil_sleep_time': 0.04,  
        'fire_rate': 50,  
    },
}

# RecoilManager 类
class RecoilManager:
    def __init__(self):
        self.weapon_params = None
        self.recoil_thread = None
        self.fire_thread = None
        self.stop_event = threading.Event()
        self.lock = threading.Lock()

    def _get_weapon_params(self, weapon):
        return WEAPON_CONFIG.get(weapon, WEAPON_CONFIG['AK'])
    
    def start_recoil(self, weapon='AK', arg=None):
        """ 开始压枪和射击 """
        if not arg:
            arg = [0, 0, True]
        with self.lock:
            if self.recoil_thread and self.recoil_thread.is_alive():
                logging.warning("压枪和射击线程已经在运行。")
                return
            self.weapon_params = self._get_weapon_params(weapon)
            self.stop_event.clear()
            logging.info(f'开始压枪 - 武器: {weapon}, 参数: {arg}')

            # 初始化线程
            self.recoil_thread = threading.Thread(
                target=self._recoil_control,
                name=f"recoil_control_{weapon}"
            )
            self.fire_thread = threading.Thread(
                target=self._fire_control,
                name=f"fire_control_{weapon}"
            )

            # 启动线程
            self.recoil_thread.start()
            self.fire_thread.start()
    
    def stop_recoil(self, weapon='AK', arg=None):
        """ 停止压枪和射击 """
        if not arg:
            arg = [0, 0, False]
        with self.lock:
            if not self.recoil_thread or not self.recoil_thread.is_alive():
                logging.warning("压枪和射击线程未在运行。")
                return
            logging.info(f'停止压枪 - 武器: {weapon}, 参数: {arg}')
            self.stop_event.set()

            # 等待线程结束
            self.recoil_thread.join()
            self.fire_thread.join()
            logging.info("压枪和射击线程已停止。")
    
    def _recoil_control(self):
        """ 压枪控制线程逻辑 """
        try:
            while not self.stop_event.is_set():
                hmbb.motton(hmbb.get_mouseId(),0, self.weapon_params['recoil_motton_param1'])
                time.sleep(self.weapon_params['recoil_sleep_time'])
                logging.debug("压枪中...")
        except Exception as e:
            logging.error(f"压枪控制线程发生错误: {e}")
            self.stop_event.set()

    def _fire_control(self):
        """ 射速控制线程逻辑 """
        try:
            while not self.stop_event.is_set():
                if hasattr(hmbb, 'fire'):
                    hmbb.fire()
                    logging.debug("射击一次")
                time.sleep(1.0 / self.weapon_params['fire_rate'])
        except Exception as e:
            logging.error(f"射速控制线程发生错误: {e}")
            self.stop_event.set()

# 提供全局实例
recoil_manager = RecoilManager()

# 封装调用函数
def start_recoil(weapon='AK', x=0, y=0):
    """ 开始压枪和射击 """
    recoil_manager.start_recoil(weapon=weapon, arg=[x, y, True])

def stop_recoil(weapon='AK', x=0, y=0):
    """ 停止压枪和射击 """
    recoil_manager.stop_recoil(weapon=weapon, arg=[x, y, False])
# 测试主函数
if __name__ == "__main__":
    try:
        print("开始测试...")
        start_recoil(weapon='AK', x=10, y=20)
        time.sleep(5)  # 模拟按压 5 秒
        stop_recoil(weapon='AK', x=10, y=20)

        start_recoil(weapon='M4', x=15, y=25)
        time.sleep(5)  # 模拟按压 5 秒
        stop_recoil(weapon='M4', x=15, y=25)

        print("测试完成。")
    except KeyboardInterrupt:
        stop_recoil()
        print("程序被用户终止。")
'''
#简单用法
def main(arg):
    if arg[2]:
        start_recoil(weapon='AK', x=10, y=20)
        hmbb.down(120,arg[0],arg[1])
    else:
        stop_recoil(weapon='AK', x=10, y=20)
        hmbb.up(120,arg[0],arg[1])
'''

