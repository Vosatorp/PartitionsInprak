import typing as tp
import json
import matplotlib.pyplot as plt


def check(Title: str,
          Diameter: tp.Optional[float],
          Points: tp.Dict[str, tp.Tuple[float, float]],
          Omega: tp.Tuple[str],
          Bitmask: tp.Tuple[int],
          Partition: tp.List[tp.Tuple[str]]) -> None:
    """
    The function takes the name of the partition(Title),
    declared maximum diameter of parts (Diameter),
    a list of used points(Points), a tire(Omega),
    which points are on the sides and which are not (Bitmask),
    and array(Partition) containing the polygons of the partition.

    It is assumed, that the points of Omega and Parts of Partition
    are given in the counterclockwise order.
    """

    dist = lambda A, B: abs(complex(*Points[A]) - complex(*Points[B]))
    vector = lambda A, B: (B[0] - A[0], B[1] - A[1])
    cross_product = lambda A, B: A[0] * B[1] - A[1] * B[0]
    dot_product   = lambda A, B: A[0] * B[0] + A[1] * B[1]

    def get_diameter(Part: tp.Tuple[str]) -> float:
        """
        Returns the diameter of the polygon that the given part is
        """
        res = 0
        for A in Part:
            for B in Part:
                res = max(res, dist(A, B))
        return res

    def check_diameters() -> float:
        """
        Outputs the diameters of all parts, counts
        and returns the maximum diameter among all parts.
        """
        max_diam = 0
        for Part in Partition:
            cur_diam = get_diameter(Part)
            max_diam = max(max_diam, cur_diam)
            # print('diameter:', cur_diam)
            # uncomment the line if you want to see the diameter of each part
        if Diameter is None:
            flag = True
        else:
            eps = 1e-9
            flag = abs(max_diam - Diameter) < eps
        if not flag:
            print('The stated diameter and the actual diameter are different')
        print('maximum of diameters:', max_diam, '(ok)' if flag else '(NOT OK)')
        return max_diam, flag

    def get_area(Part: tp.Tuple[str]) -> float:
        res = 0
        for i in range(len(Part)):
            res += cross_product(Points[Part[i]], Points[Part[i - 1]])
        return abs(res) / 2

    def check_sum_area() -> bool:
        """
        Calculates the area of all the parts
        and checks that their sum is equal to the area of Omega.
        """
        eps = 1e-9
        total_area = sum(get_area(Part) for Part in Partition)
        omega_area = get_area(Omega)
        print('total area:', total_area)
        print('area of Omega:', omega_area)
        return abs(total_area - omega_area) < eps

    def check_any_edge_in_two() -> bool:
        """
        Checks that each edge of the partition is in exactly
        two parts if it is not on the boundary of Omega,
        and checks that it is in exactly one part
        if the edge is on the boundary.
        """
        flag = True
        for A in Points:
            for B in Points:
                if A == B:
                    continue
                cnt_AB = 0
                cnt_BA = 0
                for Part in Partition:
                    for i in range(len(Part)):
                        if (Part[i - 1], Part[i]) == (A, B):
                            cnt_AB += 1
                        elif (Part[i - 1], Part[i]) == (B, A):
                            cnt_BA += 1
                for i in range(len(Omega)):
                    if (Omega[i], Omega[i - 1]) == (A, B):
                        cnt_AB += 1
                    elif (Omega[i], Omega[i - 1]) == (B, A):
                        cnt_BA += 1
                if cnt_BA + cnt_AB > 0:
                    if not (cnt_AB == cnt_BA == 1):
                        print(cnt_AB, cnt_BA)
                        print(f'Partition failed for segment ({A}, {B})')
                        return False
        print('All edges are in exactly two parts')
        return True

    def belong(P: tp.Tuple[float, float], segment) -> bool:
        eps = 1e-5
        v1 = vector(P, segment[0])
        v2 = vector(P, segment[1])
        return abs(cross_product(v1, v2)) < eps and dot_product(v1, v2) <= 0

    def check_all_points_on_sides() -> bool:
        """
        Checks that any point from Omega
        lies on the corresponding side of the tire
        """
        ones = [i for i in range(len(Bitmask)) if Bitmask[i] == 1]
        it = 0
        curSeg = Points[Omega[ones[it - 1]]], Points[Omega[ones[it]]]
        for i in range(len(Omega)):
            if Bitmask[i]:
                it += 1
                curSeg = Points[Omega[ones[it - 1]]], Points[Omega[ones[it % len(ones)]]]
            elif not belong(Points[Omega[i]], curSeg):
                print(f'Point {Omega[i]} do not belong to segment {Omega[ones[it - 1]]},{Omega[ones[it]]}')
                return False
        print('All points from Omega lies on the corresponding sides of the tire')
        return True

    def draw_partition() -> None:
        plt.figure(figsize=(7, 7))
        for Part in Partition:
            for i in range(len(Part)):
                x1, y1 = Points[Part[i - 1]]
                x2, y2 = Points[Part[i]]
                plt.plot([x1, x2], [y1, y2], color='black')
        plt.xlim((-0.7, 0.7))
        plt.ylim((-0.7, 0.7))

        for i in range(len(Omega)):
            if Bitmask[i]:
                plt.scatter(*Points[Omega[i]], color='black')

        plt.title(Title + f'\ndiam: {mxdiam:.6f}')
        plt.show()

    print('\n' + Title)
    mxdiam, flag0 = check_diameters()
    flag1 = check_sum_area()
    flag2 = check_any_edge_in_two()
    flag3 = check_all_points_on_sides()
    if flag0 and flag1 and flag2 and flag3:
        print('Partition of Omega is correct')
    else:
        print('Partition is incorrect')
    draw_partition()

    return None

def read_json(file):
    """
    Reads the json file containing
    the fields Title, Diameter, Points, Omega, Bitmask and Partition.
    """
    with open(file) as json_file:
        data = json.load(json_file)
        Title = data['Title']
        if data.get('Diameter'):
            Diameter = float(data['Diameter'])
        else:
            Diameter = None
        raw_points = data['Points']
        Points = {key: eval(val) for key, val in raw_points.items()}
        Omega = eval(data['Omega'])
        Bitmask = eval(data['Bitmask'])
        raw_partition = data['Partition']
        Partition = [eval(str(polygon)) for polygon in raw_partition]
    return Title, Diameter, Points, Omega, Bitmask, Partition

def setup():
    check(*read_json('d5_omega6_2.json'))
    check(*read_json('d5_omega6_11.json'))
    check(*read_json('d5_omega6_121.json'))
    check(*read_json('d5_omega6_123.json'))
    check(*read_json('d11_omega2.json'))
    check(*read_json('d13_omega2.json'))
    check(*read_json('d15_omega2.json'))
    check(*read_json('d16_omega6.json'))
    check(*read_json('d17_omega2.json'))
    check(*read_json('d18_omega6.json'))
    check(*read_json('d21_omega2.json'))
    check(*read_json('d22_omega2.json'))
    check(*read_json('d24_omega61.json'))
    check(*read_json('d24_omega62.json'))

def check10(n, omegs=('11', '12', '13', '14', '21', '22', '23', '24', '25', '26')):
    for i in omegs:
        name = f'd{n}_partitions/d{n}_omega{i}.json'
        check(*read_json(name))    

# setup()