from random import uniform
from math import radians,cos,sin,sqrt,exp
import operator
from FunctionalSet.SymbolicRegression.FunctionWrapper import Funwrapper
from EvoAlgs.GP.GPbase import GP_base
class Problem():
    def __init__(self,sample_size_training, bounds_training,sample_size_test, bounds_test):
        self.sample_size_training=sample_size_training
        self.bounds_training=bounds_training
        self.sample_size_test=sample_size_test
        self.bounds_test=bounds_test
        self.addwrapper = Funwrapper(operator.add, 2, "Add")
        self.subwrapper = Funwrapper(operator.sub, 2, "Sub")
        self.mulwrapper = Funwrapper(operator.mul, 2, "Mul")
        self.divwrapper = Funwrapper(self.Div, 2, "Div")
        self.sinwrapper = Funwrapper(self.sinx, 1, "Sin")
        self.coswrapper = Funwrapper(self.cosx, 1, "Cos")
        self.expwrapper = Funwrapper(exp, 1, "Exp")
        self.parabwrapper = Funwrapper(self.parab, 1, "X^2")
        self.abswrapper = Funwrapper(abs, 1, "Abs")
        self.minuswrapper = Funwrapper(self.minus, 1, "Minus")
        self.sqrtwrapper = Funwrapper(self.sqrtx, 1, "Sqrt")

    def add(self, ValuesList):
        sumtotal = 0
        for val in ValuesList:
            sumtotal = sumtotal + val
        return sumtotal

    def sub(self, ValuesList):
        return ValuesList[0] - ValuesList[1]

    def mul(self, ValuesList):
        return ValuesList[0] * ValuesList[1]

    def div(self, ValuesList):
        if ValuesList[1] == 0:
            return 1
        return ValuesList[0] / ValuesList[1]

    def Div(self, a, b):
        if b == 0:
            return 1
        return a / b

    def sinx(self, a):
        xx = radians(a)
        if xx == float('inf'):
            return xx
        else:
            return sin(xx)

    def cosx(self, a):
        with open('a.txt', 'w') as out:
            out.write('{}\n'.format(a))
        xx = radians(a)
        if xx == float('inf'):
            return xx
        else:
            return cos(xx)

    def parab(self, a):
        return a ** 2

    def minus(self, a):
        return -a

    def sqrtx(self, a):
        if a < 0:
            return float('inf')
        elif a == float('inf'):
            return a
        else:
            return sqrt(a)

    def examplefun(self, *args):
        return args[0]**3 + 4 * args[1] + 8 * args[2] + 1

    def constructcheckdata(self, num_of_variables, bounds, sample_size=300):
        generated_samples = []
        for i in range(sample_size):
            one_example={}
            for j in range(num_of_variables):
                one_example[f'x{j+1}']=uniform(bounds[0], bounds[1])
            one_example['result'] = self.examplefun(*one_example.values())
            generated_samples.append(one_example)
        return generated_samples

    def samples_generation(self):
        checkdata = self.constructcheckdata(num_of_variables=3,bounds=self.bounds_training,sample_size=self.sample_size_training)
        checkdataforbesttree = self.constructcheckdata(num_of_variables=3,bounds=self.bounds_test,sample_size=self.sample_size_test)
        return checkdata,checkdataforbesttree

    def run_experement(self):
        training_sample,test_sample=self.samples_generation()
        constantarray = [uniform(0, 10) for i in range(1, 10)]

        launches = 30
        res = []
        percent = 100
        averagenum_of_generation = 0
        averagenum_len = 0

        for i in range(0, launches):
            env = GP_base([self.mulwrapper, self.addwrapper, self.parabwrapper, self.subwrapper], ["x1", "x2", "x3"],
                             constantarray, training_sample, test_sample, percent)

            returnedvalues = env.evolution()
            print("returnedvalues\n", returnedvalues)

            percent = returnedvalues[0] * 100
            if returnedvalues[1] != None:
                averagenum_of_generation += returnedvalues[1]
                averagenum_len += 1
            if percent <= 1:
                res.append(percent)
            # res.append(env.envolve()*100)
            print("launch number:\n",i)
            print("res:\n",res)

        print("RES\n",res)
        print("reslen\n",len(res))
        averagenum_of_generation = averagenum_of_generation / averagenum_len
        print("average num of generation\n",averagenum_of_generation)