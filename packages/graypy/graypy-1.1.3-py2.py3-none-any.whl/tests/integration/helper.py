#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""helper functions for testing graypy with a local Graylog instance"""

from time import sleep
from uuid import uuid4

import requests


def get_unique_message():
    return str(uuid4())


DEFAULT_FIELDS = [
    "message", "full_message", "source", "level",
    "func", "file", "line", "module", "logger_name",
]

BASE_API_URL = 'http://127.0.0.1:9000/api/search/universal/relative?query=message:"{0}"&range=5&fields='


def get_graylog_response(message, fields=None):
    """Search for a given log message (with possible additional fields)
    within a local Graylog instance"""
    fields = fields if fields else []
    api_resp = _get_api_response(message, fields)
    return _parse_api_response(api_resp)


def _build_api_string(message, fields):
    return BASE_API_URL.format(message) + "%2C".join(set(DEFAULT_FIELDS + fields))


def _get_api_response(message, fields):
    sleep(2)
    url = _build_api_string(message, fields)
    api_response = requests.get(
        url,
        auth=("admin", "admin"),
        headers={"accept": "application/json"}
    )
    return api_response


def _parse_api_response(api_response):
    assert api_response.status_code == 200
    print(api_response.json())
    messages = api_response.json()["messages"]
    assert 1 == len(messages)
    return messages[0]["message"]
