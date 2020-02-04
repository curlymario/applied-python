
import argparse
import sys


def output(line):
    print(line)


def pattern_match(line, params):
    if (not params.invert and params.pattern in line) or (
            params.invert and not params.pattern in line):
        return True

def count_lines(lines, params):
    line_count = 0
    for line in lines:
        line = line.rstrip()
        if pattern_match(line, params):
            line_count += 1
    return line_count

def grep(lines, params):
    if params.count:
        line_count = count_lines(lines, params)
        output(str(line_count))
    else:
        for line in lines:
            line = line.rstrip()
            if pattern_match(line, params):
                output(line)



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
