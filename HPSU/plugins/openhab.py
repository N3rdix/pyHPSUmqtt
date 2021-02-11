#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# config inf conf_file (defaults):
# [OPENHAB]
# HOST = hostname_or_ip
# PORT = 8080
# ITEMPREFIX = Rotex_

import configparser
import requests
import sys
import os


class export():
    hpsu = None

    def __init__(self, hpsu=None, logger=None, config_file=None):
        self.hpsu = hpsu
        self.logger = logger
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        if os.path.isfile(self.config_file):
            self.config.read(self.config_file)
        else:
            sys.exit(9)

        # openhab hostname or IP
        if self.config.has_option('OPENHAB', 'HOST'):
            self.openhabhost = self.config['OPENHAB']['HOST']
        else:
            self.openhabhost = 'localhost'

        # openhab port
        if self.config.has_option('OPENHAB', 'PORT'):
            self.openhabport = int(self.config['OPENHAB']['PORT'])
        else:
            self.openhabport = 8080

        # openhab item name
        if self.config.has_option('OPENHAB', 'ITEMPREFIX'):
            self.openhabitemprefix = self.config['OPENHAB']['ITEMPREFIX']
        else:
            self.openhabitemprefix = 'Rotex_'

    def rest_send(self, item, value):
        url = "http://%s:%s/rest/items/%s%s/state" % (self.openhabhost, str(self.openhabport), self.openhabitemprefix, item)
        try:
            r = requests.put(url, data=str(value))
        except requests.exceptions.RequestException as e:
            rc = "ko"
            self.hpsu.logger.exception("Error " + str(e.code) + ": " + str(e.reason))

    def pushValues(self, vars=None):
        for r in vars:
            self.rest_send(r['name'], r['resp'])


    #if __name__ == '__main__':
    #    app = openhab()

    #    app.exec_()
