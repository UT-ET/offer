offer
=====

|BuildStatus|

Quickly *offer* a file for download on LAN.

Usage
-----

::

    pip install offer

Then you can use it from the CLI:

::

    offer ~/path/file.ext

It'll try to host the file on port ``80`` by default and will fall back on port
``8000`` silently if it is not run with the correct permissions. You can provide
a custom port via the ``--port`` argument.

Then from another computer/tablet/phone, you can either point the browser at
the IP address printed out or use `curl`.

Note about cURL
---------------

Remember to use the `-L` flag with cURL to follow redirects.

.. |BuildStatus| image:: https://travis-ci.org/musically-ut/offer.svg?branch=master
   :target: https://travis-ci.org/musically-ut/offer
