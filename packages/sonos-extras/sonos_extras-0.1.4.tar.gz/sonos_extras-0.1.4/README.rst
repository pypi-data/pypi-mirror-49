sonos_extras
============

.. image:: https://img.shields.io/pypi/v/sonos_extras.svg
    :target: https://pypi.python.org/pypi/sonos_extras
    :alt: Latest PyPI version

Some extra useful commands for Sonos systems, based on SoCo.

Usage
-----
Simple example::

    from sonos_extras import SonosExtras
    client = SonosExtras("192.168.1.10") # replace with your speaker's IP
    client.get_current_track_info()

Methods
^^^^^^^
stop_after() :  stops after the current track is finished

Installation
------------
::
    
    pip install sonos-extras

Requirements
^^^^^^^^^^^^
python 3.6

Compatibility
-------------

Python 3.6

Licence
-------
The MIT License (MIT)

Copyright (c) 2019 MaziarA

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Authors
-------

`sonos_extras` was written by `MaziarA <maziara2@gmail.com>`_.
