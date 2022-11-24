import math

from vector3 import *
from projection import *

class Earth_globe:
    def __init__(self):
        self.R_equ = 6378.137 # equatorial radius in km
        self.R_pol = 6356.752 # polar radius in km
        self.R_mean = 6371.000 # volumetric mean radius in km

        self.model = self.generate_Earth_model()

    def get_R_at_latitude(self, lat):
        if lat == 0:
            return self.R_equ
        elif lat == 90:
            return self.R_pol
        
        r1 = self.R_equ
        r2 = self.R_pol
        B = math.radians(lat)

        R_numerator = ((r1**2) * math.cos(B))**2 + ((r2**2) * math.sin(B))**2
        R_denominator = (r1 * math.cos(B))**2 + (r2 * math.sin(B))**2
        R = math.sqrt(R_numerator/R_denominator)
        return R

    def generate_Earth_model(self):
        vertices = []
        for theta in range(0, 359, 10):
            for phi in range(-179, 179, 10):
                R = self.get_R_at_latitude(phi)
                new_vertex = spherical2cartesian([R, theta, phi])
                vertices.append(new_vertex)

        return vertices

