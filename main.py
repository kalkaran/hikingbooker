#!/usr/bin/env python3

import requests
import re
import sys
import configparser

def get_csfr_token(text):
    m = re.search('name="csfr_token" value="([^"]+)"'), text)
    return m.group(1)

def login(session, url, password):
    r = session.get(url)
    r.raise_for_status()
    get_csfr_token(r.text)

