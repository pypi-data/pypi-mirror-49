
# -*- coding: utf-8 -*-

u'''Terrestrial Reference Frame (TRF) class L{RefFrame} and registry thereof L{RefFrames}.

Transcribed from Chris Veness' (C) 2006-2019 JavaScript originals
U{latlon-ellipsoidal-referenceframe.js<https://GitHub.com/chrisveness/geodesy/blob/master/
latlon-ellipsoidal-referenceframe.js>} and U{latlon-ellipsoidal-referenceframe-txparams.js
<https://GitHub.com/chrisveness/geodesy/blob/master/latlon-ellipsoidal-referenceframe-txparams.js>}.

Modern geodetic reference frames: a latitude/longitude point defines a geographic location on,
above or below the earth’s surface, measured in degrees from the equator and the U{International
Reference Meridian<https://WikiPedia.org/wiki/IERS_Reference_Meridian>} (IRM) and metres above
the ellipsoid within a given I{Terrestrial Reference Frame} at a given I{epoch}.

This is scratching the surface of complexities involved in high precision geodesy, but may
be of interest and/or value to those with less demanding requirements.  More information
U{here<https://www.Movable-Type.co.UK/scripts/geodesy-library.html>} and U{here
<https://www.Movable-Type.co.UK/scripts/geodesy-library.html#latlon-ellipsoidal-referenceframe>}.

Note that I{ITRF solutions} do not directly use an ellipsoid, but are specified by Cartesian
coordinates.  The GRS80 ellipsoid is recommended for transformations to geographical coordinates.

Note WGS84(G730/G873/G1150) are coincident with ITRF at 10-centimetre level, see also U{here
<ftp://ITRF.ENSG.IGN.FR/pub/itrf/WGS84.TXT>}.  WGS84(G1674) and ITRF20014 / ITRF2008 ‘are
likely to agree at the centimeter level’, see also U{QPS/QINSy<https://Confluence.QPS.NL/qinsy/
en/how-to-deal-with-etrs89-datum-and-time-dependent-transformation-parameters-45353274.html>}.

@var RefFrames.ETRF2000: RefFrame(name='ETRF2000', epoch=2005.0, ellipsoid=Ellipsoid(name='GRS80')
@var RefFrames.GDA94: RefFrame(name='GDA94', epoch=1994.0, ellipsoid=Ellipsoid(name='GRS80')
@var RefFrames.ITRF2000: RefFrame(name='ITRF2000', epoch=1997.0, ellipsoid=Ellipsoid(name='GRS80')
@var RefFrames.ITRF2005: RefFrame(name='ITRF2005', epoch=2000.0, ellipsoid=Ellipsoid(name='GRS80')
@var RefFrames.ITRF2008: RefFrame(name='ITRF2008', epoch=2005.0, ellipsoid=Ellipsoid(name='GRS80')
@var RefFrames.ITRF2014: RefFrame(name='ITRF2014', epoch=2010.0, ellipsoid=Ellipsoid(name='GRS80')
@var RefFrames.ITRF91: RefFrame(name='ITRF91', epoch=1988.0, ellipsoid=Ellipsoid(name='GRS80')
@var RefFrames.ITRF93: RefFrame(name='ITRF93', epoch=1988.0, ellipsoid=Ellipsoid(name='GRS80')
@var RefFrames.NAD83: RefFrame(name='NAD83', epoch=1997.0, ellipsoid=Ellipsoid(name='GRS80')
@var RefFrames.WGS84g1150: RefFrame(name='WGS84g1150', epoch=2001.0, ellipsoid=Ellipsoid(name='WGS84')
@var RefFrames.WGS84g1674: RefFrame(name='WGS84g1674', epoch=2005.0, ellipsoid=Ellipsoid(name='WGS84')
@var RefFrames.WGS84g1762: RefFrame(name='WGS84g1762', epoch=2005.0, ellipsoid=Ellipsoid(name='WGS84')
'''

from datum import Ellipsoid, Ellipsoids, Transform
from fmath import isscalar, map1
from lazily import _ALL_LAZY
from named import classname, _NamedDict as _X, \
                 _NamedEnum, _NamedEnumItem
from utily import property_RO, _TypeError

__all__ = _ALL_LAZY.trf
__version__ = '19.07.08'

_mDays = (0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
# temporarily hold a single instance for each float value
_trfFs = {}


def _F(f):
    '''Cache a single C{float}.
    '''
    try:
        f = _trfFs[f]  # PYCHOK del _trfFs
    except KeyError:
        _trfFs[f] = f  # PYCHOK del _trfFs
    return f


def _T(*fs):
    '''(INTERNAL) Cache a tuple of single C{float}s.
    '''
    return map1(_F, *fs)


def _2epoch(epoch):  # imported by .ellipsoidalBase.py
    '''(INTERNAL) Validate an C{epoch}.
    '''
    if isscalar(epoch) and epoch > 0:  # XXX 1970?
        return _F(epoch)
    raise TypeError('%s not %s: %r' % ('epoch', 'scalar', epoch))


class RefFrameError(ValueError):
    '''Reference frame or conversion issue.
    '''
    pass


class RefFrame(_NamedEnumItem):
    '''Terrestrial Reference Frame (TRF).
    '''
    _ellipsoid = None  #: Ellipsoid GRS80 or WGS84 (L{Ellipsoid}).
    _epoch     = 0     #: Epoch, calendar year (C{float}).

    def __init__(self, epoch, ellipsoid, name=''):
        '''New L{RefFrame}.

           @param epoch: Epoch, a fractional calendar year (C{scalar}).
           @param ellipsoid: The ellipsoid (L{Ellipsoid}).
           @keyword name: Optional, unique name (C{str}).

           @raise NameError: A L{RefFrame} with that B{C{name}}
                             already exists.

           @raise TypeError: If B{C{epoch}} is not C{scalar} or
                             B{C{ellipsoid}} is not an L{Ellipsoid}.
        '''
        _TypeError(Ellipsoid, ellipsoid=ellipsoid)
        self._ellipsoid = ellipsoid
        self._epoch = _2epoch(epoch)
        self._register(RefFrames, name)

    @property_RO
    def ellipsoid(self):
        '''Get this reference frame's ellipsoid (L{Ellipsoid}).
        '''
        return self._ellipsoid

    @property_RO
    def epoch(self):
        '''Get this reference frame's epoch (C{float}).
        '''
        return self._epoch

    def toStr(self):  # PYCHOK expected
        '''Return this reference frame as a text string.

           @return: This L{RefFrame}'s attributes (C{str}).
        '''
        e = self.ellipsoid
        t = ('name=%r'               % (self.name,),
             'epoch=%.1f'            % (self.epoch,),
             'ellipsoid=%s(name=%r)' % (classname(e), e.name))
        return ', '.join(t)


RefFrames = _NamedEnum('RefFrames', RefFrame)  #: Registered reference frames.
# <https://GitHub.com/chrisveness/geodesy/blob/master/latlon-ellipsoidal-referenceframe.js>
RefFrames._assert(
    ITRF2014   = RefFrame(_F(2010.0), Ellipsoids.GRS80, 'ITRF2014'),
    ITRF2008   = RefFrame(_F(2005.0), Ellipsoids.GRS80, 'ITRF2008'),
    ITRF2005   = RefFrame(_F(2000.0), Ellipsoids.GRS80, 'ITRF2005'),
    ITRF2000   = RefFrame(_F(1997.0), Ellipsoids.GRS80, 'ITRF2000'),
    ITRF93     = RefFrame(_F(1988.0), Ellipsoids.GRS80, 'ITRF93'),
    ITRF91     = RefFrame(_F(1988.0), Ellipsoids.GRS80, 'ITRF91'),
    WGS84g1762 = RefFrame(_F(2005.0), Ellipsoids.WGS84, 'WGS84g1762'),
    WGS84g1674 = RefFrame(_F(2005.0), Ellipsoids.WGS84, 'WGS84g1674'),
    WGS84g1150 = RefFrame(_F(2001.0), Ellipsoids.WGS84, 'WGS84g1150'),
    ETRF2000   = RefFrame(_F(2005.0), Ellipsoids.GRS80, 'ETRF2000'),  # ETRF2000(R08)
    NAD83      = RefFrame(_F(1997.0), Ellipsoids.GRS80, 'NAD83'),  # CORS96
    GDA94      = RefFrame(_F(1994.0), Ellipsoids.GRS80, 'GDA94'))


def date2epoch(year, month, day):
    '''Return the reference frame C{epoch} for a calendar day.

       @param year: Year of the date (C{scalar}).
       @param month: Month in the B{C{year}} (C{scalar}, 1..12).
       @param day: Day in the B{C{month}} (C{scalar}, 1..31).

       @return: Epoch, the fractional year (C{float}).

       @raise ValueError: Invalid B{C{year}}, B{C{month}} or B{C{day}}.

       @note: Any B{C{year}} is considered a leap year, i.e. having
              29 days in February.
    '''
    try:
        y, m, d = map1(int, year, month, day)
        if y > 0 and 1 <= m <= 12 and 1 <= d <= _mDays[m]:
            return y + float(sum(_mDays[:m]) + d) / 366.0
    except (ValueError, TypeError):
        pass
    raise ValueError('%s invalid: %s-%s-%s' % ('date', year, month, day))


# TRF conversions specified as 7-parameter Helmert transforms and an epoch.  Most
# from U{Transformation Parameters<http://ITRF.IGN.FR/trans_para.php>}, more at U{QPS
# <https://Confluence.QPS.NL/qinsy/files/en/29856813/45482834/2/1453459502000/ITRF_Transformation_Parameters.xlsx>}.
_trfNs =                                   ('tx',    'ty',    'tz',   's',   'sx',    'sy',    'sz')
_trfXs = {  # (from_TRF, to_TRF):            mm       mm       mm     ppb     mas      mas      mas
    # see U{Transformation Parameters ITRF2014<http://ITRF.IGN.FR/doc_ITRF/Transfo-ITRF2014_ITRFs.txt>}
    ('ITRF2014', 'ITRF2008'): _X(epoch=_F(2010.0),  # <http://ITRF.ENSG.IGN.FR/ITRF_solutions/2014/tp_14-08.php>
                                 xform=_T(  1.6,     1.9,     2.4,  -0.02,   0.0,     0.0,     0.0),
                                 rates=_T(  0.0,     0.0,    -0.1,   0.03,   0.0,     0.0,     0.0)),
    ('ITRF2014', 'ITRF2005'): _X(epoch=_F(2010.0),
                                 xform=_T(  2.6,     1.0,    -2.3,   0.92,   0.0,     0.0,     0.0),
                                 rates=_T(  0.3,     0.0,    -0.1,   0.03,   0.0,     0.0,     0.0)),
    ('ITRF2014', 'ITRF2000'): _X(epoch=_F(2010.0),
                                 xform=_T(  0.7,     1.2,   -26.1,   2.12,   0.0,     0.0,     0.0),
                                 rates=_T(  0.1,     0.1,    -1.9,   0.11,   0.0,     0.0,     0.0)),
    ('ITRF2014', 'ITRF97'):   _X(epoch=_F(2010.0),
                                 xform=_T(  7.4,    -0.5,   -62.8,   3.8,    0.0,     0.0,     0.26),
                                 rates=_T(  0.1,    -0.5,    -3.3,   0.12,   0.0,     0.0,     0.02)),
    ('ITRF2014', 'ITRF96'):   _X(epoch=_F(2010.0),
                                 xform=_T(  7.4,    -0.5,   -62.8,   3.8,    0.0,     0.0,     0.26),
                                 rates=_T(  0.1,    -0.5,    -3.3,   0.12,   0.0,     0.0,     0.02)),
    ('ITRF2014', 'ITRF94'):   _X(epoch=_F(2010.0),
                                 xform=_T(  7.4,    -0.5,   -62.8,   3.8,    0.0,     0.0,     0.26),
                                 rates=_T(  0.1,    -0.5,    -3.3,   0.12,   0.0,     0.0,     0.02)),
    ('ITRF2014', 'ITRF93'):   _X(epoch=_F(2010.0),
                                 xform=_T(-50.4,     3.3,   -60.2,   4.29,  -2.81,   -3.38,    0.4),
                                 rates=_T( -2.8,    -0.1,    -2.5,   0.12,  -0.11,   -0.19,    0.07)),
    ('ITRF2014', 'ITRF92'):   _X(epoch=_F(2010.0),
                                 xform=_T( 15.4,     1.5,   -70.8,   3.09,   0.0,     0.0,     0.26),
                                 rates=_T(  0.1,    -0.5,    -3.3,   0.12,   0.0,     0.0,     0.02)),
    ('ITRF2014', 'ITRF91'):   _X(epoch=_F(2010.0),
                                 xform=_T( 27.4,    15.5,   -76.8,   4.49,   0.0,     0.0,     0.26),
                                 rates=_T(  0.1,    -0.5,    -3.3,   0.12,   0.0,     0.0,     0.02)),
    ('ITRF2014', 'ITRF90'):   _X(epoch=_F(2010.0),
                                 xform=_T( 25.4,    11.5,   -92.8,   4.79,   0.0,     0.0,     0.26),
                                 rates=_T(  0.1,    -0.5,    -3.3,   0.12,   0.0,     0.0,     0.02)),
    ('ITRF2014', 'ITRF89'):   _X(epoch=_F(2010.0),
                                 xform=_T( 30.4,    35.5,  -130.8,   8.19,   0.0,     0.0,     0.26),
                                 rates=_T(  0.1,    -0.5,    -3.3,   0.12,   0.0,     0.0,     0.02)),
    ('ITRF2014', 'ITRF88'):   _X(epoch=_F(2010.0),
                                 xform=_T( 25.4,    -0.5,  -154.8,  11.29,   0.1,     0.0,     0.26),
                                 rates=_T(  0.1,    -0.5,    -3.3,   0.12,   0.0,     0.0,     0.02)),

    # see U{Transformation Parameters ITRF2008<http://ITRF.IGN.FR/doc_ITRF/Transfo-ITRF2008_ITRFs.txt>}
#   ('ITRF2008', 'ITRF2005'): _X(epoch=_F(2005.0),  # <http://ITRF.ENSG.IGN.FR/ITRF_solutions/2008/tp_08-05.php>
#                                xform=_T( -0.5,    -0.9,    -4.7,   0.94,   0.0,     0.0,     0.0),
#                                rates=_T(  0.3,     0.0,     0.0,   0.0,    0.0,     0.0,     0.0)),
    ('ITRF2008', 'ITRF2005'): _X(epoch=_F(2000.0),
                                 xform=_T( -2.0,    -0.9,    -4.7,   0.94,   0.0,     0.0,     0.0),
                                 rates=_T(  0.3,     0.0,     0.0,   0.0,    0.0,     0.0,     0.0)),
    ('ITRF2008', 'ITRF2000'): _X(epoch=_F(2000.0),
                                 xform=_T( -1.9,    -1.7,   -10.5,   1.34,   0.0,     0.0,     0.0),
                                 rates=_T(  0.1,     0.1,    -1.8,   0.08,   0.0,     0.0,     0.0)),
    ('ITRF2008', 'ITRF97'):   _X(epoch=_F(2000.0),
                                 xform=_T(  4.8,     2.6,   -33.2,   2.92,   0.0,     0.0,     0.06),
                                 rates=_T(  0.1,    -0.5,    -3.2,   0.09,   0.0,     0.0,     0.02)),
    ('ITRF2008', 'ITRF96'):   _X(epoch=_F(2000.0),
                                 xform=_T(  4.8,     2.6,   -33.2,   2.92,   0.0,     0.0,     0.06),
                                 rates=_T(  0.1,    -0.5,    -3.2,   0.09,   0.0,     0.0,     0.02)),
    ('ITRF2008', 'ITRF94'):   _X(epoch=_F(2000.0),
                                 xform=_T(  4.8,     2.6,   -33.2,   2.92,   0.0,     0.0,     0.06),
                                 rates=_T(  0.1,    -0.5,    -3.2,   0.09,   0.0,     0.0,     0.02)),
    ('ITRF2008', 'ITRF93'):   _X(epoch=_F(2000.0),
                                 xform=_T(-24.0,     2.4,   -38.6,   3.41,  -1.71,   -1.48,   -0.3),
                                 rates=_T( -2.8,    -0.1,    -2.4,   0.09,  -0.11,   -0.19,    0.07)),
    ('ITRF2008', 'ITRF92'):   _X(epoch=_F(2000.0),
                                 xform=_T( 12.8,     4.6,   -41.2,   2.21,   0.0,     0.0,     0.06),
                                 rates=_T(  0.1,    -0.5,    -3.2,   0.09,   0.0,     0.0,     0.02)),
    ('ITRF2008', 'ITRF91'):   _X(epoch=_F(2000.0),
                                 xform=_T( 24.8,    18.6,   -47.2,   3.61,   0.0,     0.0,     0.06),
                                 rates=_T(  0.1,    -0.5,    -3.2,   0.09,   0.0,     0.0,     0.02)),
    ('ITRF2008', 'ITRF90'):   _X(epoch=_F(2000.0),
                                 xform=_T( 22.8,    14.6,   -63.2,   3.91,   0.0,     0.0,     0.06),
                                 rates=_T(  0.1,    -0.5,    -3.2,   0.09,   0.0,     0.0,     0.02)),
    ('ITRF2008', 'ITRF89'):   _X(epoch=_F(2000.0),
                                 xform=_T( 27.8,    38.6,  -101.2,   7.31,   0.0,     0.0,     0.06),
                                 rates=_T(  0.1,    -0.5,    -3.2,   0.09,   0.0,     0.0,     0.02)),
    ('ITRF2008', 'ITRF88'):   _X(epoch=_F(2000.0),
                                 xform=_T( 22.8,     2.6,  -125.2,  10.41,   0.1,     0.0,     0.06),
                                 rates=_T(  0.1,    -0.5,    -3.2,   0.09,   0.0,     0.0,     0.02)),

    ('ITRF2005', 'ITRF2000'): _X(epoch=_F(2000.0),  # <http://ITRF.ENSG.IGN.FR/ITRF_solutions/2005/tp_05-00.php>
                                 xform=_T(  0.1,    -0.8,    -5.8,   0.4,    0.0,     0.0,     0.0),
                                 rates=_T( -0.2,     0.1,    -1.8,   0.08,   0.0,     0.0,     0.0)),

    ('ITRF2000', 'ITRF97'):   _X(epoch=_F(1997.0),
                                 xform=_T( 0.67,     0.61,   -1.85,  1.55,   0.0,     0.0,     0.0),
                                 rates=_T( 0.0,     -0.06,   -0.14,  0.01,   0.0,     0.0,     0.02)),
    ('ITRF2000', 'ITRF96'):   _X(epoch=_F(1997.0),
                                 xform=_T( 0.67,     0.61,   -1.85,  1.55,   0.0,     0.0,     0.0),
                                 rates=_T( 0.0,     -0.06,   -0.14,  0.01,   0.0,     0.0,     0.02)),
    ('ITRF2000', 'ITRF94'):   _X(epoch=_F(1997.0),
                                 xform=_T( 0.67,     0.61,   -1.85,  1.55,   0.0,     0.0,     0.0),
                                 rates=_T( 0.0,     -0.06,   -0.14,  0.01,   0.0,     0.0,     0.02)),
    ('ITRF2000', 'ITRF93'):   _X(epoch=_F(1988.0),
                                 xform=_T( 12.7,     6.5,   -20.9,   1.95,  -0.39,    0.8,    -1.14),
                                 rates=_T( -2.9,    -0.2,    -0.6,   0.01,  -0.11,   -0.19,    0.07)),
    ('ITRF2000', 'ITRF92'):   _X(epoch=_F(1988.0),
                                 xform=_T( 1.47,     1.35,   -1.39,  0.75,   0.0,     0.0,    -0.18),
                                 rates=_T( 0.0,     -0.06,   -0.14,  0.01,   0.0,     0.0,     0.02)),
    ('ITRF2000', 'ITRF91'):   _X(epoch=_F(1988.0),
                                 xform=_T( 26.7,    27.5,   -19.9,   2.15,   0.0,     0.0,    -0.18),
                                 rates=_T(  0.0,    -0.6,    -1.4,   0.01,   0.0,     0.0,     0.02)),
    ('ITRF2000', 'ITRF90'):   _X(epoch=_F(1988.0),
                                 xform=_T( 2.47,     2.35,   -3.59,  2.45,   0.0,     0.0,    -0.18),
                                 rates=_T( 0.0,     -0.06,   -0.14,  0.01,   0.0,     0.0,     0.02)),
    ('ITRF2000', 'ITRF89'):   _X(epoch=_F(1988.0),
                                 xform=_T( 2.97,     4.75,   -7.39,  5.85,   0.0,     0.0,    -0.18),
                                 rates=_T( 0.0,     -0.06,   -0.14,  0.01,   0.0,     0.0,     0.02)),
    ('ITRF2000', 'ITRF88'):   _X(epoch=_F(1988.0),
                                 xform=_T( 2.47,     1.15,   -9.79,  8.95,   0.1,     0.0,    -0.18),
                                 rates=_T( 0.0,     -0.06,   -0.14,  0.01,   0.0,     0.0,     0.02)),

    # see U{Boucher, C. & Altamimi, Z. "Memo: Specifications for reference frame fixing in the
    # analysis of a EUREF GPS campaign" (2011) <https://ETRS89.ENSG.IGN.FR/memo-V8.pdf>} and
    # Altamimi, Z. U{"Key results of ITRF2014 and implication to ETRS89 realization", EUREF2016
    # <https://www.EUREF.EU/symposia/2016SanSebastian/01-02-Altamimi.pdf>}.
    ('ITRF2014', 'ETRF2000'): _X(epoch=_F(2000.0),
                                 xform=_T( 53.7,    51.2,   -55.1,   1.02,   0.891,   5.39,   -8.712),
                                 rates=_T(  0.1,     0.1,    -1.9,   0.11,   0.081,   0.49,   -0.792)),
    ('ITRF2008', 'ETRF2000'): _X(epoch=_F(2000.0),
                                 xform=_T( 52.1,    49.3,   -58.5,   1.34,   0.891,   5.39,   -8.712),
                                 rates=_T(  0.1,     0.1,    -1.8,   0.08,   0.081,   0.49,   -0.792)),
    ('ITRF2005', 'ETRF2000'): _X(epoch=_F(2000.0),
                                 xform=_T( 54.1,    50.2,   -53.8,   0.4,    0.891,   5.39,   -8.712),
                                 rates=_T( -0.2,     0.1,    -1.8,   0.08,   0.081,   0.49,   -0.792)),
    ('ITRF2000', 'ETRF2000'): _X(epoch=_F(2000.0),
                                 xform=_T( 54.0,    51.0,   -48.0,   0.0,    0.891,   5.39,   -8.712),
                                 rates=_T(  0.0,     0.0,     0.0,   0.0,    0.081,   0.49,   -0.792)),

    # see U{Solar, T. & Snay, R.A. "Transforming Positions and Velocities between the
    # International Terrestrial Reference Frame of 2000 and North American Datum of 1983"
    # (2004)<https://www.NGS.NOAA.gov/CORS/Articles/SolerSnayASCE.pdf>}
    ('ITRF2000', 'NAD83'):    _X(epoch=_F(1997.0),  # note NAD83(CORS96)
                                 xform=_T(995.6, -1901.3,  -521.5,   0.62,  25.915,   9.426,  11.599),
                                 rates=_T(  0.7,    -0.7,     0.5,  -0.18,   0.067,  -0.757,  -0.051)),

    # see Table 2 in U{Dawson, J. & Woods, A. "ITRF to GDA94 coordinate transformations", Journal of
    # Applied Geodesy 4 (2010), 189-199<https://www.ResearchGate.net/publication/258401581_ITRF_to_GDA94_coordinate_transformations>}
    # (note, sign of rotations for GDA94 reversed as "Australia assumes rotation to be of coordinate
    # axes" rather than the more conventional "position around the coordinate axes")
    ('ITRF2008', 'GDA94'):    _X(epoch=_F(1994.0),
                                 xform=_T(-84.68,  -19.42,   32.01,  9.71,  -0.4254,  2.2578,  2.4015),
                                 rates=_T(  1.42,    1.34,    0.9,   0.109,  1.5461,  1.182,   1.1551)),
    ('ITRF2005', 'GDA94'):    _X(epoch=_F(1994.0),
                                 xform=_T(-79.73,   -6.86,   38.03,  6.636,  0.0351, -2.1211, -2.1411),
                                 rates=_T(  2.25,   -0.62,   -0.56,  0.294, -1.4707, -1.1443, -1.1701)),
    ('ITRF2000', 'GDA94'):    _X(epoch=_F(1994.0),
                                 xform=_T(-45.91,  -29.85,  -20.37,  7.07,  -1.6705,  0.4594,  1.9356),
                                 rates=_T( -4.66,    3.55,   11.24,  0.249,  1.7454,  1.4868,  1.224)),
}

_Forward =  1.0e-3  # mm2m, ppb2ppM, mas2as
_Reverse = -1.0e-3  # same, inverse transforms


def _intermediate(n1, n2):
    '''(INTERNAL) Find a trf* "in between" C{n1} and C{n2}.
    '''
    f1 = set(m for n, m in _trfXs.keys() if n == n1)  # from trf1
    t2 = set(n for n, m in _trfXs.keys() if m == n2)  # to trf2
    n = f1.intersection(t2)
    return n.pop() if n else ''


def _reframeTransforms(rf2, rf, epoch):
    '''(INTERNAL) Get 0, 1 or 2 Helmert C{Transforms} to convert
       reference frame C{rf} observed at C{epoch} into C{rf2}.
    '''
    n2 = rf2.name  # .upper()
    n1 = rf.name   # .upper()
    if n1 == n2 or (n1.startswith('ITRF') and n2.startswith('WGS84')) \
                or (n2.startswith('ITRF') and n1.startswith('WGS84')):
        return ()

    if (n1, n2) in _trfXs:
        return (_2Transform((n1, n2), epoch, _Forward),)

    if (n2, n1) in _trfXs:
        return (_2Transform((n2, n1), epoch, _Reverse),)

    n = _intermediate(n1, n2)
    if n:
        return (_2Transform((n1, n), epoch, _Forward),
                _2Transform((n, n2), epoch, _Forward))

    n = _intermediate(n2, n1)
    if n:
        return (_2Transform((n, n1), epoch, _Reverse),
                _2Transform((n2, n), epoch, _Reverse))

    raise RefFrameError('no %s % to %s' % ('conversion', n1, n2))


def _2Transform(n1_n2, epoch, _Forward_Reverse):
    '''(INTERNAL) Combine a 14-element Helmert C{trfX} and
       C{d_epoch} into a single 7-element C{Transform}.
    '''
    X = _trfXs[n1_n2]
    e = epoch - X.epoch  # fractional delta years
    d = dict((n, (x + r * e) * _Forward_Reverse) for
              n,  x,  r in zip(_trfNs, X.xform, X.rates))
    t = Transform(**d)
    return t


if __name__ == '__main__':

    n, t = len(_trfFs), (len(RefFrames) + len(_trfXs) * 15)
    print('len(_trfFs) %d / len(_trfXs) %d: %.1f%%\n' % (n, t, n * 100.0 / t))

    for m in range(1, 13):
        y, d = 2020, _mDays[m]
        print('date2epoch(%d, %d, %d) %.3f' % (y, m, d, date2epoch(y, m, d)))

    # __doc__ of this file
    t = [''] + repr(RefFrames).split('\n')
    print('\n@var '.join(i.strip(',') for i in t))

_F = float  # float back to normal
del _trfFs  # trash floats cache
