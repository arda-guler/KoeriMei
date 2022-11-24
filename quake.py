from projection import *

class earthquake:
    def __init__(self, date, lat, long, depth, mag):
        self.date = date
        self.lat = lat
        self.long = long
        self.depth = depth
        self.mag = mag

        R = get_R_at_latitude(lat)
        self.cartesian = spherical2cartesian([R, long, lat])

    def __repr__(self):
        r_str = "Earthquake:\n"
        r_str += " Date/Time: " + str(self.date) + "\n"
        r_str += " Lat: " + str(self.lat) + "N Long: " + str(self.long) + "E\n"
        r_str += " Depth: " + str(self.depth) + "\n"
        r_str += " Mag: " + str(self.mag) + "\n"
        return r_str
