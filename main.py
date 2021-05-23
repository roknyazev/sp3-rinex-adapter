import ladapter
import matplotlib.pyplot as plt

rinex = ladapter.RINEXAdapter()
rinex.calc("data/BRDC0010.20n")
sp3 = ladapter.SP3Adapter()
sp3.calc("data/Sta21443.sp3")


rinex_fig = plt.figure()
rinex_ax = rinex_fig.add_subplot(111, projection='3d')
for spacecraft in rinex.data:
    rinex_ax.plot(spacecraft[3][0], spacecraft[3][1], spacecraft[3][2])


sp3_fig = plt.figure()
sp3_ax = sp3_fig.add_subplot(111, projection='3d')
for spacecraft in sp3.data:
    if spacecraft[0][0] == 'G':
        sp3_ax.plot(spacecraft[3][0], spacecraft[3][1], spacecraft[3][2])

plt.show()
