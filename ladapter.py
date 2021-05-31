import numpy as np
import lreader
import copy


class AAdapter:
    def __init__(self):
        self.data = None  # for each spacecraft: identifier, precision, epoch, coordinates
        self.reader = None

    def calc(self, path):
        pass


class SP3Adapter(AAdapter):
    def __init__(self):
        super().__init__()

    @staticmethod
    def earth_angle(hour, minute, second):
        cur_time = hour * 3600 + minute * 60 + second
        rot = 360 / 86400
        result = rot * cur_time
        return result * np.pi / 180

    @staticmethod
    def aerth_rotation(angle):
        return np.array([[np.cos(angle), -np.sin(angle), 0],
                         [np.sin(angle), np.cos(angle), 0],
                         [0, 0, 1]])

    def calc(self, path):
        self.reader = lreader.SP3Reader(path)
        self.data = copy.deepcopy(self.reader.spacecrafts)
        for sp in self.data:
            sp[3][0] = []
            sp[3][1] = []
            sp[3][2] = []
        j = 0
        for sp in self.reader.spacecrafts:
            date = sp[2]
            coordinates = sp[3]
            i = 0
            for d in date:
                x = coordinates[0][i]
                y = coordinates[1][i]
                z = coordinates[2][i]
                vec = np.array([x, y, z]).T
                angle = self.earth_angle(d.hour, d.minute, d.second)
                rot = self.aerth_rotation(angle)
                result = rot.dot(vec)
                self.data[j][3][0].append(result[0])
                self.data[j][3][1].append(result[1])
                self.data[j][3][2].append(result[2])
                i += 1
            j += 1
        print(123)




class RINEXAdapter(AAdapter):
    def __init__(self):
        super().__init__()

    @staticmethod
    def a_matrix(omega, ipsilon, OMEGA, i):
        u = omega + ipsilon
        elem1 = np.cos(u) * np.cos(OMEGA) - np.sin(u) * np.sin(OMEGA) * np.cos(i)
        elem2 = -np.sin(u) * np.cos(OMEGA) - np.cos(u) * np.sin(OMEGA) * np.cos(i)
        elem3 = np.sin(i) * np.sin(OMEGA)

        elem4 = np.cos(u) * np.sin(OMEGA) + np.sin(u) * np.cos(OMEGA) * np.cos(i)
        elem5 = -np.sin(u) * np.sin(OMEGA) + np.cos(u) * np.cos(OMEGA) * np.cos(i)
        elem6 = -np.sin(i) * np.cos(OMEGA)

        elem7 = np.sin(u) * np.sin(i)
        elem8 = np.cos(u) * np.sin(i)
        elem9 = np.cos(i)
        a = [[elem1, elem2, elem3],
             [elem4, elem5, elem6],
             [elem7, elem8, elem9]]
        return np.array(a)

    def transform_into_descart(self, omega, ipsilon, OMEGA, i, a, e):
        mu = 398600.436e9
        a_m = self.a_matrix(omega, ipsilon, OMEGA, i)
        p = a * (1 - e ** 2)  # фокальный параметр
        r = np.array([[p / (1 + e * np.cos(ipsilon))],
                      [0],
                      [0]])
        v = np.array([[((mu / p) ** 0.5) * e * np.sin(ipsilon)],
                      [((mu / p) ** 0.5) * (1 + e * np.cos(ipsilon))],
                      [0]])
        return a_m.dot(r), a_m.dot(v)

    def calc(self, path):
        self.reader = lreader.RINEXGPSReader(path)
        self.data = copy.deepcopy(self.reader.spacecrafts)
        for sp in self.data:
            sp[3] = [[], [], [], None]

        i = 0
        for sp in self.data:
            for kelems in self.reader.spacecrafts[i][3]:
                coordinates, velocity = self.transform_into_descart(kelems.periapsis_argument,
                                                                    kelems.true_anomaly,
                                                                    kelems.ascending_node_longitude,
                                                                    kelems.inclination,
                                                                    kelems.semimajor_axis,
                                                                    kelems.eccentricity)
                sp[3][0].append(coordinates[0][0])
                sp[3][1].append(coordinates[1][0])
                sp[3][2].append(coordinates[2][0])
            i += 1



