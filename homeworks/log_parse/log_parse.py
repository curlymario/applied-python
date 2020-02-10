# -*- encoding: utf-8 -*-

from collections import namedtuple
import re


def parse(
        ignore_files=False,
        ignore_urls=[],
        start_at=None,
        stop_at=None,
        request_type=None,
        ignore_www=False,
        slow_queries=False
):
    log_file = open('log.log', 'r')
    Log_entry = namedtuple('Log_entry', [
        'request_date',
        'request_time',
        'request_type',
        'request',
        'protocol',
        'response_code',
        'response_time'
    ])
    log_start = re.compile('\[[0-2][0-9]/[A-Za-z]{3}/[1-2][0-9]{3} [0-2][0-9]:[0-5][0-9]:[0-9][0-9]\]')
    parsed_log = set()
    for string in log_file.readlines():
        if log_start.match(string[0:22]):
            entry = Log_entry(*string.replace('"', '').split())
            parsed_log.add(entry)
    return []


if __name__ == '__main__':
    parse()
