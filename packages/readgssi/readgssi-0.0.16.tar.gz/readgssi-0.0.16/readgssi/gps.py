from datetime import datetime, timedelta
import pynmea2
import math
import numpy as np
import pandas as pd
from geopy.distance import geodesic
import readgssi.functions as fx
from readgssi.constants import TZ
from math import sin, cos, sqrt, atan2, radians

"""
contains functions for reading gps data from various formats
"""

def msgparse(msg):
    """
    .. deprecated:: 0.0.12

    This function returns the NMEA message variables shared by both RMC and GGA.

    :param pynmea2.nmea.NMEASentence msg: A pynmea2 sentence object.
    :rtype: :py:class:`datetime.datetime`, :py:class:`float`, :py:class:`float`
    """
    return msg.timestamp, msg.latitude, msg.longitude

def readdzg(fi, frmt, header, verbose=False):
    """
    A parser to extract gps data from DZG file format. DZG contains raw NMEA sentences, which should include at least RMC and GGA.

    NMEA RMC sentence string format:
    :py:data:`$xxRMC,UTC hhmmss,status,lat DDmm.sss,lon DDDmm.sss,SOG,COG,date ddmmyy,checksum \*xx`

    NMEA GGA sentence string format:
    :py:data:`$xxGGA,UTC hhmmss.s,lat DDmm.sss,lon DDDmm.sss,fix qual,numsats,hdop,mamsl,wgs84 geoid ht,fix age,dgps sta.,checksum \*xx`
    
    Shared message variables between GGA and RMC: timestamp, latitude, and longitude

    RMC contains a datestamp which makes it preferable, but this parser will read either.

    :param str fi: File containing gps information
    :param str frmt: GPS information format ('dzg' = DZG file containing gps sentence strings (see below); 'csv' = comma separated file with: lat,lon,elev,time)
    :param dict header: File header produced by :py:func:`readgssi.dzt.readdzt`
    :param bool verbose: Verbose, defaults to False
    :rtype: GPS data (pandas.DataFrame)

        The dataframe contains the following fields:
        * datetimeutc (:py:class:`datetime.datetime`)
        * trace (:py:class:`int` trace number)
        * longitude (:py:class:`float`)
        * latitude (:py:class:`float`)
        * altitude (:py:class:`float`)
        * velocity (:py:class:`float`)
        * sec_elapsed (:py:class:`float`)
        * meters (:py:class:`float` meters traveled)

    """
    if header['rhf_spm'] == 0:
        spu = header['rhf_sps']
    else:
        spu = header['rhf_spm']
    array = pd.DataFrame(columns=['datetimeutc', 'trace', 'longitude', 'latitude', # our dataframe
                                  'altitude', 'velocity', 'sec_elapsed', 'meters'])

    trace = 0 # the elapsed number of traces iterated through
    tracenum = 0 # the sequential increase in trace number
    rownp = 0 # array row number
    rowrmc = 0 # rmc record iterated through (gps file)
    rowgga = 0 # gga record
    sec_elapsed = 0 # number of seconds since the start of the line
    m = 0 # meters traveled over entire line
    m0, m1 = 0, 0 # meters traveled as of last, current loop
    u = 0 # velocity
    u0 = 0 # velocity on last loop
    timestamp = False
    prevtime = False
    init_time = False
    td = False
    prevtrace = False
    rmc, gga = False, False
    rmcwarn = True
    lathem = 'north'
    lonhem = 'east'
    x0, x1, y0, y1 = False, False, False, False # coordinates
    z0, z1 = 0, 0
    x2, y2, z2, sec2 = 0, 0, 0, 0
    with open(fi, 'r') as gf:
        if verbose:
            fx.printmsg('using gps file:     %s' % (fi))
        if frmt == 'dzg': # if we're working with DZG format
            for ln in gf: # loop through the first few sentences, check for RMC
                if 'RMC' in ln: # check to see if RMC sentence (should occur before GGA)
                    rmc = True
                    if rowrmc == 0:
                        msg = pynmea2.parse(ln.rstrip()) # convert gps sentence to pynmea2 named tuple
                        ts0 = TZ.localize(datetime.combine(msg.datestamp, msg.timestamp)) # row 0's timestamp (not ideal)
                    if rowrmc == 1:
                        msg = pynmea2.parse(ln.rstrip())
                        ts1 = TZ.localize(datetime.combine(msg.datestamp, msg.timestamp)) # row 1's timestamp (not ideal)
                        td = ts1 - ts0 # timedelta = datetime1 - datetime0
                    rowrmc += 1
                if 'GGA' in ln:
                    gga = True
                    if rowgga == 0:
                        msg = pynmea2.parse(ln.rstrip()) # convert gps sentence to pynmea2 named tuple
                        ts0 = TZ.localize(datetime.combine(datetime(1980, 1, 1), msg.timestamp)) # row 0's timestamp (not ideal)
                    if rowgga == 1:
                        msg = pynmea2.parse(ln.rstrip())
                        ts1 = TZ.localize(datetime.combine(datetime(1980, 1, 1), msg.timestamp)) # row 1's timestamp (not ideal)
                        td = ts1 - ts0 # timedelta = datetime1 - datetime0
                    rowgga += 1
            gpssps = 1 / td.total_seconds() # GPS samples per second
            if (rmcwarn) and (rowrmc == 0):
                fx.printmsg('WARNING: no RMC sentences found in GPS records. this could become an issue if your file goes through 00:00:00.')
                fx.printmsg("         if you get a time jump error please open a github issue at https://github.com/iannesbitt/readgssi/issues")
                fx.printmsg("         and attach the verbose output of this script plus a zip of the DZT and DZG files you're working with.")
                rmcwarn = False
            if (rmc and gga) and (rowrmc != rowgga):
                fx.printmsg('WARNING: GGA and RMC sentences are not recorded at the same rate! This could cause unforseen problems!')
                fx.printmsg('    rmc: %i records' % rowrmc)
                fx.printmsg('    gga: %i records' % rowgga)
            if verbose:
                ss0, ss1, ss2 = '', '', ''
                if gga:
                    ss0 = 'GGA'
                if rmc:
                    ss2 = 'RMC'
                if gga and rmc:
                    ss1 = ' and '
                fx.printmsg('found %i %s%s%s GPS epochs at rate of ~%.2f Hz' % (rowrmc, ss0, ss1, ss2, gpssps))
                fx.printmsg('reading gps locations to data frame...')

            gf.seek(0) # back to beginning of file
            rowgga, rowrmc = 0, 0
            for ln in gf: # loop over file line by line
                if '$GSSIS' in ln:
                    # if it's a GSSI sentence, grab the scan/trace number
                    trace = int(ln.split(',')[1])

                if (rmc and gga) and ('GGA' in ln):
                    # RMC doesn't use altitude so if it exists we include it from a neighboring GGA
                    z1 = pynmea2.parse(ln.rstrip()).altitude
                    if rowrmc != rowgga:
                        # this takes care of the case where RMC lines occur above GGA
                        z0 = array['altitude'].iat[rowgga]
                        array['altitude'].iat[rowgga] = z1
                    rowgga += 1

                if rmc == True: # if there is RMC, we can use the full datestamp but there is no altitude
                    if 'RMC' in ln:
                        msg = pynmea2.parse(ln.rstrip())
                        timestamp = TZ.localize(datetime.combine(msg.datestamp, msg.timestamp)) # set t1 for this loop
                        u = msg.spd_over_grnd * 0.514444444 # convert from knots to m/s

                        sec1 = timestamp.timestamp()
                        x1, y1 = float(msg.longitude), float(msg.latitude)
                        if msg.lon_dir in 'W':
                            lonhem = 'west'
                        if msg.lat_dir in 'S':
                            lathem = 'south'
                        if rowrmc != 0:
                            elapsedelta = timestamp - prevtime # t1 - t0 in timedelta format
                            elapsed = float((timestamp-init_time).total_seconds()) # seconds elapsed
                            m += u * elapsedelta.total_seconds()
                        else:
                            u = 0
                            m = 0
                            elapsed = 0
                            if verbose:
                                fx.printmsg('record starts in %s and %s hemispheres' % (lonhem, lathem))
                        x0, y0, z0, sec0, m0 = x1, y1, z1, sec1, m # set xyzs0 for next loop
                        prevtime = timestamp # set t0 for next loop
                        if rowrmc == 0:
                            init_time = timestamp
                        prevtrace = trace
                        array = array.append({'datetimeutc':timestamp.strftime('%Y-%m-%d %H:%M:%S.%f %z'),
                                              'trace':trace, 'longitude':x1, 'latitude':y1, 'altitude':z1,
                                              'velocity':u, 'sec_elapsed':elapsed, 'meters':m}, ignore_index=True)
                        rowrmc += 1

                else: # if no RMC, we hope there is no UTC 00:00:00 in the file.........
                    if 'GGA' in ln:
                        msg = pynmea2.parse(ln.rstrip())
                        timestamp = TZ.localize(datetime.combine(header['rhb_cdt'], msg.timestamp)) # set t1 for this loop

                        sec1 = timestamp.timestamp()
                        x1, y1 = float(msg.longitude), float(msg.latitude)
                        try:
                            z1 = float(msg.altitude)
                        except AttributeError:
                            z1 = 0
                        if msg.lon_dir in 'W':
                            lonhem = 'west'
                        if msg.lat_dir in 'S':
                            lathem = 'south'
                        if rowgga != 0:
                            m += geodesic((y1, x1, z1), (y0, x0, z0)).meters
                            if rmc == False:
                                u = float((m - m0) / (sec1 - sec0))
                            elapsedelta = timestamp - prevtime # t1 - t0 in timedelta format
                            elapsed = float((timestamp-init_time).total_seconds()) # seconds elapsed
                            if elapsed > 3600.0:
                                fx.printmsg("WARNING: Time jumps by more than an hour in this GPS dataset and there are no RMC sentences to anchor the datestamp!")
                                fx.printmsg("         This dataset may cross over the UTC midnight dateline!\nprevious timestamp: %s\ncurrent timestamp:  %s" % (prevtime, timestamp))
                                fx.printmsg("         trace number:       %s" % trace)
                        else:
                            u = 0
                            m = 0
                            elapsed = 0
                            if verbose:
                                fx.printmsg('record starts in %s and %s hemispheres' % (lonhem, lathem))
                        x0, y0, z0, sec0, m0 = x1, y1, z1, sec1, m # set xyzs0 for next loop
                        prevtime = timestamp # set t0 for next loop
                        if rowgga == 0:
                            init_time = timestamp
                        prevtrace = trace
                        array = array.append({'datetimeutc':timestamp.strftime('%Y-%m-%d %H:%M:%S.%f %z'),
                                              'trace':trace, 'longitude':x1, 'latitude':y1, 'altitude':z1,
                                              'velocity':u, 'sec_elapsed':elapsed, 'meters':m}, ignore_index=True)
                        rowgga += 1

            if verbose:
                if rmc:
                    fx.printmsg('processed %i gps epochs (RMC)' % (rowrmc))
                else:
                    fx.printmsg('processed %i gps epochs (GGA)' % (rowgga))

        elif frmt == 'csv':
            with open(fi, 'r') as f:
                gps = np.fromfile(f)

    array['datetimeutc'] = pd.to_datetime(array['datetimeutc'], format='%Y-%m-%d %H:%M:%S.%f +0000', utc=True)
    array.set_index('datetimeutc', inplace=True)
    ## testing purposes
    # if True:
    #     if verbose:
    #         fx.printmsg('writing GPS to %s-gps.csv' % (fi))
    #     array.to_csv('%s-gps.csv' % (fi))
    return array
