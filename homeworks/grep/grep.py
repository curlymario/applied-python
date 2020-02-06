
import argparse
import sys
import re


def output(line):
    print(line)


def pattern_match(pattern, line):
    if pattern.search(line) is not None:
        return True
    else:
        return False

def pattern_compile(params):
    pattern_string = params.pattern

    if '*' in pattern_string:
        pattern_string = pattern_string.replace('*', '.*')
    if '?' in pattern_string:
        pattern_string = pattern_string.replace('?', '.')
    if params.invert:
        pattern_string = f'^((?!{pattern_string}).)*$'
    if params.ignore_case:
        return re.compile(pattern_string, re.I)
    else:
        return re.compile(pattern_string)

def count_lines(lines, pattern):
    line_count = 0
    for line in lines:
        line = line.rstrip()
        if pattern_match(pattern, line):
            line_count += 1
    return line_count

def enumerate_line(i, line):
    return f'{i + 1}:{line}'

def enumerate_context(i, line):
    return f'{i + 1}-{line}'

def output_context(num, lines, used, pattern, params):
    if len(lines) >= num + 1:
        context = lines[num].rstrip()
        if context not in used:
            used.append(context)
            if not pattern_match(pattern, context):
                if params.line_number:
                    context = enumerate_context(num, context)
                output(context)

def grep(lines, params):
    pattern = pattern_compile(params)
    if params.count:
        line_count = count_lines(lines, pattern)
        output(str(line_count))
    else:
        N = params.context or params.before_context or params.after_context or 0
        used = []
        for i, line in enumerate(lines):
            line = line.rstrip()
            if pattern_match(pattern, line):

                if params.context or params.before_context:
                    for j in range(-N, 0):
                        num = i + j
                        output_context(num, lines, used, pattern, params)

                if params.line_number:
                    line = enumerate_line(i, line)
                output(line)

                if params.context or params.after_context:
                    for j in range(1, N+1):
                        num = i + j
                        output_context(num, lines, used, pattern, params)


def parse_args(args):
    parser = argparse.ArgumentParser(description='This is a simple grep on python')
    parser.add_argument(
        '-v',
        action="store_true",
        dest="invert",
        default=False,
        help='Selected lines are those not matching pattern.')
    parser.add_argument(
        '-i',
        action="store_true",
        dest="ignore_case",
        default=False,
        help='Perform case insensitive matching.')
    parser.add_argument(
        '-c',
        action="store_true",
        dest="count",
        default=False,
        help='Only a count of selected lines is written to standard output.')
    parser.add_argument(
        '-n',
        action="store_true",
        dest="line_number",
        default=False,
        help='Each output line is preceded by its relative line number in the file, starting at line 1.')
    parser.add_argument(
        '-C',
        action="store",
        dest="context",
        type=int,
        default=0,
        help='Print num lines of leading and trailing context surrounding each match.')
    parser.add_argument(
        '-B',
        action="store",
        dest="before_context",
        type=int,
        default=0,
        help='Print num lines of trailing context after each match')
    parser.add_argument(
        '-A',
        action="store",
        dest="after_context",
        type=int,
        default=0,
        help='Print num lines of leading context before each match.')
    parser.add_argument(
        'pattern',
        action="store",
        help='Search pattern. Can contain magic symbols: ?*')
    return parser.parse_args(args)


def main():
    params = parse_args(sys.argv[1:])
    grep(sys.stdin.readlines(), params)


if __name__ == '__main__':
    main()
