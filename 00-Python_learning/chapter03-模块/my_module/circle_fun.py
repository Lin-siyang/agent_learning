__all__ = ['circle_area']#控制 import * 时导入哪些功能



#根据半径计算圆的面积
def circle_area(radius):
    area = 3.14 * radius * radius
    return area


#根据半径计算圆的周长
def circle_len(r):
    return 2 * 3.14 * r

#测试函数
# __name__ : Python中的内置变量，表示当前的模块名（直接运行当前模块，__name__的值为"__main__"）
# 当该模块被导入时，__name__的值为模块名（这里即circle_fun）
# 执行当前文件则会执行如下代码；如果被当做模块导入，则不会执行
if __name__ == '__main__':
    print("-"*50)