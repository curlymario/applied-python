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
    logfile = open('log.log', 'r')
    Logline = namedtuple('Logline', [
        'request_date',
        'request_time',
        'request_type',
        'request',
        'protocol',
        'response_code',
        'response_time'
    ])
    logstart = re.compile('\[[0-2][0-9]/[A-Za-z]{3}/[1-2][0-9]{3} [0-2][0-9]:[0-5][0-9]:[0-9][0-9]\]')
    parsed_log = set()
    for line in logfile.readlines():
        if logstart.match(line[0:22]):
            line_content = Logline(*line.replace('"','').split())
            parsed_log.add(line_content)
    return []

if __name__ == '__main__':
    parse()