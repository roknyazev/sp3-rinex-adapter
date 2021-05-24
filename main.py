import client
import ladapter
import matplotlib.pyplot as plt

# rinex = ladapter.RINEXAdapter()
# rinex.calc("data/BRDC0010.20n")
# sp3 = ladapter.SP3Adapter()
# sp3.calc("data/Sta21443.sp3")
# rinex_fig = plt.figure()
# rinex_ax = rinex_fig.add_subplot(111, projection='3d')
# for spacecraft in rinex.data:
#     rinex_ax.plot(spacecraft[3][0], spacecraft[3][1], spacecraft[3][2])
# sp3_fig = plt.figure()
# sp3_ax = sp3_fig.add_subplot(111, projection='3d')
# for spacecraft in sp3.data:
#     if spacecraft[0][0] == 'G':
#         sp3_ax.plot(spacecraft[3][0], spacecraft[3][1], spacecraft[3][2])
# plt.show()

while True:
    try:
        print("Введите путь к файлу:")
        path = str(input())
        satellites = client.Analisys(path)
        break
    except BaseException:
        print("\nНеверный файл!\n")

print("Доступные спутники:")

string = ""
i = 0
tmp = ""
for sat in satellites.adapter.data:
    if sat[0][0] != tmp:
        print(string)
        string = ""
        tmp = sat[0][0]
    string += sat[0] + "  "
    i += 1
print(string + '\n')

while True:
    print("Введите тип спутника (закончить ввод - введите \"break\"):")
    stype = str(input())
    if stype == "break":
        break
    print("Введите номер спутника:")
    ind = int(input())
    satellites.load(stype, ind)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for sat in satellites.data:
    ax.plot(sat[3][0], sat[3][1], sat[3][2])

plt.show()

# data/BRDC0010.20n
# data/Sta21443.sp3
