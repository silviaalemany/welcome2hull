import random
import math
import matplotlib.pyplot as plt
import numpy as np
import time

class Point:
    def __init__(self, X, Y):
        self.x, self.y = x, y

    def __eq__(a, b, epsilon):
        return (abs(a - b) <= epsilon)

    def generatePoints(n):
        points = []
        distinct = set()
        for i in range(n):
            point = Point(random.random(), random.random())
            if point in distinct: continue
            points.append(point)
        return points

    def reflex(u, v, w):
        return ((v.x - w.x)*(u.y - w.y) - (v.y - w.y)*(u.x - w.x)) <= 0

    def naiveHull(points):
        hullPoints = set()
        for i in range(len(points)):
            sign = 0
            for j in range(len(points)):
                if i == j:
                    continue
                guard = True
                for k in range(len(points)):
                    if i == k or k == j: continue
                    # if left is true, points[k] is either colinear with or "leftOf" the 
                    # line passing through points i and j on the plane
                    left = reflex(points[i], points[k], points[j])
                    if left: 
                        continue 
                    else:
                        guard = False
                        break
                if guard:
                    hullPoints.add(points[i])
                    hullPoints.add(points[j])
            
                    
        hull = list(hullPoints)
        #origin = min(hull, key = lambda v: (v.y, -v.x))
        #hull = sorted(hull, key = lambda v: angle(v, origin))
        return hull



    def dist(v, u):
        return math.sqrt(math.pow(v.x - u.x, 2) + math.pow(v.y - u.y, 2))


    def angle(v, u):
        # assuming distinct points, this is simply used to avoid divide by 0 errors when sorting
        # without taking time to remove our reference point
        if v == u: return float('-inf')
        cosine = (v.x - u.x)/math.sqrt(math.pow(v.x - u.x, 2) + math.pow(v.y - u.y, 2))
        # print(math.acos(cosine))
        return math.acos(cosine)


    def grahamHull(points):
        origin = min(points, key = lambda v: (v.y, -v.x))
        # sort by angle relative to an x axis passing thru reference point
        # use euclidean distance from ref as a tiebreaker (sorts in increasing order, hence the negative sign)
        points = sorted(points, key = lambda v: (angle(v, origin), -dist(v, origin)))
        angles = set()
        stack = []
        for point in points:
            cur = angle(point, origin)
            if cur in angles: 
                continue
            while len(stack) > 1 and reflex(point, stack[-1], stack[-2]):
                print(stack[-1])
                stack.pop()
            stack.append(point)
            angles.add(cur)
        return stack

    # plotting
    def diff(list1, list2):
        c = set(list1).union(set(list2))  
        d = set(list1).intersection(set(list2)) 
        return list(c - d)

    data = generatePoints(10000)
    hull = naiveHull(data)
    points = diff(data, hull)
    hull.append(hull[0])
    xHull, yHull = (np.array(hull)).T
    print(len(hull))
    print(len(data))

    fig, ax = plt.subplots()
    ax.plot(xHull, yHull, c='b')

    x, y = (np.array(data)).T
    ax.scatter(x, y, c='k', s=0.75)
    plt.legend()

    plt.show()