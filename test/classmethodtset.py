class A(object):

    def foo(self, x):
        print("executing foo(%s,%s)" % (self, x))
        print('self:', self)

    @classmethod
    def class_foo(cls, x):
        print("executing class_foo(%s,%s)" % (cls, x))
        print('cls:', cls)
        cls.static_foo(x)

    @staticmethod
    def static_foo(x):
        print("executing static_foo(%s)" % x)    

A.class_foo(1)