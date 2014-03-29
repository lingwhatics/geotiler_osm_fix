# Matplotlib Basemap Toolkit example

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

import logging
logging.basicConfig(level=logging.DEBUG)

import geotiler

# background map dimensions
WIDTH = 512
HEIGHT = 512

bbox = 11.78560, 46.48083, 11.79067, 46.48283

fig = plt.figure(figsize=(10, 10))
ax = plt.subplot(111)

#
# download background map using OpenStreetMap
#
dimensions = ModestMaps.Core.Point(WIDTH, HEIGHT)
loc1 = ModestMaps.Geo.Location(bbox[1], bbox[0])
loc2 = ModestMaps.Geo.Location(bbox[3], bbox[2])

cls = ModestMaps.builtinProviders['OPENSTREETMAP']
provider = cls()
mm = ModestMaps.mapByExtent(provider, loc1, loc2, dimensions)
# or
#   mm = ModestMaps.mapByExtentZoom(provider, loc1, loc2, 18)

img = mm.draw() # or simply save in tile cache, i.e. in <tile> file, see below
                # for `imread` also

# recalculate bbox, which can change i.e. due to mapByExtent call
p1, p2 = mm.extent
bbox = p1.lon, p1.lat, p2.lon, p2.lat

#
# create basemap
#
map = Basemap(
    llcrnrlon=bbox[0], llcrnrlat=bbox[1],
    urcrnrlon=bbox[2], urcrnrlat=bbox[3],
    projection='merc', ax=ax
)

# or optionally, read from tile cache: im = plt.imread(<tile>)
map.imshow(img, interpolation='lanczos', origin='upper')

#
# plot 3 custom points
#
x0, y0 = 11.78816, 46.48114 # http://www.openstreetmap.org/search?query=46.48114%2C11.78816
x1, y1 = 11.78771, 46.48165 # http://www.openstreetmap.org/search?query=46.48165%2C11.78771
x, y = map((x0, x1), (y0, y1))
ax.scatter(x, y, c='red', edgecolor='none', s=10, alpha=0.9)

plt.savefig('test.pdf', bbox_inches='tight')
plt.close()

# vim: sw=4:et:ai