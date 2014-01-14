check-hls-records
=================

Nagios plugin to check for valid HLS records in Wowza or similar software

Getting it
----------
Just clone this repo somewhere, or download latest version of this plugin from https://raw2.github.com/pauliusm/check-hls-records/master/check-hls-records.py

Requirements
------------
Python 2.x, probably would work with 3.x, but untested (please send feedback).
Also you need `python-pycurl` package - get your OS's supported package, or via pip.

How it works?
-------------
Script fetches playlist content from wowza server, parses it, then fetches chunklist, then medialist, and finaly mpeg stream. If mpeg stream begins with 'G', it considers it valid, and exits returning 0 (OK).
In any other case it would return 2 (critical).
I know, it's not perfect, but for now works for me.

Usage
-----
Add to nrpe.cfg lines like:

````
command[check_stream_records]=/usr/lib64/nagios/plugins/check-hls-records.py recorder.tld stream 1 5
````

And setup service check in nagios config:
````
define service {
        service_description             NRPE_stream_records
        use                             <whatever template>
        host_name                       recorder.tld
        max_check_attempts              3
        check_command                   check_nrpe!check_stream_records!
}
````

BUGS
------------
There are some, for sure...


FAQ
---
`Q:` Will it works only on wowza?

`A:` For now yes, but could be easily adopted to work with other HLS VOD software.

