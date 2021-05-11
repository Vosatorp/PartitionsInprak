import re
import json
from math import atan2
import matplotlib.pyplot as plt

eps = 1e-4
v = lambda a, b: (b[0] - a[0], b[1] - a[1])
dist = lambda a, b: ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5
vect = lambda a, b: a[0] * b[1] - a[1] * b[0]
equal = lambda a, b: dist(a, b) < eps

def calc_hull(points):
    """
    Take numerated points in format (x, y, num)
    Return a hull as indexes
    And also bitmask (b1, b2, b3)
    b_i = 1 <==> hull[i] is vertex of hull
    b_i = 0 <==> hull[i] on the size of hull
    """
    M = min(points)
    was = [0] * len(points)
    hull = [M]
    bitm = [1]
    while 1:
        nxt = None
        lst = hull[-1]
        for p in points:
            if equal(p, lst) or was[p[2]]:
                continue
            if nxt is None:
                nxt = p
                continue
            vv = vect(v(lst, nxt), v(lst, p)) 
            if vv < -eps:
                nxt = p
            elif abs(vv) < eps and dist(lst, p) < dist(lst, nxt):
                nxt = p
        if nxt is None:
            break
        if len(hull) <= 1:
            bitm.append(1)
        else:
            vv = vect(v(hull[-2], lst), v(lst, nxt))
            if abs(vv) < eps:
                bitm.pop()
                bitm.append(0)
                bitm.append(1)
            else:
                bitm.append(1)       
        hull.append(nxt)
        was[nxt[2]] = 1
        if equal(nxt, M):
            hull.pop()
            bitm.pop()
            break         
    ind_hull = [ind for x, y, ind in hull]
    return ind_hull, bitm

def transform(file, title=None, shift=(0.5, 0.5)):

    def read():
        extracted = re.findall(r'\d+', input())
        return list(map(int, extracted))

    fin = open(file, 'r')
    input = fin.readline
    n = int(input())
    diam = float(input())
    m = int(input())
    regions = eval(input())
    p = eval(input())
    p = [(*i, ind) for ind, i in enumerate(p)]
    hull, bitmask = calc_hull(p.copy())
    print(hull)
    print(bitmask)
    for x, y, ind in p:
        plt.scatter(x, y, s=5)
    for i in range(len(hull)):
        x1, y1, _ = p[hull[i]]
        x2, y2, _ = p[hull[i - 1]]
        plt.plot([x1, x2], [y1, y2])
        if bitmask[i]:
            plt.scatter(x1, y1)
    plt.show()

    if title is None:
        title = ""

    data = {}
    data["Title"] = title
    data["Diameter"] = str(diam)
    data["Points"] = {ind: str((x - shift[0], y - shift[1])) for x, y, ind in p}
    data["Omega"] = str(tuple([str(i) for i in hull]))
    data["Bitmask"] = str(tuple(bitmask))
    data["Partition"] = [
        [str(i) for i in region[-2::-1]] for region in regions
    ]
    name = title
    with open(f'{name}.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)

def transform10(n, omegs=None):
    if omegs is None:
        omegs = ('11', '12', '13', '14', '21', '22', '23', '24', '25', '26')
    for i in omegs:
        transform(f'd{n}_omega{i}.txt', title = f'd{n}_partitions/d{n}_omega{i}')