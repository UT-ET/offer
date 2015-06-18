#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of offer.
# https://github.com/musically-ut/offer

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Utkarsh Upadhyay <musically.ut@gmail.com>

import argparse as _argparse
import os as _os
import sys as _sys
import netifaces as _N
import urllib2 as _U2
_path = _os.path

try:
    import BaseHTTPServer as _B
    import SimpleHTTPServer as _S
    SimpleHTTPRequestHandler = _S.SimpleHTTPRequestHandler
except ImportError:
    import http.server as _B
    SimpleHTTPRequestHandler = _B.SimpleHTTPRequestHandler


class FileHTTPServerHandler(SimpleHTTPRequestHandler):

    absFilePath = None

    # @Overriding
    def send_head(self):
        """Common code for GET and HEAD commands.

        This sends the response code and MIME headers.

        Return value is either a file object (which has to be copied
        to the outputfile by the caller unless the command was HEAD,
        and must be closed by the caller under all circumstances), or
        None, in which case the caller has nothing further to do.
        """

        offerredPath = self.absFilePath
        f = None
        fName = _path.basename(offerredPath)

        urlPath = _U2.unquote(self.path)
        if urlPath == '/':
            self.send_response(307)
            self.send_header("Location", "/" + _U2.quote(fName))
            self.end_headers()
            return None

        ctype = self.guess_type(offerredPath)
        try:
            f = open(offerredPath, 'rb')
        except OSError:
            self.send_error(404, "File not found")
            return None

        try:
            self.send_response(200)
            self.send_header("Content-type", ctype)
            fs = _os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs[6]))
            self.send_header("Content-Disposition", "attachment")
            self.send_header("Last-Modified",
                             self.date_time_string(fs.st_mtime))
            self.end_headers()
            return f
        except:
            f.close()
            raise

def getValidIPs():
    ips = []
    for iface in _N.interfaces():
        addrsDict = _N.ifaddresses(iface)
        if _N.AF_INET in addrsDict:
            for addrInfo in addrsDict[_N.AF_INET]:
                ip = addrInfo['addr']
                if not ip.startswith('127.0.0'):
                    ips.append(ip)

    return ips


def main():
    """Host a file."""

    description = """Host a file on the LAN."""

    argParser = _argparse.ArgumentParser(description=description)
    argParser.add_argument('file',
                           help='File to host')
    argParser.add_argument('-p', '--port',
                           help='Port to use. (default: 80/8000)',
                           type=int, default=0)

    args = argParser.parse_args()

    absFilePath = _path.abspath(_path.expandvars(_path.expanduser(args.file)))
    if not _path.isfile(absFilePath):
        _sys.stdout.write(u"Couldn't find/access file: " + args.file + "\n")
        _sys.exit(-1)

    tryDefaultPorts = args.port == 0

    # Code from http.server in Python3
    handler = FileHTTPServerHandler
    handler.protocol_version = "HTTP/1.0"
    handler.absFilePath = absFilePath

    port = 80 if tryDefaultPorts else args.port

    try:
        server_address = ("", port)
        httpd = _B.HTTPServer(server_address, handler)
    except IOError as e:
        # If it is a permission denied error, and we had been ambitiously
        # trying port, 80, let's try port 8000 instead
        if e.errno == 13 and tryDefaultPorts:
            port = 8000
            server_address = ("", port)
            httpd = _B.HTTPServer(server_address, handler)
        else:
            raise

    sa = httpd.socket.getsockname()
    _sys.stderr.write("Serving file {} on {}:{} ...\n"
                        .format(absFilePath, sa[0], sa[1]))

    possibleIps = getValidIPs()
    if len(possibleIps) == 0:
        _sys.stderr.write(u'No IPs for localhost found. ' +
                          u'Are you connected to LAN?\n')
    else:
        _sys.stderr.write(u'Download the file by pointing the browser ' +
                          u'on the remote machine to:\n')
        portStr = '' if port == 80 else ':' + str(port)
        for ip in possibleIps:
            _sys.stderr.write(u'\t' + ip + portStr + '\n')

    _sys.stderr.write('Press Ctrl-C to stop hosting.\n')

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        _sys.stderr.write("\nKeyboard interrupt received, exiting.\n")
        httpd.server_close()
        _sys.exit(0)
