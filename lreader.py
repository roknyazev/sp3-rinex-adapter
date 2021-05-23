import datetime


class KeplerianElements:
    def __init__(self,
                 eccentricity,
                 semimajor_axis,
                 inclination,
                 ascending_node_longitude,
                 periapsis_argument,
                 true_anomaly):
        self.eccentricity = eccentricity  # e
        self.semimajor_axis = semimajor_axis  # A
        self.inclination = inclination  # i
        self.ascending_node_longitude = ascending_node_longitude  # OMEGA
        self.periapsis_argument = periapsis_argument  # omega
        self.true_anomaly = true_anomaly  # M (ipsilon)

    def get_elements(self):
        return [self.eccentricity,
                self.semimajor_axis,
                self.inclination,
                self.ascending_node_longitude,
                self.periapsis_argument,
                self.true_anomaly]


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
            int(line[3:7]),  # year
            int(line[8:10]),  # month
            int(line[11:13]),  # day
            int(line[14:16]),  # hour
            int(line[17:19]),  # minute
            int(float(line[20:31])))  # second
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
                        int(lines[i][3:7]),  # year
                        int(lines[i][8:10]),  # month
                        int(lines[i][11:13]),  # day
                        int(lines[i][14:16]),  # hour
                        int(lines[i][17:19]),  # minute
                        int(float(lines[i][20:31]))))  # second
                i += 1
            else:
                j = 0
                while lines[i][0] == 'P':
                    line = lines[i]
                    self.spacecrafts[j][3][0].append(float(line[4:18]))
                    self.spacecrafts[j][3][1].append(float(line[18:32]))
                    self.spacecrafts[j][3][2].append(float(line[32:46]))
                    self.spacecrafts[j][3][3].append(float(line[46:60]))
                    j += 1
                    i += 1


class RINEXGPSReader(AReader):
    def __init__(self, path):
        super().__init__(path)
        self.read()

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
        while lines[i].strip() and i < len(lines):
            index = int(lines[i][0:3]) + 1
            identifier = 'G' + str(index)

            epoch = datetime.datetime(2000 + int(lines[i][3:(3+2)]),
                                      int(lines[i][6:(6+2)]),
                                      int(lines[i][9:(9+2)]),
                                      int(lines[i][12:(12+2)]),
                                      int(lines[i][15:(15+2)]),
                                      int(float(lines[i][19:(19+3)])))

            eccentricity = float(lines[i + 2][22:(22 + 19)].replace('D', 'e'))
            semimajor_axis = float(lines[i + 2][60:(60 + 19)].replace('D', 'e'))
            inclination = float(lines[i + 4][3:(3 + 19)].replace('D', 'e'))
            ascending_node_longitude = float(lines[i + 3][41:(41 + 19)].replace('D', 'e'))
            periapsis_argument = float(lines[i + 4][41:(41 + 19)].replace('D', 'e'))
            true_anomaly = float(lines[i + 1][60:(60 + 19)].replace('D', 'e'))

            kepler_elem = KeplerianElements(eccentricity,
                                            semimajor_axis,
                                            inclination,
                                            ascending_node_longitude,
                                            periapsis_argument,
                                            true_anomaly)

            this_identifier_already_here = False
            for sp in self.spacecrafts:
                if sp[0] == identifier:
                    sp[2].append(epoch)
                    sp[3].append(kepler_elem)
                    this_identifier_already_here = True

            if not this_identifier_already_here:
                self.spacecrafts.append([identifier, None, [epoch], [kepler_elem]])
                # Identifier, precision, epoch, Keplerian elements
            i += 8
