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
        path = self.absFilePath
        f = None
        ctype = self.guess_type(path)
        fName = _path.basename(path)
        try:
            f = open(path, 'rb')
        except OSError:
            self.send_error(404, "File not found")
            return None
        try:
            self.send_response(200)
            self.send_header("Content-type", ctype)
            fs = _os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs[6]))
            self.send_header("Content-Disposition",
                             "attachment; filename='" + fName + "'")
            self.send_header("Last-Modified",
                             self.date_time_string(fs.st_mtime))
            self.end_headers()
            return f
        except:
            f.close()
            raise


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
        _sys.stdout.write(u"Couldn't find/access file: " + args.file)
        _sys.exit(-1)

    tryDefaultPorts = args.port == 0

    # Code from http.server in Python3
    handler = FileHTTPServerHandler
    handler.protocol_version = "HTTP/1.0"
    handler.absFilePath = absFilePath

    try:
        server_address = ("", 80 if tryDefaultPorts else args.port)
        httpd = _B.HTTPServer(server_address, handler)
    except IOError as e:
        # If it is a permission denied error, and we had been ambitiously
        # trying port, 80, let's try port 8000 instead
        if e.errno == 13 and tryDefaultPorts:
            server_address = ("", 8000)
            httpd = _B.HTTPServer(server_address, handler)
        else:
            raise

    sa = httpd.socket.getsockname()
    print("Serving file {} on {}:{} ...".format(absFilePath, sa[0], sa[1]))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        httpd.server_close()
        _sys.exit(0)
