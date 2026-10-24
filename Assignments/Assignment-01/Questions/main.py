import math
import csv
from collections import defaultdict

COORDINATES_FILE = "Coordinates.csv"
DISTANCE_FILE  = "distances.csv"

def distance(x1, y1, z1, x2, y2, z2):
    return math.sqrt(( x1 - x2 ) ** 2 + ( y1 - y2 ) ** 2 + ( z1 - z2 ) ** 2)

coordinates = {}
adjacency_list = defaultdict(list)

with open(COORDINATES_FILE, 'r') as file:
    reader = csv.reader(file)
    next(reader)
    for star_name, x, y, z in reader:
        coordinates[star_name] = (int(x), int(y), int(z))

with open(DISTANCE_FILE, "r") as file:
    reader = csv.reader(file)
    for source, destination, dist in reader:
        adjacency_list[source].append((destination, int(dist)))

SOURCE_STAR = "Sun"
DESTINATION_STAR = "61 Virginis"
# DESTINATION_STAR = "Upsilon Andromedae"

from heapq import heapify, heappop, heappush
priority_queue = [ (0, SOURCE_STAR)  ]
visited = set()
heapify(priority_queue)
# f_n = g_n + h_n
while priority_queue:
    dist, current_star =  heappop(priority_queue) # source to current star distance, current_star
    if current_star in visited:
        continue
    if current_star == DESTINATION_STAR:
        print("Reached " + " " + DESTINATION_STAR + " Distance = " + str(dist) )
    visited.add(current_star)
    for neigborstar_name, neigborstar_distance in adjacency_list[current_star]:
        heappush(priority_queue, (dist + neigborstar_distance, neigborstar_name))
















