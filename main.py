import numpy
import lreader
import lreader
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')


sp3 = lreader.SP3Reader("data/Sta21443.sp3")

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for spacecraft in sp3.spacecrafts:
    ax.plot(spacecraft[3][0], spacecraft[3][1], spacecraft[3][2])

plt.show()
