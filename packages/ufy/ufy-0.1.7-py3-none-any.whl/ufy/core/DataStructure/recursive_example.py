# -*- coding: utf-8 -*-
# @Time     : 2021/6/3 17:34
# @Author   : ufy
# @Email    : antarm@outlook.com / 549147808@qq.com
# @file     : recursive_example.py
# @info     :
import os.path


class EnglishRuler:
    def draw_line(self, tick_length, tick_label=''):
        """Draw one line with given tick length (followed by optional label)."""
        line = '-' * tick_length
        if tick_label:
            line += '  ' + tick_label
        print(line)

    def draw_interval(self, center_length):
        """Draw tick interval based upon a central tick length."""
        if center_length > 0:
            self.draw_interval(center_length - 1)
            self.draw_line(center_length)
            self.draw_interval(center_length - 1)

    def draw_ruler(self, num_inches, major_length):
        """Draw English ruler with given number of inches, major tick length"""
        self.draw_line(major_length, '0')
        for j in range(1, 1 + num_inches):
            self.draw_interval(major_length - 1)
            self.draw_line(major_length, str(j))


class Search:
    def __init__(self, data):
        self._data = data
        print(self._data[:10])

    def binary_search(self, target, low, high):
        if low > high:
            return False, -1
        else:
            mid = (low + high) // 2
            if target == self._data[mid]:
                return True, target
            elif target < self._data[mid]:
                return self.binary_search(target, low, mid - 1)
            else:
                return self.binary_search(target, mid + 1, high)


class FileSystem:
    def disk_usage(self, path):
        total = os.path.getsize(path)
        if os.path.isdir(path):
            for filename in os.listdir(path):
                childpath = os.path.join(path, filename)
                total += self.disk_usage(childpath)

        print('{0:<10}'.format(total), path)
        return total


if __name__ == '__main__':
    # english_ruler = EnglishRuler()
    # english_ruler.draw_ruler(3, 5)

    # search = Search([i for i in range(10000)])
    # print(search.binary_search(500, 0, 10000))

    fs = FileSystem()
    print(os.path.abspath(os.path.curdir))
    fs.disk_usage(os.path.curdir)
