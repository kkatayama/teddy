"""

teddy - A utilities library for my python projects

=======
Methods
=======
get_length_itertools(iter_type, iter_obj, iter_size)
    Returns the total number of iterable items.

"""
import re
import os
import sys
import logging
import coloredlogs
from rich import print
from chardet.universaldetector import UniversalDetector
from logging.handlers import TimedRotatingFileHandler
from math import factorial as mf
from lucidic import Lucidic
# import markdown

# -- CONFIGS -- #
MODULE = coloredlogs.find_program_name()
LOG_FILE = 'logs/{}.log'.format(os.path.splitext(MODULE)[0])
field_styles = {
    'asctime': {'color': 221, 'bright': True},
    'programname': {'color': 45, 'faint': True},
    'funcName': {'color': 177, 'normal': True},
    'lineno': {'color': 'cyan', 'bright': True}
}
level_styles = {
    "debug": {'color': 'green', 'bright': True},
    "info": {'color': 'white', 'bright': True},
    "warning": {'color': "yellow", 'normal': True},
    "error": {'color': "red", 'bright': True},
    "critical": {'color': 'red', 'bold': True, 'background': 'red'}
}
log_format = "%(asctime)s: [%(programname)s: %(funcName)s();%(lineno)s] %(message)s"
console = Console()


def getFileHandler():
    log_file_formatter = coloredlogs.ColoredFormatter(log_format, field_styles=field_styles, level_styles=level_styles)
    log_file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
    log_file_handler.addFilter(coloredlogs.ProgramNameFilter())
    log_file_handler.setFormatter(log_file_formatter)
    return log_file_handler


def getLogger():
    # -- CREATE LOGGER -- #
    logger = logging.getLogger(MODULE)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(getFileHandler())
    coloredlogs.install(level='DEBUG', fmt=log_format, field_styles=field_styles, level_styles=level_styles)
    return logger


def getInfo(obj, unique_value, desired_keys):
    idx = Lucidic(obj)
    idx_q = idx.search(unique_value, strict=True)
    info = {}
    for key in desired_keys:
        kdx   = Lucidic(obj)
        kdx_q = kdx.search(key)
        for k in kdx_q:
            if k['keypath'] == idx_q[0]['keypath']:
                info.update(idx_q[0]['match'])
                info.update(k['match'])
    return info


def convert_bytes(number_in_bytes):
    '''
    ### USAGE ###
    from teddy import convert_bytes

    print(convert_bytes(10248000))

    9.77 MB
    '''
    tags = [ "B", "KB", "MB", "GB", "TB" ]

    i = 0
    double_bytes = number_in_bytes

    while (i < len(tags) and  number_in_bytes >= 1024):
            double_bytes = number_in_bytes / 1024.0
            i = i + 1
            number_in_bytes = number_in_bytes / 1024

    return str(round(double_bytes, 2)) + " " + tags[i]


def split_string(line, n):
    return [line[i:i+n] for i in range(0, len(line), n)]


def print_header(item, size=0, tab=4, log=False):
    item = str(item)
    size = size if size else tab + len(item) + tab
    header = '+{}+\n|{:^{size}}|\n+{}+'.format('-'*size, item, '-'*size, size=size)

    if log:
        return header
    print(header)


def xor2(s1, s2):
    c_max = max(s1, s2)
    c_min = min(s1, s2)
    i_min = 0
    r = ''
    for i_max in range(len(c_max)):
        if i_min  == len(c_min):
            i_min = 0
        r += chr(ord(c_min[i_min])^ord(c_max[i_max]))
        i_min += 1
    return r


def binomail(n, r):
    return (mf(n)/(mf(r)*mf(n-r)))


def get_length_itertools(iter_type, iter_obj, iter_size):
    """
    Python's itertools module provides many utilities for handling iterable objects.
    However, it lacks the ability to provide a total number of items in an object.
    This method will return the total number of iterable items in an object.

    ==========
    Parameters
    ==========
    iter_type : str
        The type of itertools iterable object.
        ==============    ===============================================
        iter_type         example elements (iter_size = 2)
        ==============    ===============================================
        'combinations'    AB AC AD BC BD CD
        'permutations'    AB AC AD BA BC BD CA CB CD DA DB DC
        'product'         AA AB AC AD BA BB BC BD CA CB CC CD DA DB DC DD
        ==============    ===============================================
    iter_obj : str, list
        The object containing all possible items for itertools to populate.
    iter_size : int
        The number of elements in the subsequence of iterable object.

    =======
    Returns
    =======
    total : int
        The total number of subsequence iterable objects
    """

    candidates = len(iter_obj)
    if 'permutation' in iter_type:
        total = 1
        for i in range(iter_size):
            total *= (candidates - i)
    elif 'product' in iter_type:
        total = candidates ** iter_size
    elif 'combination' in iter_type:
        total = binomail(candidates, iter_size)
    return total


def js_minify(raw):
    modifiers = ['\n', '\t', '    ', '  ']
    for m in modifiers:
        raw = raw.replace(m, '')
    return raw.replace(' = ','=').replace(') {','){').replace(', ',',')


def find_cmd(cmd, find_all=False):
    cmds = []
    for cmd_path in filter(os.path.isdir, os.environ['PATH'].split(':')):
        if cmd.lower() in map(str.lower, os.listdir(cmd_path)):
            index = list(map(str.lower, os.listdir(cmd_path))).index(cmd.lower())
            bin_cmd = os.path.join(cmd_path, os.listdir(cmd_path)[index])
            if find_all:
                cmds += [bin_cmd]
            else:
                return bin_cmd
    return cmds


# -- taken from: "https://github.com/apsun/AniConvert/blob/master/aniconvert.py"
def process_handbrake_output(process):
    def print_err(message="", end="\n", flush=False):
        print(message, end=end, file=sys.stderr)
        if flush:
            sys.stderr.flush()

    pattern1 = re.compile(r"Encoding: task \d+ of \d+, (\d+\.\d\d) %")
    pattern2 = re.compile(
        r"Encoding: task \d+ of \d+, (\d+\.\d\d) % "
        r"\((\d+\.\d\d) fps, avg (\d+\.\d\d) fps, ETA (\d\dh\d\dm\d\ds)\)")
    percent_complete = None
    current_fps = None
    average_fps = None
    estimated_time = None
    prev_message = ""
    format_str = "Progress: {percent:.2f}% done"
    long_format_str = format_str + " (FPS: {fps:.2f}, average FPS: {avg_fps:.2f}, ETA: {eta})"
    try:
        while True:
            output = process.stdout.readline()
            if len(output) == 0:
                break
            output = output.rstrip()
            match = pattern1.match(output)
            if not match:
                continue
            percent_complete = float(match.group(1))
            match = pattern2.match(output)
            if match:
                format_str = long_format_str
                current_fps = float(match.group(2))
                average_fps = float(match.group(3))
                estimated_time = match.group(4)
            message = format_str.format(
                percent=percent_complete,
                fps=current_fps,
                avg_fps=average_fps,
                eta=estimated_time)
            print_err(message, end="")
            blank_count = max(len(prev_message) - len(message), 0)
            print_err(" " * blank_count, end="\r")
            prev_message = message
    finally:
        print_err(flush=True)


def getFileEncoding(file_name):
    detector = UniversalDetector()
    detector.reset()
    with open(file_name, 'rb') as f:
        for line in f:
            detector.feed(line)
            if detector.done:
                break
    detector.close()
    return detector.result


if __name__ == '__main__':
    option = sys.argv[1:]
    if option == 'emacs':
        print('')
