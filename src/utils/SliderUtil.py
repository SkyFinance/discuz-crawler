'''
Author: Yaaprogrammer
Date: 2022-01-27 18:26:33
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-22 20:37:36
Description: 滑块计算工具类

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''

import random

from PIL.Image import Image


class SliderUtil:

    @staticmethod
    def GetDistance(bgImage: Image, fullbgImage: Image) -> int:
        """获取缺口与起点的距离

        Args:
            bgImage (Image): 缺口图
            fullbgImage (Image): 全背景图

        Returns:
            int: 距离
        """
        distance = 60
        for i in range(distance, fullbgImage.size[0]):
            for j in range(fullbgImage.size[1]):
                if (not SliderUtil.isPixelEqual(fullbgImage, bgImage, i, j)):
                    distance = i
                    return distance - 5
        return distance

    @staticmethod
    def isPixelEqual(bgImage: Image, fullbgImage: Image, x: int,
                     y: int) -> bool:
        """判断像素是否相等,有一定阈值

        Args:
            bgImage (Image): 缺口图
            fullbgImage (Image): 全背景图
            x (int): x像素
            y (int): y像素

        Returns:
            bool: 是否相等
        """
        bgPixel = bgImage.load()[x, y]
        fullbgPixel = fullbgImage.load()[x, y]
        threshold = 60
        for i in range(0, 3):
            if (abs(bgPixel[i] - fullbgPixel[i] < threshold)):
                return True
        return False

    @staticmethod
    def GenerateTrack(distance):
        """
        根据偏移量和手动操作模拟计算移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        """
        # 移动轨迹
        tracks = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 时间间隔
        t = 0.2
        # 初始速度
        v = 0

        while current < distance:
            if current < mid:
                a = random.uniform(2, 5)
            else:
                a = -(random.uniform(12.5, 13.5))
            v0 = v
            v = v0 + a * t
            x = v0 * t + 1 / 2 * a * t * t
            current += x

            if 0.6 < current - distance < 1:
                x = x - 0.53
                tracks.append(round(x, 2))

            elif 1 < current - distance < 1.5:
                x = x - 1.4
                tracks.append(round(x, 2))
            elif 1.5 < current - distance < 3:
                x = x - 1.8
                tracks.append(round(x, 2))

            else:
                tracks.append(round(x, 2))

        print(sum(tracks))
        return tracks
