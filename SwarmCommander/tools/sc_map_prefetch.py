#!/usr/bin/env python3

from SwarmCommander.modules import sc_map_tiler

import sys

if len(sys.argv) < 7:
    print("Usage: map_prefetch.py lat_top lat_bottom lon_left lon_right min_zoom max_zoom\n")
    print("Note that zoom is from 1 to 20\n")
    exit(-1)

lat_top = float(sys.argv[1])
lat_bottom = float(sys.argv[2])
lon_left = float(sys.argv[3])
lon_right = float(sys.argv[4])
min_zoom = int(sys.argv[5])
max_zoom = int(sys.argv[6])

tiler = sc_map_tiler.SC_MapTilerModule(None, 0.0, 0.0)

tiler.set_debug(True)
tiler.prefetch_lat_lon(lat_top, lat_bottom, lon_left, lon_right, min_zoom, max_zoom)

