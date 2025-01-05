import hmbb
import time
import cv2
import numpy as np

# 示例：从 bytes 数据读取图片
def read_image_from_bytes(image_bytes):
    # 将 bytes 数据转换为 numpy 数组
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    # 解码图片
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return image
def crop_and_save(image, top_left, bottom_right, output_path):
    # 提取左上角和右下角的坐标
    x1, y1 = top_left
    x2, y2 = bottom_right
    # 裁剪图片
    cropped_image = image[int(y1):int(y2), int(x1):int(x2)]
    # 保存裁剪后的图片
    ret, binary_image = cv2.threshold(cropped_image, 127, 255, cv2.THRESH_BINARY_INV)
    cv2.imwrite(output_path, binary_image)
#触发脚本截图找色识别左右手持枪demo
def main(arg):
    try:
        if arg[2]:
            #按下
            print(f'按下-参数:{arg}')
            #读取当前帧图像
            image = read_image_from_bytes(hmbb.frame_Image())
            #读取当前游戏分辨率
            (w,h) = hmbb.get_frame_size()
        
            # 获取指定坐标的像素值
            主武器像素 = image[int(0.8513569913766914 * h),int(0.3953454545456859 * w)]
            副武器像素 = image[int(0.8513569913766914 * h),int(0.5029818181820497 * w)]
            target_color = np.array([7,230,247])
        
            # 计算像素值与目标颜色的欧氏距离
            distance = np.sqrt(np.sum((主武器像素 - target_color) ** 2))
            distance2 = np.sqrt(np.sum((副武器像素 - target_color) ** 2))
            
            if distance > 70:
                print(f'武器1')
                #取枪械1
                top_left = (0.39480280103092624 * w,0.851115770099863*h)  #自己用的话直接固定
                bottom_right = (0.4960355784058356 * w,0.9182521199465411 * h)
                crop_and_save(image,top_left,bottom_right,"1.jpg")
            if distance2 > 70:
                print(f'武器2')
                #取枪械2
                top_left = (0.5028281363310187 * w,0.8524379805052806*h)  #自己用的话直接固定
                bottom_right = (0.603480783176559 * w,0.9182832467010613 * h)
                crop_and_save(image,top_left,bottom_right,"2.jpg")
            print(f'鼠标坐标:{arg}')
        else:
            #松开
            print(f'松开-参数:{arg}')
    except Exception as e:
        print(f"外部捕获到异常：{e}")
