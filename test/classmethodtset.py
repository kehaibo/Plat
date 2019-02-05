class A(object):

    xin = 1
    def __init__(self,a):
        a = a
        a=1

    def foo(self, x):
        print("executing foo(%s,%s)" % (self, x))
        print('self:', self)
        print(xin)

    @classmethod
    def class_foo(cls, x):
        print("executing class_foo(%s,%s)" % (cls, x))
        print('cls:', cls)
        print('cls.xin:',cls.xin)
        cls.static_foo(x)

    @staticmethod
    def static_foo(x):
        print("executing static_foo(%s)" % x)    

#A.class_foo(1)
a = 0
aobj = A(a)
print(a)