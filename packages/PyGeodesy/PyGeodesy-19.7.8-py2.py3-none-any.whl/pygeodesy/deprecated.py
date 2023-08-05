
# -*- coding: utf-8 -*-

u'''DEPRECATED classes, functions, etc. exported for backward compatibility.
'''

from heights import HeightIDWequirectangular, HeightIDWeuclidean, \
                    HeightIDWhaversine
# avoid importing other modules
from lazily import _ALL_LAZY

__all__ = _ALL_LAZY.deprecated
__version__ = '19.07.05'

_R_M = _WGS84 = _UTM = object()


# DEPRECATED classes, for export only
class HeightIDW(HeightIDWeuclidean):  # PYCHOK exported
    '''DEPRECATED, use class L{HeightIDWeuclidean}.
    '''
    pass


class HeightIDW2(HeightIDWequirectangular):  # PYCHOK exported
    '''DEPRECATED, use class L{HeightIDWequirectangular}.
    '''
    pass


class HeightIDW3(HeightIDWhaversine):  # PYCHOK exported
    '''DEPRECATED, use class L{HeightIDWhaversine}.
    '''
    pass


def areaof(points, adjust=True, radius=_R_M, wrap=True):
    '''DEPRECATED, use function L{areaOf}.
    '''
    from points import areaOf
    from utily import R_M  # PYCHOK shadows?
    r = R_M if radius is _R_M else radius  # PYCHOK shadows?
    return areaOf(points, adjust=adjust, radius=r, wrap=wrap)


def bounds(points, wrap=True, LatLon=None):
    '''DEPRECATED, use function L{boundsOf}.

       @return: 2-Tuple C{(latlonSW, latlonNE)} as B{C{LatLon}}
                or 4-Tuple C{(latS, lonW, latN, lonE)} if
                B{C{LatLon}} is C{None}.
    '''
    from points import boundsOf
    return tuple(boundsOf(points, wrap=wrap, LatLon=LatLon))


def decodeEPSG2(arg):
    '''DEPRECATED, use function L{epsg.decode2}.

       @return: 2-Tuple C{(zone, hemipole)}
    '''
    from epsg import decode2
    return tuple(decode2(arg))


def encodeEPSG(zone, hemipole='', band=''):
    '''DEPRECATED, use function L{epsg.encode}.

       @return: C{EPSG} code (C{int}).
    '''
    from epsg import encode
    return int(encode(zone, hemipole=hemipole, band=band))


def equirectangular3(lat1, lon1, lat2, lon2, **options):
    '''DEPRECATED, use function C{equirectangular_}.

       @return: 3-Tuple C{(distance2, delta_lat, delta_lon)}.
    '''
    from formy import equirectangular_
    return tuple(equirectangular_(lat1, lon1, lat2, lon2, **options)[:3])


def hypot3(x, y, z):
    '''(DEPRECATED), use function L{hypot_}.
    '''
    from fmath import hypot_
    return hypot_(x, y, z)


def isenclosedby(point, points, wrap=False):
    '''DEPRECATED, use function L{isenclosedBy}.
    '''
    from points import isenclosedBy
    return isenclosedBy(point, points, wrap=wrap)


def nearestOn3(point, points, closed=False, wrap=False, **options):
    '''DEPRECATED, use function L{nearestOn5}.

       @return: 3-Tuple C{(lat, lon, distance)}
    '''
    from points import nearestOn5  # no name conflict
    return tuple(nearestOn5(point, points, closed=closed, wrap=wrap, **options)[:3])


def nearestOn4(point, points, closed=False, wrap=False, **options):
    '''DEPRECATED, use function L{nearestOn5}.

       @return: 4-Tuple C{(lat, lon, distance, angle)}
    '''
    from points import nearestOn5  # no name conflict
    return tuple(nearestOn5(point, points, closed=closed, wrap=wrap, **options)[:4])


def parseUTM(strUTM, datum=_WGS84, Utm=_UTM, name=''):
    '''DEPRECATED, use function L{parseUTM5}.

       @return: The UTM coordinate (B{L{Utm}}) or 4-tuple C{(zone,
                hemisphere, easting, northing)} if B{C{Utm}} is C{None}.
    '''
    from datum import Datums  # PYCHOK shadows?
    from utm import parseUTM5, Utm as _Utm
    d = Datums.WGS84 if datum is _WGS84 else datum  # PYCHOK shadows?
    U = _Utm if Utm is _UTM else Utm
    r = parseUTM5(strUTM, datum=d, Utm=U, name=name)
    if isinstance(r, tuple):  # UtmUps5Tuple
        r = r.zone, r.hemipole, r.easting, r.northing  # no band
    return r


def perimeterof(points, closed=False, adjust=True, radius=_R_M, wrap=True):
    '''DEPRECATED, use function L{perimeterOf}.
    '''
    from points import perimeterOf
    from utily import R_M  # PYCHOK shadows?
    r = R_M if radius is _R_M else radius  # PYCHOK shadows?
    return perimeterOf(points, closed=closed, adjust=adjust, radius=r, wrap=wrap)


def polygon(points, closed=True, base=None):
    '''DEPRECATED, use function L{points2}.
    '''
    from utily import points2
    return points2(points, closed=closed, base=base)


def simplify2(points, pipe, radius=_R_M, shortest=False, indices=False, **options):
    '''DEPRECATED, use function L{simplifyRW}.
    '''
    from simplify import simplifyRW
    from utily import R_M  # PYCHOK shadows?
    r = R_M if radius is _R_M else radius  # PYCHOK shadows?
    return simplifyRW(points, pipe, radius=r, shortest=shortest, indices=indices, **options)


def toUtm(latlon, lon=None, datum=None, Utm=_UTM, cmoff=True, name=''):
    '''DEPRECATED, use function L{toUtm8}.

       @return: The UTM coordinate (B{C{Utm}}) or a 6-tuple C{(zone,
                easting, northing, band, convergence, scale)} if
                B{C{Utm}} is C{None} or B{C{cmoff}} is C{False}.
    '''
    from utm import toUtm8, Utm as _Utm
    U = _Utm if Utm is _UTM else Utm
    r = toUtm8(latlon, lon=lon, datum=datum, Utm=U, name=name, falsed=cmoff)
    if isinstance(r, tuple):  # UtmUps8Tuple
        # no hemisphere/pole and datum
        r = r.zone, r.easting, r.northing, r.band, r.convergence, r.scale
    return r


def utmZoneBand2(lat, lon):
    '''DEPRECATED, use function L{utmZoneBand5}.

       @return: 2-Tuple C{(zone, band)}.
    '''
    from utm import utmZoneBand5
    r = utmZoneBand5(lat, lon)  # UtmUpsLatLon5Tuple
    return r.zone, r.band

# **) MIT License
#
# Copyright (C) 2018-2019 -- mrJean1 at Gmail dot com
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
