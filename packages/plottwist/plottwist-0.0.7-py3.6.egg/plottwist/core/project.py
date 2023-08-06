#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains implementation for Plot Twist Artella project
"""

from __future__ import print_function, division, absolute_import

__author__ = "Tomas Poveda"
__license__ = "MIT"
__maintainer__ = "Tomas Poveda"
__email__ = "tpovedatd@gmail.com"

import webbrowser
try:
    from urllib.parse import quote
except ImportError:
    from urllib2 import quote

from artellapipe.core import project as artella_project

import plottwist
from plottwist.launcher import tray


class PlotTwist(artella_project.ArtellaProject):

    PROJECT_PATH = plottwist.get_project_path()
    TRAY_CLASS = tray.PlotTwistTray
    PROJECT_CONFIG_PATH = plottwist.get_project_config_path()
    PROJECT_SHELF_FILE_PATH = plottwist.get_project_shelf_path()
    PROJECT_MENU_FILE_PATH = plottwist.get_project_menu_path()

    def __init__(self, resource=None):

        self._project_url = None
        self._documentation_url = None
        self._kitsu_url = None
        self._drive_url = None
        self._emails = list()

        super(PlotTwist, self).__init__(resource=resource)

    def init_config(self):
        super(PlotTwist, self).init_config()

        project_config_data = self.get_config_data()
        if not project_config_data:
            return

        self._project_url = project_config_data.get('PROJECT_URL', None)
        self._documentation_url = project_config_data.get('PROJECT_DOCUMENTATION_URL', None)
        self._kitsu_url = project_config_data.get('PROJECT_KITSU_URL', None)
        self._drive_url = project_config_data.get('PROJECT_DRIVE_URL', None)
        self._emails = project_config_data.get('EMAILS', list())

    @property
    def project_url(self):
        """
        Returns URL to official Plot Twist web page
        :return: str
        """

        return self._project_url

    @property
    def documentation_url(self):
        """
        Returns URL where Plot Twist documentation is stored
        :return: str
        """

        return self._documentation_url

    @property
    def kitsu_url(self):
        """
        Returns URL that links to Kitsu production tracker
        """

        return self._kitsu_url

    @property
    def drive_url(self):
        """
        Returns URL that links to Drive
        :return: str
        """

        return self._drive_url

    @property
    def emails(self):
        """
        Returns list of emails that will be used when sending an email
        :return: list(str)
        """

        return self._emails

    def open_webpage(self):
        """
        Opens Plot Twist official web page in browser
        """

        if not self._project_url:
            return

        webbrowser.open(self._project_url)

    def open_documentation(self):
        """
        Opens Plot Twist documentation web page in browser
        """

        if not self._documentation_url:
            return

        webbrowser.open(self._documentation_url)

    def open_kitsu(self):
        """
        Opens Plot Twist Kitsu web page in browser
        """

        if not self._kitsu_url:
            return

        webbrowser.open(self._kitsu_url)

    def open_drive(self):
        """
        Opens Plot Twist Drive web page in browser
        """

        if not self._drive_url:
            return

        webbrowser.open(self._drive_url)

    def send_email(self, title=None):
        """
        Opens email application with proper info
        """

        if not title:
            title = self.name.title()

        webbrowser.open("mailto:%s?subject=%s" % (','.join(self._emails), quote(title)))

