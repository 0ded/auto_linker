import json
import os


class DataHandler:
    def __init__(self, path, tf=None):
        self.file = JsonHandler(path)
        if tf is not None:
            try:
                os.remove(path)
            except:
                pass
            self.file.write({"tf": len(tf)})

    def append(self, data, seconds=0, minutes=0, hours=0, days=0):
        time = time_to_timeframe(self.file.get_copy()["tf"], seconds, minutes, hours, days)
        self.file.change_value(str(time), str(data))

    def get(self, seconds=0, minutes=0, hours=0, days=0):
        try:
            time = time_to_timeframe(self.file.get_copy()["tf"], seconds, minutes, hours, days)
            return self.file.get_copy()[str(time)]
        except:
            return None

    def is_init(self):
        try:
            self.file.get_copy()["tf"]
        except:
            return False
        else:
            return True


class JsonHandler:
    # reading and writing json files
    def __init__(self, path):
        self.path = path

    def get_copy(self, copy_file=None):
        # returning the parameters from the json as a dictionary
        # if copy_file isn't None it copies the parameter from self to this file (override)
        f1 = open(self.path, "r")
        parameters = json.load(f1)
        if copy_file is not None:
            with open(copy_file.path, "w") as f2:
                json.dump(parameters, f2)
        f1.close()
        return parameters

    def write(self, parameters):
        # dumps a dictionary to self (override)
        with open(self.path, "w") as f:
            json.dump(parameters, f)

    def change_value(self, key, value):
        # changes a specific key in the dictionary
        parameters = self.get_copy()
        parameters[key] = value
        self.write(parameters)
        return parameters

    def wipe(self):
        with open(self.path, "w") as f:
            data = json.load(f)
            for e in data:
                del e


class Timeframe:
    units = ["seconds", "minutes", "hours", "days"]

    def __init__(self, unit, scope, scope_unit="seconds"):
        # unit is the unit of time
        # scope is how much of the unit
        # scope_ unit if you want to use a different unit for the scope
        self.check_unit_validity([unit])
        self.unit = self.units.index(unit)
        self.scope = scope
        self.scope_unit = self.units.index("seconds")
        # this part is not needed for now
        # it's for using scope units that is not seconds
        """""
            if scope_unit is not None:
                self.check_unit_validity([scope_unit])
                self.scope_unit = self.units.index(scope_unit)
            else:
                self.scope_unit = self.units.index(unit)

            if self.scope_unit > self.unit:
                raise Exception("scope unit must be smaller than time unit")
            """

    def check_unit_validity(self, args):
        # error checking if unit is used currently
        for arg in args:
            if not self.units.__contains__(arg):
                raise Exception("un-supported time unit '{0}'".format(arg))

    def __len__(self):
        # how many scope_units are in scope*unit
        s = 0
        for i in range(self.unit, self.scope_unit, -1):
            if i == self.unit:
                s += self.scope
            if i == 3:
                s *= 24
            if i < 3:
                s *= 60
        return s

    def __str__(self):
        return "{0}.{1}.{2}:{3}".format(self.scope, self.unit, self.scope_unit, len(self))


def time_to_timeframe(tfl, seconds=0, minutes=0, hours=0, days=0):
    temp = seconds + minutes * 60 + hours * 60 * 60 + days * 60 * 60 * 24
    return temp % tfl

def timeframe_to_time(timeframe):
    seconds = timeframe % 60
    timeframe /= 60
    timeframe = int(timeframe)
    minutes = timeframe % 60
    timeframe /= 60
    timeframe = int(timeframe)
    hours = timeframe % 24
    timeframe /= 24
    days = int(timeframe)
    return seconds, minutes, hours, days

