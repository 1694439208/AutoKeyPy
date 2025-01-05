import hmbb
import time
import cv2
import numpy as np
import os
from datetime import datetime

# 从 bytes 数据读取图片
def read_image_from_bytes(image_bytes):
    try:
        image_array = np.frombuffer(image_bytes, dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("解码图像失败")
        return image
    except Exception as e:
        print(f"读取图像失败: {e}")
        return None

# 裁剪并保存图像
def crop_and_save(image, top_left, bottom_right, output_dir, prefix="weapon"):
    try:
        x1, y1 = map(int, top_left)
        x2, y2 = map(int, bottom_right)
        cropped_image = image[y1:y2, x1:x2]
        if cropped_image.size == 0:
            raise ValueError("裁剪区域无效")

        # 二值化处理
        _, binary_image = cv2.threshold(cropped_image, 127, 255, cv2.THRESH_BINARY_INV)

        # 动态文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(output_dir, f"{prefix}_{timestamp}.jpg")
        cv2.imwrite(output_path, binary_image)
        print(f"保存裁剪图像: {output_path}")
    except Exception as e:
        print(f"裁剪或保存图像失败: {e}")

def main(arg, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)  # 创建输出目录
    target_color = np.array([7, 230, 247])  # 目标颜色
    tolerance = 70  # 容忍度

    try:
        if arg[2]:  # 按下事件
            print(f'按下-参数: {arg}')
            image = read_image_from_bytes(hmbb.frame_Image())
            if image is None:
                print("读取图像失败，跳过处理")
                return

            (w, h) = hmbb.get_frame_size()

            # 获取指定坐标的像素值
            主武器像素 = image[int(0.851 * h), int(0.395 * w)]
            副武器像素 = image[int(0.851 * h), int(0.503 * w)]

            # 计算欧氏距离
            distance = np.linalg.norm(主武器像素 - target_color)
            distance2 = np.linalg.norm(副武器像素 - target_color)

            # 判断武器状态
            if distance > tolerance:
                print("检测到主武器")
                crop_and_save(image, (0.395 * w, 0.851 * h), (0.496 * w, 0.918 * h), output_dir, prefix="main_weapon")
            if distance2 > tolerance:
                print("检测到副武器")
                crop_and_save(image, (0.503 * w, 0.852 * h), (0.603 * w, 0.918 * h), output_dir, prefix="secondary_weapon")

            print(f'鼠标坐标: {arg}')
        else:
            print(f'松开-参数: {arg}')
    except Exception as e:
        print(f"外部捕获到异常：{e}")

# 测试入口
if __name__ == "__main__":
    test_arg = [0, 0, True]
    main(test_arg)
