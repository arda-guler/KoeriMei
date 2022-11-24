# gets data from kandilli observatory and earthquake monitoring center
import requests
from bs4 import BeautifulSoup
from datetime import datetime

from quake import earthquake

def read_koeri_list():
    url = "http://www.koeri.boun.edu.tr/scripts/lasteq.asp"
    resp = requests.get(url)
    wpage = BeautifulSoup(resp.text, 'html.parser')
    wpage = str(wpage).split("\n")

    quakelist_start = wpage.index("---------- --------  --------  -------   ----------    ------------    -----------\r")
    quakelist_end = wpage.index("</pre>")

    quakelist = wpage[quakelist_start+1:quakelist_end-1]

    return quakelist

def parse_quakelist():
    raw_data = read_koeri_list()

    parsed_data = []

    for line in raw_data:
        line = line.split(" ")

        for element in line:
            if element == "" or element == " ":
                line.remove(element)
                del element

        parsed_data.append(line)

    return parsed_data

def generate_quakes():
    parsed_data = parse_quakelist()
    quakes = []

    for q_data in parsed_data:
        try:
            q_dtstr = q_data[0] + "-" + q_data[1]
            q_date = datetime.strptime(q_dtstr, '%Y.%m.%d-%H:%M:%S')
            q_lat = float(q_data[2])
            q_long = float(q_data[3])
            q_depth = float(q_data[4])
            q_mag = float(q_data[6])

            new_quake = earthquake(q_date, q_lat, q_long, q_depth, q_mag)
            quakes.append(new_quake)
        except:
            print("KOERI WARNING: Could not parse quake data. Skipping..")

    return quakes

def generate_quakes_test():
    parsed_data = parse_quakelist()
    quakes = []

    for q_data in parsed_data:
        q_dtstr = q_data[0] + "-" + q_data[1]
        q_date = datetime.strptime(q_dtstr, '%Y.%m.%d-%H:%M:%S')
        q_lat = float(q_data[2])
        q_long = float(q_data[3])
        q_depth = float(q_data[4])
        q_mag = float(q_data[6])

        new_quake = earthquake(q_date, q_lat, q_long, q_depth, q_mag)
        quakes.append(new_quake)

    return quakes


