# -*- coding: utf-8 -*-
import logging
import json
import time


def handler(event, context):
    evt = json.loads(event)
    logging.info(evt)
    time.sleep(60)
    return evt