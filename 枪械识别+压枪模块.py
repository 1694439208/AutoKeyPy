import os
import time
import cv2
import numpy as np

'''
#按键映射用法
import hmbb
import time
from tool import *
def main(arg):
    try:
        if arg[2]:
            #按下
            hmbb.down(20,arg[0],arg[1])
            time.sleep(30/1000)
            get_weapon()
        else:
            hmbb.up(20,arg[0],arg[1])
    except Exception as e:
        print(f"外部捕获到异常：{e}")

'''
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
    #ret, binary_image = cv2.threshold(cropped_image, 127, 255, cv2.THRESH_BINARY_INV)
    #cv2.imwrite(output_path, cropped_image)
    return cropped_image
def read_image_chinese_path(image_path):
    """
    读取中文路径的图像
    :param image_path: 图像路径（支持中文）
    :return: 图像（OpenCV格式）
    """
    # 以二进制模式读取文件
    with open(image_path, 'rb') as f:
        image_bytes = f.read()

    # 将字节流解码为图像
    image = cv2.imdecode(np.frombuffer(image_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)
    return image

class ImageMatcher:
    def __init__(self, feature_detector='SIFT', match_threshold=0.7):
        """
        初始化图像匹配器
        :param feature_detector: 特征检测器类型，可选 'ORB', 'SIFT', 'SURF'
        :param match_threshold: 匹配阈值，用于筛选优质匹配点
        """
        self.feature_detector = feature_detector
        self.match_threshold = match_threshold

        # 初始化特征检测器
        if self.feature_detector == 'ORB':
            self.detector = cv2.ORB_create()
        elif self.feature_detector == 'SIFT':
            self.detector = cv2.SIFT_create()
        elif self.feature_detector == 'SURF':
            self.detector = cv2.xfeatures2d.SURF_create()
        else:
            raise ValueError("Unsupported feature detector. Choose from 'ORB', 'SIFT', 'SURF'.")

        # 初始化匹配器
        if self.feature_detector == 'ORB':
            self.matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        else:
            FLANN_INDEX_KDTREE = 1
            index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
            search_params = dict(checks=50)
            self.matcher = cv2.FlannBasedMatcher(index_params, search_params)

    def extract_features(self, image):
        """
        提取图像的特征点和描述符
        :param image: 输入图像（灰度图）
        :return: 关键点, 描述符
        """
        # 如果图像是彩色图，转换为灰度图
        if len(image.shape) == 3:  # 彩色图有3个通道
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray_image = image  # 已经是灰度图
        keypoints, descriptors = self.detector.detectAndCompute(gray_image, None)
        return keypoints, descriptors

    def match_images(self, descriptors1, descriptors2):
        """
        匹配两幅图像的描述符
        :param descriptors1: 第一幅图像的描述符
        :param descriptors2: 第二幅图像的描述符
        :return: 匹配点数量
        """
        if self.feature_detector == 'ORB':
            matches = self.matcher.match(descriptors1, descriptors2)
            return len(matches)
        else:
            matches = self.matcher.knnMatch(descriptors1, descriptors2, k=2)
            good_matches = [m for m, n in matches if m.distance < self.match_threshold * n.distance]
            return len(good_matches)

    def find_most_similar_folder(self, query_image, dataset_path):

        """
        在指定数据集中查找与查询图像最相似的文件夹
        :param query_image: 查询图像（OpenCV格式，灰度图）
        :param dataset_path: 数据集的根路径
        :return: 最相似的文件夹名称, 匹配点数量
        """
        # 提取查询图像的特征
        query_keypoints, query_descriptors = self.extract_features(query_image)

        if query_descriptors is None:
            raise ValueError("No features detected in the query image.")

        # 遍历数据集中的所有文件夹
        max_matches = 0
        best_folder = None

        

        for folder_name in os.listdir(dataset_path):
            #print(f"folder_name:{folder_name}")
            folder_path = os.path.join(dataset_path, folder_name)
            if not os.path.isdir(folder_path):
                continue

            total_matches = 0


            # 遍历文件夹中的所有图片
            for image_name in os.listdir(folder_path):
                image_path = os.path.join(folder_path, image_name)
                if not image_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                    continue

                

                # 读取图像并提取特征
                image = read_image_chinese_path(image_path)
                keypoints, descriptors = self.extract_features(image)

                if descriptors is None:
                    continue

                # 匹配特征
                matches = self.match_images(query_descriptors, descriptors)
                total_matches += matches

            # 更新最佳匹配文件夹
            if total_matches > max_matches:
                max_matches = total_matches
                best_folder = folder_name

        return best_folder, max_matches
def click(arg,timems):
    import hmbb
    hmbb.down(20,arg[0],arg[1])
    time.sleep(timems/1000)
    hmbb.up(20,arg[0],arg[1])
def get_weapon():
    import hmbb
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
    
    
    当前武器 = None
    if distance < 70:  # 距离越小，颜色越接近
            print('选择武器1')
            # 武器1的区域坐标
            top_left = (0.39480280103092624 * w, 0.851115770099863 * h)
            bottom_right = (0.4960355784058356 * w, 0.9182521199465411 * h)
            当前武器 = crop_and_save(image, top_left, bottom_right, "weapon1.jpg")
    elif distance2 < 70:  # 距离越小，颜色越接近
        print('选择武器2')
        # 武器2的区域坐标
        top_left = (0.5028281363310187 * w, 0.8524379805052806 * h)
        bottom_right = (0.603480783176559 * w, 0.9182832467010613 * h)
        当前武器 = crop_and_save(image, top_left, bottom_right, "weapon2.jpg")
    else:
        print('未检测到武器')
        
    # 初始化图像匹配器
    matcher = ImageMatcher(feature_detector='SIFT')

    # 读取查询图像（OpenCV格式）
    query_image = 当前武器

    # 数据集路径
    dataset_path = r"识图"

    # 查找最相似的文件夹
    best_folder, max_matches = matcher.find_most_similar_folder(query_image, dataset_path)
    print(f"当前手持枪械是: {best_folder}, 匹配点数量: {max_matches}")
  
# 示例用法
if __name__ == "__main__":
    # 初始化图像匹配器
    matcher = ImageMatcher(feature_detector='SIFT')

    # 读取查询图像（OpenCV格式）
    query_image = cv2.imread(r"2.jpg", cv2.IMREAD_GRAYSCALE)
    print(query_image)
    # 数据集路径
    dataset_path = r"识图"

    # 查找最相似的文件夹
    best_folder, max_matches = matcher.find_most_similar_folder(query_image, dataset_path)
    print(f"最相似的枪械是: {best_folder}, 匹配点数量: {max_matches}")
