# -*- encoding: utf-8 -*-

from typing import NamedTuple
import re
from datetime import datetime


class Log_entry(NamedTuple):
    request_date: datetime
    request_type: str
    request: tuple
    protocol: str
    response_code: int
    response_time: int


class Log_pattern(NamedTuple):
    datetime: re.Pattern
    schema: re.Pattern
    host: re.Pattern
    fullpath: re.Pattern
    path: re.Pattern
    file: re.Pattern


class Request(NamedTuple):
    schema: str
    host: str
    path: str


def define_patterns():
    datetime = re.compile('\[[0-2][0-9]/[A-Za-z]{3}/[1-2][0-9]{3} [0-2][0-9]:[0-5][0-9]:[0-9][0-9]\]')
    schema = re.compile('^.*(?=://)')
    host = re.compile('(?<=://).*?(?=/)')
    fullpath = re.compile('(?<=://)(?<=/)*.*')
    path = re.compile('(?<=/).*(?=\?)|(?<=/).*')
    file = re.compile('(?<=/).*\..*')
    return Log_pattern(datetime, schema, host, fullpath, path, file)


def convert_datetime(string):
    return datetime.strptime(string, '%d/%b/%Y %H:%M:%S')


def read_log(log_file, pattern):
    parsed_log = []
    for string in log_file.readlines():
        if pattern.datetime.match(string[0:22]):
            _date, _time, _type, _request, _protocol, _r_code, _r_time = string.replace('"', '').split()
            _date = _date.replace('[', '')
            _time = _time.replace(']', '')
            _schema = pattern.schema.search(_request).group(0)
            _host = pattern.host.search(_request).group(0)
            _fullpath = pattern.fullpath.search(_request).group(0)
            _path = pattern.path.search(_fullpath).group(0)

            entry = Log_entry(
                request_date=convert_datetime(' '.join((_date, _time))),
                request_type=_type,
                request=Request(_schema, _host, _path),
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
    parsing_patterns = define_patterns()
    log_file = open('log.log', 'r')
    log = read_log(log_file, parsing_patterns)

    return []


if __name__ == '__main__':
    parse()
