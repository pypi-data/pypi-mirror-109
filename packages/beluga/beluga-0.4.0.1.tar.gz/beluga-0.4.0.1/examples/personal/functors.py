from beluga.symbolic.data_classes import GenericFunctor

class Fadd1(GenericFunctor):
    def transformation(self, x):
        return x+1

add1 = Fadd1()

times2 = GenericFunctor()
times2.strrep = 'times2'

def ftimes2(self, x):
    return x*2

times2.set_transformation(ftimes2)

class Fadd3(GenericFunctor):
    def transformation(self, x):
        return x+3

add3 = Fadd3()

add5 = GenericFunctor(5)
add5.strrep = 'addsomething'

add5.set_transformation(lambda self, x: x + self.data)

add10 = GenericFunctor(5)
add10.strrep = 'addsomething'

add10.set_transformation(lambda self, x: x + 2*self.data)

mapper1 = add10 * add5 * add5

print((add1 * times2)(3))

print((add1**6)(5))
