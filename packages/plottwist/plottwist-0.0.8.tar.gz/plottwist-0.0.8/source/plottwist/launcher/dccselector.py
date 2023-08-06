#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains DCC Selector implementation for Plot Twist
"""

from __future__ import print_function, division, absolute_import

__author__ = "Tomas Poveda"
__license__ = "MIT"
__maintainer__ = "Tomas Poveda"
__email__ = "tpovedatd@gmail.com"

import plottwist
from artellalauncher.widgets import dccselector


class PlotTwistDCCSelector(dccselector.DCCSelector, object):
    def __init__(self, launcher, parent=None):
        super(PlotTwistDCCSelector, self).__init__(launcher=launcher, parent=parent)

    def ui(self):
        super(PlotTwistDCCSelector, self).ui()

        selector_logo = plottwist.resource.pixmap(name='launcher_logo', extension='png')
        self.add_logo(selector_logo)

    def _get_title_pixmap(self):
        return plottwist.resource.pixmap(name='plottwist_title', extension='png')