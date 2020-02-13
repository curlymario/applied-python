# -*- encoding: utf-8 -*-

from typing import NamedTuple
import re
import datetime


class Log_entry(NamedTuple):
    request_date: str
    request_type: str
    request: tuple
    protocol: str
    response_code: int
    response_time: int


def read_log(log_file):
    log_start = re.compile('\[[0-2][0-9]/[A-Za-z]{3}/[1-2][0-9]{3} [0-2][0-9]:[0-5][0-9]:[0-9][0-9]\]')
    schema_pattern = re.compile('^.*:(?=//)')
    parsed_log = []
    for string in log_file.readlines():
        if log_start.match(string[0:22]):
            _date, _time, _type, _request, _protocol, _r_code, _r_time = string.replace('"', '').split()
            _date = _date.replace('[', '')
            _time = _time.replace(']', '')
            _schema = schema_pattern.search(_request)
            entry = Log_entry(
                request_date=' '.join((_date, _time)),
                request_type=_type,
                request=(_schema, ),
                protocol=_protocol,
                response_code=int(_r_code),
                response_time=int(_r_time)
            )
            parsed_log.append(entry)
    return parsed_log


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
    log = read_log(log_file)

    return []


if __name__ == '__main__':
    parse()
