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
    url: str
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
            _url = pattern.fullpath.search(_request).group(0)
            _path = pattern.path.search(_url).group(0)

            entry = Log_entry(
                request_date=convert_datetime(' '.join((_date, _time))),
                request_type=_type,
                request=Request(_schema, _url, _host, _path),
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

    top_logs = {}
    for entry in log:
        if ignore_files and parsing_patterns.file.search(entry.request.path):
            continue
        if ignore_urls and entry.request.host in ignore_urls:
            continue
        if start_at and entry.request_date < convert_datetime(start_at):
            continue
        if stop_at and entry.request_date > convert_datetime(stop_at):
            continue
        if request_type and entry.request_type != request_type:
            continue

        url = entry.request.url
        if ignore_www:
            url = url.replace('www.', '')

        if slow_queries:
            if url in top_logs:
                top_logs[url]['count'] += 1
                top_logs[url]['time'] += entry.response_time
            else:
                top_logs[url] = {'count': 1, 'time': entry.response_time}
        else:
            if url in top_logs:
                top_logs[url] += 1
            else:
                top_logs[url] = 1

    if slow_queries:
        top_slowest = [int(top_logs[key]['time']/top_logs[key]['count']) for key in top_logs]
        top_slowest.sort(reverse=True)
        return top_slowest[:5]
    else:
        top_popular = [top_logs[key] for key in top_logs]
        top_popular.sort(reverse=True)
        return top_popular[:5]


if __name__ == '__main__':
    parse()
