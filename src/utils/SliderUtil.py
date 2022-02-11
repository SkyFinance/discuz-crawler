'''
Author: Yaaprogrammer
Date: 2022-01-27 18:26:33
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-04 20:46:04
Description: 滑块计算工具类

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''

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
    def GenerateTracks(distance: int) -> dict:
        """生成轨迹列表

        Args:
            distance (int): 缺口与起点的距离

        Returns:
            dict: "forward_tracks":list,"back_tracks":list
        """
        distance += 20
        v = 0
        t = 0.2
        forwardTracks = []
        current = 0
        mid = distance * 3 / 5
        while current < distance:
            if current < mid:
                a = 2
            else:
                a = -3
            s = v * t + 0.5 * a * (t**2)
            v = v + a * t
            current += s
            forwardTracks.append(round(s))
        backTracks = [-3, -3, -2, -2, -2, -2, -2, -1, -1, -1]
        return {'forward_tracks': forwardTracks, 'back_tracks': backTracks}

    def __ease_out_expo(sep):
        if sep == 1:
            return 1
        else:
            return 1 - pow(2, -10 * sep)

    @staticmethod
    def GenerateTrack(distance: int) -> list:
        def __easeOutExpo(sep):
            if sep == 1:
                return 1
            else:
                return 1 - pow(2, -10 * sep)
        slideTrack = []
        count = 30 + int(distance / 2)
        _x = 0
        for i in range(count):
            x = round(__easeOutExpo(i / count) * distance)
            if x == _x:
                continue
            slideTrack.append(x - _x)
            _x = x
        return slideTrack
