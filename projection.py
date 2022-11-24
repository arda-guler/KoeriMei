import math
PI = math.pi

from vector3 import *

def latlong2mercantor(lat, long, map_width, map_height):

    x = (long + 180) * (map_width/360)
    
    lat_radians = lat * PI/180
    mercN = math.log(math.tan((PI/4)+(latRad/2)))
    y = (map_height/2) - (map_width * mercN/(2*PI))

    return x, y

# takes cartezian coords list
# gives spherical coords list
def cartesian2spherical(cart):
    
    x = cart.x
    y = cart.y
    z = cart.z
    
    rho = math.sqrt(x**2 + y**2 + z**2)
    try:
        theta = math.degrees(math.atan((math.sqrt(x**2 + y**2))/z))
    except ZeroDivisionError:
        theta = 90
    phi = math.degrees(math.atan(y/x))
    
    return [rho, theta, phi]

# takes spherical coords list
# gives cartezian coords list
def spherical2cartesian(sph):

    rho = sph[0]
    theta = math.radians(sph[1])
    phi = math.radians(sph[2])
    
    x = math.cos(theta) * math.cos(phi) * rho
    y = math.sin(theta) * math.cos(phi) * rho
    z = math.sin(phi) * rho
    
    return vec3(x, y, z)

def get_R_at_latitude(lat):
    r1 = 6378.137
    r2 = 6356.752
    
    if lat == 0:
        return r1
    elif lat == 90:
        return r2
    
    B = math.radians(lat)

    R_numerator = ((r1**2) * math.cos(B))**2 + ((r2**2) * math.sin(B))**2
    R_denominator = (r1 * math.cos(B))**2 + (r2 * math.sin(B))**2
    R = math.sqrt(R_numerator/R_denominator)
    return R
