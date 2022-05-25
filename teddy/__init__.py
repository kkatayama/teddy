"""

teddy - A utilities library for my python projects

=======
Methods
=======
get_length_itertools(iter_type, iter_obj, iter_size)
    Returns the total number of iterable items.

"""
import logging
import os
import re
import sys
import time
import json
from logging.handlers import TimedRotatingFileHandler
from math import factorial as mf

import coloredlogs
import pandas as pd
from chardet.universaldetector import UniversalDetector
from lucidic import Lucidic
from rich import print

# import markdown

__version__ = "1.0.6"
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

###############################################################################
#                               Dictionary Utils                              #
###############################################################################
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


def uniqueDicts(obj):
    """
    Remove Duplicate Objects in a List of Dicts

    Args:
        obj: list - list of dictionary objects
    Returns:
        list: unique list of dictionary objects
    """
    return [json.loads(d) for d in set(json.dumps(r, sort_keys=True) for o in obj)]


def convert_bytes(number_in_bytes):
    """
    ### USAGE ###
    from teddy import convert_bytes

    print(convert_bytes(10248000))

    9.77 MB
    """
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


def camel_case_split(line):
    RE_WORDS = re.compile(r'''
        # Find words in a string. Order matters!
        [A-Z]+(?=[A-Z][a-z]) |  # All upper case before a capitalized word
        [A-Z]?[a-z]+ |  # Capitalized words / all lower case
        [A-Z]+ |  # All upper case
        \d+  # Numbers
    ''', re.VERBOSE)
    return [word.lower() for word in RE_WORDS.findall(line)]



def convertEPGTime(p_time="", dt_obj=False, epg_fmt=False):
    """Convert EPG Programme "start" and/or "stop" time from UTC to EST

    Note:
        Do not enable `dt_obj` and `epg_fmt` at the same time.
        Setting `dt_obj` takes precedence over `epg_fmt`.

    Args:
        p_time (str, datetime): The datetime string (or object) to convert
        dt_obj (:obj:`bool`, optional): Request datetime object. Default=False
        epg_fmt (bool, optional): Request epg formatted string. Default=False

    Returns:
        Converted EST time as a datetime or str object

    Examples:
        >>> convertEPGTime("20210803180000 +0000")
        '2021-08-03 02:00:00 PM'

        >>> convertEPGTime("20210803180000 +0000", epg_fmt=True)
        '20210803140000 -0400'

        >>> convertEPGTime("20210803180000 +0000", dt_obj=True)
        Timestamp('2021-08-03 14:00:00-0400', tz='US/Eastern')

    """
    est_dt = pd.to_datetime(p_time).tz_convert('US/Eastern')
    if dt_obj:
        return est_dt
    if epg_fmt:
        return est_dt.strftime("%Y%m%d%H%M%S %z")
    return est_dt.strftime("%Y-%m-%d %I:%M:%S %p")


def getEPGTimeNow(dt_obj=False, epg_fmt=False):
    """Return EPG Programme "start" and/or "stop" time based on current time (30 minute start)

    Args:
        dt_obj (:obj:`bool`, optional): Request datetime object. Default=False
        epg_fmt (bool, optional): Request epg formatted string. Default=False

    Returns:
        The current time as a datetime or str object

    Examples:
    >>> getEPGTimeNow()
    '2021-08-03 04:00:00 PM'

    >>> getEPGTimeNow(epg_fmt=True)
    '20210803160000 -0400'

    >>> getEPGTimeNow(dt_obj=True)
    Timestamp('2021-08-03 16:00:00-0400', tz='US/Eastern')
    """
    est_dt = pd.to_datetime(time.time(), unit='s', utc=True).tz_convert('US/Eastern').floor('30min')
    if dt_obj:
        return est_dt
    if epg_fmt:
        return est_dt.strftime("%Y%m%d%H%M%S %z")
    return est_dt.strftime("%Y-%m-%d %I:%M:%S %p")

def sha_sum(algorithm="sha256", url=""):
    r = requests.get(url)
    h = eval(f'hashlib.{algorithm}({r.content}).hexdigest()')
    size = len(r.content)
    return h, size

if __name__ == '__main__':
    option = sys.argv[1:]
    if option == 'emacs':
        print('')
