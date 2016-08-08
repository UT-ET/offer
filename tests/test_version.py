#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of offer.
# https://github.com/musically-ut/offer

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Utkarsh Upadhyay <musically.ut@gmail.com>

from preggy import expect

from offer import __version__
from tests.base import TestCase


class VersionTestCase(TestCase):
    def test_has_proper_version(self):
        expect(__version__).to_equal('0.2.1')
