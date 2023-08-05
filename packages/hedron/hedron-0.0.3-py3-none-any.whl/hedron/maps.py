import staticmaps
from staticmaps.color import RED
from cluster_center import average_geolocation
from distance import distance
import random
import pygeodesy
import numpy as np
from range_key_dict import RangeKeyDict
from pprint import pprint
import pandas as pd

tp = staticmaps.tile_provider_OSM
TRED = staticmaps.Color(255, 0, 0, 100)
RED = staticmaps.RED
TYELLOW = staticmaps.Color(255, 255, 0, 100)
YELLOW = staticmaps.YELLOW
TGREEN = staticmaps.Color(0, 255, 0, 100)
GREEN = staticmaps.GREEN
TBLUE = staticmaps.Color(0, 0, 255, 100)
BLUE = staticmaps.BLUE

class Context(staticmaps.Context):
    def add_hash_poly(self, h, fill_color, width, color):
        self.add_object(staticmaps.Area(make_hash_poly_points(h),
                                        fill_color=fill_color,
                                        width=width,
                                        color=color))

    def add_neighbor_hash_polys(self, h, fill_color, width, color):
        hashes = pygeodesy.geohash.neighbors(h)
        for n in hashes.values():
            self.add_object(staticmaps.Area(make_hash_poly_points(n),
                                            fill_color=fill_color,
                                            width=width,
                                            color=color))

    def add_cluster(self, cluster, size=6, color=None, fill_color=None, width=2, colors=None):
        for lat, lon, id, day in zip(cluster.lats, cluster.lons, cluster.ids, cluster.days):
            if colors is not None:
                color = colors[id]
            point = staticmaps.create_latlng(lat, lon)
            self.add_object(staticmaps.Marker(point, color=color, size=size))

    def add_heat_hashes(self, lats, lons, percision):
       hashes = [pygeodesy.geohash.encode(lat, lon, percision) for lat, lon in zip(lats, lons)]
       sr = pd.Series(hashes, name='hashes')
       counts = dict(sr.value_counts())
       colors = density_colors(counts.values())
       for h, count in counts.items():
           c = colors[count]
           self.add_hash_poly(h, c, 1, staticmaps.TRANSPARENT)


def plot_heat_hashes(lats, lons, percision, tileprovider=tp, size=(800, 500)):
    context = Context()
    context.set_tile_provider(tileprovider)
    context.add_heat_hashes(lats, lons, percision)
    return context.render_pillow(*size)


def density_colors(counts: list, transparency=150):
   RED = staticmaps.Color(255, 0, 0, transparency)
   ORANGE = staticmaps.Color(255, 128, 0, transparency)
   YELLOW = staticmaps.Color(255, 255, 0, transparency)
   GREEN = staticmaps.Color(0, 255, 0, transparency)
   BLUE = staticmaps.Color(0, 0, 255, transparency)
   colors = [BLUE, GREEN, YELLOW, ORANGE, RED]
   counts = [n for n in counts if n>0]
   chunks = len(colors)
   lowest = min(counts)
   highest = max(counts)

   if len(set(counts))==1:
       ranges =[(lowest, highest+.1)]
       return RangeKeyDict({r:c for r, c in zip(ranges, colors)})
   chunk_size = (highest - lowest) /chunks
   previous = None
   ranges = []
   for i in np.arange(lowest, highest+.1, chunk_size):
       if previous is not None:
           ranges.append((previous, i))
       previous = i
   ranges[-1] = ranges[-1][0], ranges[-1][1]+.1
   pprint({r:c for r, c in zip(ranges, ['BLUE', 'GREEN', 'YELLOW', 'ORANGE', 'RED'])})
   return RangeKeyDict({r:c for r, c in zip(ranges, colors)})


def plot_cluster(cluster, tileprovider=tp):
    context = Context()
    context.set_tile_provider(tileprovider)
    context.add_cluster(cluster,
                        fill_color=staticmaps.parse_color('#00FF003F'),
                        width=2,
                        color=staticmaps.BLUE)
    return context.render_pillow(800, 500)


def plot_super_cluster(hashes, tileprovider=tp):
    context = Context()
    context.set_tile_provider(tileprovider)
    for h in hashes:
        context.add_hash_poly(h,
                             fill_color=staticmaps.parse_color('#00FF003F'),
                             width=2,
                             color=staticmaps.BLUE)
    return context.render_pillow(800, 500)


def plot_heat_map(super_cluster, p, tileprovider=tp):
    context = Context()
    context.set_tile_provider(tileprovider)
    lats, lons = super_cluster.lats, super_cluster.lons
    context.add_heat_hashes(lats, lons, p)
    return context.render_pillow(800, 500)


def random_color():
    r = random.randrange(0, 256)
    g = random.randrange(0, 256)
    b = random.randrange(0, 256)
    return staticmaps.Color(r, g, b)


def make_hash_poly_points(h):
    b = pygeodesy.geohash.bounds(h)
    sw = b.latS, b.lonW
    nw = b.latN, b.lonW
    ne = b.latN, b.lonE
    se = b.latS, b.lonE
    polygon = [sw, nw, ne, se, sw]
    return [staticmaps.create_latlng(lat, lon) for lat, lon in polygon]


def plot_hash(h, tileprovider=tp):
    context = Context()
    context.set_tile_provider(tileprovider)
    context.add_hash_poly(h,
                          fill_color=staticmaps.parse_color('#00FF003F'),
                          width=2,
                          color=staticmaps.BLUE)
    return context.render_pillow(800, 500)


def plot_neighbors(h, tileprovider=tp):
    context = Context()
    context.set_tile_provider(tileprovider)
    context.add_neighbor_hash_polys(h,
                                    fill_color=staticmaps.parse_color('#00FF003F'),
                                    width=2,
                                    color=staticmaps.BLUE)
    return context.render_pillow(800, 500)


def plot_nine(h, tileprovider=tp):
    context = Context()
    context.set_tile_provider(tileprovider)
    context.add_hash_poly(h,
                          fill_color=staticmaps.parse_color('#00FF010F'),
                          width=5,
                          color=staticmaps.BLUE)
    context.add_neighbor_hash_polys(h,
                                    fill_color=staticmaps.parse_color('#00FF003F'),
                                    width=2,
                                    color=staticmaps.BLUE)
    return context.render_pillow(800, 500)


def add_cluster(context, cluster, size=6, colors=None):
    for lat, lon, id, day in zip(cluster.lats, cluster.lons, cluster.ids, cluster.days):
        if colors is not None:
            color = colors[id]
        point = staticmaps.create_latlng(lat, lon)
        context.add_object(staticmaps.Marker(point, color=color, size=size))

    center = average_geolocation(list(zip(cluster.lats, cluster.lons)))
    point = staticmaps.create_latlng(*center)
    #context.add_object(staticmaps.Marker(point, color=color, size=size))

    def dist(lat, lon, center=center):
        return distance(lat, lon, center[0], center[1], 'km')
    radius = max(dist(lat, lon) for lat, lon in zip(cluster.lats, cluster.lons))
    context.add_object(staticmaps.Circle(point, radius, fill_color=staticmaps.TRANSPARENT, color=color, width=2))

    return context


def map_cluster(cluster, size=6, colors=None):
    if colors is None:
        colors = {id:random_color() for id in set(cluster.ids)}
    context = staticmaps.Context()
    context.set_tile_provider(staticmaps.tile_provider_OSM)
    context = add_cluster(context, cluster, size=size, colors=colors)
    return context.render_pillow(800, 500)


def map_super_cluster(super_cluster):
    ids = super_cluster.ids
    colors = {id:random_color() for id in set(ids)}
    context = staticmaps.Context()
    context.set_tile_provider(staticmaps.tile_provider_OSM)
    for cluster in super_cluster.values():
        context = add_cluster(context, cluster, colors=colors)
    return context.render_pillow(800, 500)
