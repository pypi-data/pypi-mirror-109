About
-----
`python-mollusc` is a portable Python module to use the ClamAV anti-virus engine on 
Windows, Linux, MacOSX and other platforms. It requires a running instance of 
the `clamd` daemon.

This is a fork of https://github.com/graingert/python-clamd

Usage
-----

To use with a unix socket::

    >>> import clamd
    >>> cd = clamd.ClamdUnixSocket()
    >>> cd.ping()
    'PONG'
    >>> cd.version()                             # doctest: +ELLIPSIS
    'ClamAV ...
    >>> cd.reload()
    'RELOADING'

To scan a file::

    >>> open('/tmp/EICAR','wb').write(clamd.EICAR)
    >>> cd.scan('/tmp/EICAR')
    {'/tmp/EICAR': ('FOUND', 'Eicar-Test-Signature')}

To scan a stream::

    >>> from io import BytesIO
    >>> cd.instream(BytesIO(clamd.EICAR))
    {'stream': ('FOUND', 'Eicar-Test-Signature')}


License
-------
`python-mollusc` is released as open-source software under the LGPL license.

clamd Install
-------------
How to install the ClamAV daemon `clamd` under Ubuntu::

    sudo apt-get install clamav-daemon clamav-freshclam clamav-unofficial-sigs
    sudo freshclam
    sudo service clamav-daemon start
