#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Safecast Tracker commands."""

import argparse
import json
import logging
import logging.handlers
import time

import requests

import safehook

__author__ = 'Greg Albrecht W2GMD <oss@undef.net>'
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2019 Greg Albrecht'


def setup_logging(log_level=None):
    """
    Sets up logging.

    :param log_level: Log level to setup.
    :type param: `logger` level.
    :returns: logger instance
    :rtype: instance
    """
    log_level = log_level or safehook.constants.LOG_LEVEL

    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(safehook.constants.LOG_FORMAT)
    logger.addHandler(console_handler)
    logger.propagate = False

    return logger


def sc_tracker():
    """Safecast Tracker Command Line interface for APRS."""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--debug', help='Enable debug logging', action='store_true'
    )
    parser.add_argument(
        '-m', '--mac_address', help='mac_address', required=True
    )
    parser.add_argument(
        '-i', '--interval', help='interval', default=0
    )
    parser.add_argument(
        '-w', '--webhook', help='webhook'
    )
    
    opts = parser.parse_args()

    if opts.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    logger = setup_logging(log_level)

    sc_p = safehook.BGeigieNanoPoller(opts.mac_address)
    sc_p.start()

    time.sleep(safehook.GPS_WARM_UP)

    try:
        while 1:
            gps_valid = sc_p.bgn_props['gps_valid'] == 'A'
            rad_valid = sc_p.bgn_props['rad_valid'] == 'A'

            if gps_valid and rad_valid:
                requests.post(opts.webhook, json=sc_p.bgn_props)

                if opts.interval == 0:
                    break
                else:
                    time.sleep(opts.interval)

    except KeyboardInterrupt:
        sc_p.stop()
    finally:
        sc_p.stop()
