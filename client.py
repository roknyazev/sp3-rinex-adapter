import ladapter


class Analisys:
    def __init__(self, path):
        if path.find(".sp3") != -1:
            self.adapter = ladapter.SP3Adapter()
        else:
            self.adapter = ladapter.RINEXAdapter()
        self.adapter.calc(path)
        self.data = []

    def load(self, satellite_type, satellite_index):
        for sp in self.adapter.data:
            ind = int(sp[0][1:3])
            if sp[0][0] == satellite_type and ind == satellite_index:
                self.data.append(sp)
                return
        print("\nСпутник не найден!\n")
