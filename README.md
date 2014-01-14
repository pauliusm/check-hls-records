check-hls-records
=================

Nagios plugin to check for valid HLS records in Wowza or similar software

Getting it
----------
Just clone this repo somewhere, or download latest version of this plugin from https://raw2.github.com/pauliusm/check-hls-records/master/check-hls-records.py

Requirements
------------
Python 2.x, probably would work with 3.x, but untested (please send feedback).

How it works?
-------------


Usage
-----
Add to nrpe.cfg lines like:

````
command[check_stream_records]=/usr/lib64/nagios/plugins/check-hls-records.py recorder.tld stream 1 5
````
And setup check in nagios.

BUGS
------------
There are some, for sure...


FAQ
---
`Q:` ?

`A:` No.

