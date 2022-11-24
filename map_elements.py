from projection import *

class settlement:
    def __init__(self, name, lat, long, alt, pop=None):
        self.name = str(name)
        self.lat = lat
        self.long = long
        self.alt = alt * 0.001
        self.pop = pop

        R = get_R_at_latitude(lat)
        self.cartesian = spherical2cartesian([R, long, lat])

    def __repr__(self):
        r_str = "Settlement: " + self.name + "\n"
        r_str += " Lat: " + str(self.lat) + "N, Long: " + str(self.long) + "E\n"
        r_str += " Altitude ASL: " + str(self.alt * 1000) + " m\n"

        if self.pop:
            if self.pop >= 0.5E6:
                r_str += " Population: " + str(round(self.pop * 1E-6, 3)) + "M\n"
            elif self.pop >= 50000:
                r_str += " Population: " + str(round(self.pop * 1E-3, 3)) + "k\n"
            else:
                r_str += " Population: " + str(self.pop) + "\n"
        else:
            r_str += " Population: Unknown\n"
            
        return r_str

    def get_pop_str(self):
        if self.pop:
            if self.pop >= 0.5E6:
                r_str = str(round(self.pop * 1E-6, 3)) + "M\n"
            elif self.pop >= 50000:
                r_str = str(round(self.pop * 1E-3, 3)) + "k\n"
            else:
                r_str = str(self.pop) + "\n"
        else:
            r_str = "Unknown"

        return r_str
