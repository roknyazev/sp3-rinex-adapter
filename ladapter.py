import numpy as np
import lreader


class AbstractAdapter:
    def __init__(self, path):
        self.data = None
        self.reader = None

    def calc(self):
        pass


class SP3Adapter(AbstractAdapter):
    def __init__(self, path):
        super().__init__(path)
        self.data = None
        self.reader = lreader.SP3Reader(path)

    def calc(self):
        pass


class RINEXAdapter(AbstractAdapter):
    def __init__(self, path):
        super().__init__(path)
        self.data = None
        self.reader = lreader.RINEXReader(path)

    def calc(self):
        pass


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


def transform_into_descart(omega, ipsilon, OMEGA, i, a, e):
    mu = 398600.436e9
    a_m = a_matrix(omega, ipsilon, OMEGA, i)
    p = a * (1 - e ** 2)  # фокальный параметр
    r = np.array([[p / (1 + e * np.cos(ipsilon))],
                  [0],
                  [0]])
    v = np.array([[((mu / p) ** 0.5) * e * np.sin(ipsilon)],
                  [((mu / p) ** 0.5) * (1 + e * np.cos(ipsilon))],
                  [0]])
    return a_m.dot(r), a_m.dot(v)
