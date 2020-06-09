# 测试文件
# homework



# wogalsjdkjansd;cn;sav

def asd(z):
    print('asd')
    def qwe(a_func):
        print('qwe')
        def zxc(x,y):
            print('zxc')
            a = a_func(x,y) + z
            return a
        return zxc
    return qwe

@asd(z=3)
def add(x,y):
    return x + y


class test():

    def __init__(self,a):

        self.a = a

    def add(self):
        return super().add()

if __name__ == '__main__':

    print(add(x=1,y=2))
    print(add.__delattr__())