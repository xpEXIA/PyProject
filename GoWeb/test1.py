# 测试文件
# homework



# wogalsjdkjansd;cn;sav

# def asd(z):
#     print('asd')
#     def qwe(a_func):
#         print('qwe')
#         def zxc(x,y):
#             print('zxc')
#             a = a_func(x,y) + z
#             return a
#         return zxc
#     return qwe
#
# @asd(z=3)
# def add(x,y):
#     return x + y


class test():

    def __init__(self,a,b=2):

        self.a = a
        self.b = b

    def add(self):
        return  self.a +1

    def result(self):

        c = self.add() + self.b
        return c

    def add_one(self,a):

        return a + 1

    def arg(self,*args,**kwargs):

        h = 0
        for i in kwargs:
            h = h + kwargs[i]
        for i in args:
            h = h + i
        return h


if __name__ == '__main__':

    a = test(1)
    c = a.add()
    print(c)
    b = a.result()
    print(b)
    print(a.arg(5,8))