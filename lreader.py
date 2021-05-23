import datetime


class AReader:
    def __init__(self, path):
        self.path = path
        self.spacecrafts = []

    def read(self):
        pass


class SP3Reader(AReader):
    def __init__(self, path):
        super().__init__(path)
        self.flag = None  # Coordinates or velocity flag
        self.date = None
        self.epoch = None
        self.coordinate_system = None
        self.orbit_type = None
        self.calc_step = None
        self.spacecraft_count = None
        self.read()

    def read(self):
        with open(self.path, 'r') as file:
            lines = file.read().splitlines()
        self.parse_header(lines)
        self.parse_location(lines)

    def parse_header(self, lines):
        line = lines[0]
        self.flag = line[3]
        self.date = datetime.datetime(
            int(line[3:7]),             # year
            int(line[8:10]),            # month
            int(line[11:13]),           # day
            int(line[14:16]),           # hour
            int(line[17:19]),           # minute
            int(float(line[20:31])))    # second
        self.epoch = int(line[32:39])
        self.coordinate_system = str(line[46:51])
        self.orbit_type = str(line[52:55])

        line = lines[1]
        self.calc_step = float(line[24:38])

        j = 2
        line = lines[j]
        self.spacecraft_count = int(line[3:6])
        offset = 0
        while lines[offset + 2][1] != '+':
            offset += 1
        for i in range(self.spacecraft_count):
            index = (9 + 3 * i) - (j - 2) * 51
            identifier = lines[j][index:index + 3]
            precision = lines[j + offset][index:index + 3]
            spacecraft = [identifier, precision, [], [[], [], [], []]]  # Identifier, precision, epoch, coordinates
            self.spacecrafts.append(spacecraft)
            if len(line) == index + 3:
                j += 1

    def parse_location(self, lines):
        i = 0
        while lines[i][0] != '*':
            i += 1
        while lines[i][0] != 'E':
            if lines[i][0] == '*':
                for spacecraft in self.spacecrafts:
                    spacecraft[2].append(datetime.datetime(
                                        int(lines[i][3:7]),             # year
                                        int(lines[i][8:10]),            # month
                                        int(lines[i][11:13]),           # day
                                        int(lines[i][14:16]),           # hour
                                        int(lines[i][17:19]),           # minute
                                        int(float(lines[i][20:31]))))   # second
                i += 1
            else:
                j = 0
                while lines[i][0] == 'P':
                    line = lines[i]
                    #self.spacecrafts[j][3].append(
                    #    [float(line[4:18]),
                    #     float(line[18:32]),
                    #     float(line[32:46]),
                    #     float(line[46:60])])
                    self.spacecrafts[j][3][0].append(float(line[4:18]))
                    self.spacecrafts[j][3][1].append(float(line[18:32]))
                    self.spacecrafts[j][3][2].append(float(line[32:46]))
                    self.spacecrafts[j][3][3].append(float(line[46:60]))
                    j += 1
                    i += 1


class KeplerianElements:
    def __int__(self,
                eccentricity,
                semimajor_axis,
                inclination,
                ascending_node_longitude,
                periapsis_argument,
                true_anomaly):
        self.eccentricity = eccentricity
        self.semimajor_axis = semimajor_axis
        self.inclination = inclination
        self.ascending_node_longitude = ascending_node_longitude
        self.periapsis_argument = periapsis_argument
        self.true_anomaly = true_anomaly

    def get_elements(self):
        return [self.eccentricity,
                self.semimajor_axis,
                self.inclination,
                self.ascending_node_longitude,
                self.periapsis_argument,
                self.true_anomaly]


class RINEXReader(AReader):
    def __init__(self, path):
        super().__init__(path)

    def read(self):
        with open(self.path, 'r') as file:
            lines = file.read().splitlines()
        self.parse_header(lines)
        self.parse_location(lines)

    def parse_header(self, lines):
        pass

    def parse_location(self, lines):
        i = 0
        while lines[i].find("END OF HEADER") == -1:
            i += 1
        i += 1
        while i < len(lines) and lines[i][0] != '\n':
            line = lines[i]
            identifier = int(line[0:3])

            epoch = datetime.datetime()
            kepler_elem = KeplerianElements()

            for sp in self.spacecrafts:
                if sp[0] == identifier:
                    sp[2].append(epoch)
                    sp[3].append(kepler_elem)


            # spacecraft = [identifier, None, [], []]  # Identifier, precision, epoch, Keplerian elements
            i += 8

