#!/usr/bin/env python
#
#

"""HLS record checker - checks for stream record made n minutes ago"""
__author__ = "Paulius Mazeika"
__email__ = "paulius@chroot.lt"
__copyright__ = "Copyright (c) 2014"
__version__ = "0.3"
__status__ = "production"

import datetime
import pycurl
import cStringIO
import sys

def get_output(link, strstart):
    """Returns strings, which starts with strstart, from link"""
    buf = cStringIO.StringIO()
    result = []
    c = pycurl.Curl()
    c.setopt(c.URL, link)
    c.setopt(c.CONNECTTIMEOUT, 60)
    c.setopt(c.WRITEFUNCTION, buf.write)
    c.setopt(c.FAILONERROR, True)
    try:
        c.perform()
    except:
        try:
            c.perform() #second try to fetch the link
        except pycurl.error, error:
            errno, errstr = error
            print "An error occurred while getting %s: %s\n" % (
                link, errstr)
            sys.exit(2) #critical exit code for nagios plugin

    output = buf.getvalue()
    buf.close()
    for line in output.split("\n"):
        if line.startswith(strstart):
            result.append(line)

    return result

def main():
    """Checks validity of HLS records of sys.argv[3] min. length made sys.argv[4] min, ago on server sys.argv[1]"""
    if len(sys.argv) != 5:
        print "Usage: check-hls-records.py <recorder> <stream> <record length in min.> <record start time min. ago>\n"
        sys.exit(1)

    recorder = sys.argv[1] #server to check
    stream = sys.argv[2] #stream name
    rlength = int(sys.argv[3]) #record length in min.
    ago = int(sys.argv[4]) #time min. ago

    starttime = datetime.datetime.now() - datetime.timedelta(minutes=ago) #time minutes ago
    plstart = "%s-%02d-%02d-%s:%s:%s" % (starttime.year, starttime.month, starttime.day,
            starttime.hour, starttime.minute, starttime.second) #wowza playlist start parameters

    link = "http://%s/%s/mp4:%s.stream/playlist.m3u8?DVR&wowzadvrplayliststart=%s&wowzadvrplaylistduration=%s" % \
           (recorder, stream, stream, plstart, rlength * 1000) #wowza record request string

    for chunk in get_output(link, 'chunklist'): #get chunklist
        mlink = "http://%s/%s/mp4:%s.stream/%s" % (recorder, stream, stream, chunk)
        medias = get_output(mlink, 'media') #get medialinklist
        for media in medias:
            mpeglink = "http://%s/%s/mp4:%s.stream/%s" % (recorder, stream, stream, media) #get mpeg links
            for _ in get_output(mpeglink, 'G'): #if data starts with 'G' - it looks like mpeg stream
                continue #just get data, errors will be raised in get_output()
    print "OK: %s has valid %s min HLS record for %s stream made %s min ago\n" % (recorder, rlength, stream, ago)
    sys.exit(0)

if __name__ == "__main__":
    main()
