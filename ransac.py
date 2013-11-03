#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import math
import random
import copy
# import numpy as np
import matplotlib.pyplot as plt

def create_test_data(n=100, gradient=1):
    data = []
    for i in range(n/2):
        x = random.random()
        y = (gradient-random.random()/10) * x
        data.append([x, y])
    for i in range(n/4):
        x = random.random()
        y = random.random()
        data.append([x, y])
    for i in range(n/4):
        x = random.uniform(0.9, 1.0)
        y = random.uniform(0.0, 0.1)
        data.append([x, y])
    return data

def random_choice_unique(list, n=2):
    choices = []
    for i in range(n):
        choice = random.choice(list)
        choices.append(choice)
        list.remove(choice)
    return choices

# parameter estimation
# y = ax
def estimation(points):
    transposed = map(list, zip(*points))
    avg = map(lambda x:sum(x)/len(x), transposed)
    param = avg[1]/avg[0]
    return param

# parameter evaluation
# y = ax
def evaluation(points, param):
    a = param 
    count = 0
    for x, y in points:
        dist = abs((y-a*x) / math.sqrt(1+a**2))
        if dist < 0.01:
            count += 1
    return count

# k: iteration
def ransac(data, m, k):
    prev_eval = 0
    estimated_param = 0
    for i in range(k):
        remains = copy.copy(data)
        n_points = random_choice_unique(remains, m)
        param = estimation(n_points)
        eval = evaluation(remains, param)
        if eval > prev_eval:
            prev_eval = eval
            estimated_param = param
    return estimated_param
    

if __name__ == '__main__':
    u = 1000
    k = 20
    m = 2

    grad = random.uniform(0.25, 1.75)
    data = create_test_data(u, grad)

    param = ransac(data, m, k)
    print 'grad: ', grad
    print 'param: ', param

    # plot
    # sample data
    plt.hold(True)
    plt.axis([0, 1, 0, 1])
    x, y = map(list, zip(*data))
    plt.scatter(x, y, s=1)
    # estimated parameter
    x, y = map(list, zip(*([[0, 0], [1, param]])))
    plt.plot(x, y, 'r')
    plt.show()
    

    
