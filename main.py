import random
import math
import matplotlib.pyplot as plt
import numpy as np
import time
import collections

class Point(object):
    # precision for comparing points
    err =  math.pow(10, -36)

    # creates point given x, y coords
    def __init__(self, x: float, y: float):
        self.x, self.y = x, y

    # override hash -- used for plotting
    def __hash__(self):
        return hash(hash(self.x) * hash(self.y))

    # override less than to compare to within specified precision
    def __lt__(self, other):
        return ((other.val - self.val) > err)

    # override equals to compare to within specified precision
    def __eq__(self, other):
        return (abs(self.x - other.x) <= self.err and abs(self.x - other.x) <= self.err)
    
    # leftOf function for naive implementation
    # (direction matters) takes a vector (u, v) and returns true if point is
    # on or left of line from u to v (direction matters)
    def leftOf(self, u, v):
        return (self.x - u.x)*(v.y - u.y) - (self.y - u.y)*(v.x - u.x) <= 0

    # override methods to print point data
    def __str__(self):
        return str((self.x, self.y))

    def __repr__(self):
        return str((self.x, self.y))


class Angle(object):
    # precision for comparing angles in hull algorithm implementation
    err =  math.pow(10, -36)
     
    # creates angle object with value attribute
    def __init__(self, val: float):
        self.val = val

    # override hash to keep track of points with duplicate angles in graham implementation
    def __hash__(self):
        return hash(self.val)

    # override less than for angular sort
    def __lt__(self, other):
        return ((other.val - self.val) > self.err)

    # override equals for angular sort/comparisons
    def __eq__(self, other):
        return (abs(self.val - other.val) <= self.err)
    

# find euclidean distance between points u, v
def dist(v, u):
    return math.sqrt(math.pow(v.x - u.x, 2) + math.pow(v.y - u.y, 2))

# find angle between points u, v
def angle(v, u):
    # assuming distinct points, this is simply used to avoid divide by 0 errors when sorting
    # without taking extra time to remove our reference point before sorting (which could be costly)
    if v == u: return Angle(float('-inf'))
    cosine = (v.x - u.x)/math.sqrt(math.pow(v.x - u.x, 2) + math.pow(v.y - u.y, 2))
    return Angle(math.acos(cosine))

# similar to leftOf but used for graham scan -- 
# given three points u, v, w to be processed by algorithm, determine whether v is reflex/collinear
# returns true if v is reflex/collinear
def reflex(u, v, w):
    return (v.x - w.x)*(u.y - w.y) - (v.y - w.y)*(u.x - w.x) <= 0

# generate n random points in range 0, 1
def randomPoints(n):
    points = []
    distinct = set()
    for i in range(n):
        point = Point(random.random(), random.random())
        # do not add point to list if it isn't unique
        if point in distinct: continue
        points.append(point)
        distinct.add(point)
    return points

# generate n points according to exponential dist
def expoPoints(n):
    return [Point(i, math.pow(2, i)) for i in range(n)]

# generate n points on perimeter of a unit circle
def circularPoints(n):
    return [Point(math.cos((2 * i * math.pi)/n), math.sin((2 * i * math.pi)/n)) for i in range(n)]

# naive hull implementation
def naiveHull(points):
    # use dictionary to store directed edges in order to efficiently output in ccw order
    edges = {}
    hull = []
    for i in range(len(points)):
        for j in range(len(points)):
            if i == j:
                continue
            guard = True
            for k in range(len(points)):
                if i == k or k == j: 
                    continue
                # if left is true, points[k] is either colinear with or "leftOf" the 
                # line passing through points i and j on the plane
                left = points[k].leftOf(points[i], points[j])
                if left:
                    continue
                else:
                    guard = False
                    break
            if guard:
                # if there is collinearity, this allows us to override an edge starting from points[i]
                # if the current edge we are processing is longer than the stored edge
                if points[i] in edges and dist(edges[points[i]], points[i]) > dist(points[j], points[i]):
                    continue
                edges[points[i]] = points[j]

    # start from an extreme point and pop entries from dictionary until a circuit is completed.
    point = min(points, key = lambda v: (v.y, -v.x))
    while edges and point in edges:
        hull.append(point)
        point = edges.pop(point)
    return hull

# graham scan implementation
def grahamHull(points):
    # identify lower right most point as a reference point
    origin = min(points, key = lambda v: (v.y, -v.x))
    # sort by angle relative to an x axis passing through ref point
    # use euclidean distance from ref as a tiebreaker (sorts in increasing order, hence the negative sign)
    points = sorted(points, key = lambda v: (angle(v, origin), -dist(v, origin)))
    visitedAngles = set()
    stack = []
    for point in points:
        # since we use euclid distance as a tie-breaker, the most extreme point
        # is processed before other points sharing its angle
        # checking if the angle has been "visited" saves us a bit of time/makes code less redundant
        cur = angle(point, origin)
        if cur in visitedAngles: 
            continue
        while len(stack) > 1 and reflex(point, stack[-1], stack[-2]):
            stack.pop()
        stack.append(point)
        visitedAngles.add(cur)
    return stack


