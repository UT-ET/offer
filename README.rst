seqfile
=======

|BuildStatus|

Quickly _offer_ a file for download on LAN.

Usage
-----

::

    pip install git+https://github.com/musically-ut/offer.git

Then you can use it from the CLI:

::

    offer ~/path/file.ext

It'll try to host the file on port `80` by default and will fall back on port
`8000` silently if it is not run with the correct permissions. You can provide
a custom port via the `--port` argument.

.. |BuildStatus| image:: https://travis-ci.org/musically-ut/offer.svg?branch=master
   :target: https://travis-ci.org/musically-ut/offer
