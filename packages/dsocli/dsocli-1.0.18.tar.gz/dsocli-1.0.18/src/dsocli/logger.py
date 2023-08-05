import os
import logging
# import re
# from time import gmtime, strftime

COLORIZE_LOGS = os.getenv('DSO_COLORIZE_LOGS') or True
BOLD_LOGS = os.getenv('DSO_BOLD_LOGS') or True
TIMESTAMP_LOGS = os.getenv('DSO_TIMESTAMP_LOGS') or True
LABEL_LOG_LEVELS = os.getenv('DSO_LABEL_LOG_LEVELS') or True

COLOR_CODES = {
    'black': u'0;30', 
    'bright gray': u'0;37',
    'blue': u'0;34', 
    'white': u'1;37',
    'green': u'0;32', 
    'bright blue': u'1;34',
    'cyan': u'0;36', 
    'bright green': u'1;32',
    'red': u'0;31', 
    'bright cyan': u'1;36',
    'purple': u'0;35', 
    'bright red': u'1;31',
    'yellow': u'0;33', 
    'bright purple': u'1;35',
    'dark gray': u'1;30', 
    'bright yellow': u'1;33',
    'magenta': u'0;35', 
    'bright magenta': u'1;35',
    'normal': u'0',
}

log_levels = {
    'error': 0, ### logs only errors
    'warning': 1, ### logs also warnings
    'info': 2, ### logs also information
    'debug': 3, ### logs also debug information
    'full': 4, ### logs also unhandled exception
}

logger_verbosity_map = {
    '0': logging.ERROR,
    '1': logging.WARNING,
    '2': logging.INFO,
    '3': logging.DEBUG,
    '4': logging.DEBUG,
}

style_codes = {
    'normal': '\033[0m',
    'bold': '\033[1m',
    'reset': '\033[0m',
}

color_codes = {
    'uncolored': {
        'normal': '\033[0m',
        'bold': '\033[1m',
    },
    'white': {
        'normal': '\033[{0}m'.format(COLOR_CODES['white']),
        'bold': '\033[{0}m\033[1m'.format(COLOR_CODES['white']),
    },
    'green': {
        'normal': '\033[{0}m'.format(COLOR_CODES['green']),
        'bold': '\033[{0}m\033[1m'.format(COLOR_CODES['green']),
    },
    'yellow': {
        'normal': '\033[{0}m'.format(COLOR_CODES['yellow']),
        'bold': '\033[{0}m\033[1m'.format(COLOR_CODES['yellow']),
    },
    'red': {
        'normal': '\033[{0}m'.format(COLOR_CODES['red']),
        'bold': '\033[{0}m\033[1m'.format(COLOR_CODES['red']),
    },
    'debug': {
        'normal': '\033[{0}m'.format(COLOR_CODES['blue']),
        'bold': '\033[{0}m\033[1m'.format(COLOR_CODES['blue']),
    },
    'info': {
        'normal': '\033[{0}m'.format(COLOR_CODES['green']),
        'bold': '\033[{0}m\033[1m'.format(COLOR_CODES['green']),
    },
    'warning': {
        'normal': '\033[{0}m'.format(COLOR_CODES['yellow']),
        'bold': '\033[{0}m\033[1m'.format(COLOR_CODES['yellow']),
    },
    'error': {
        'normal': '\033[{0}m'.format(COLOR_CODES['red']),
        'bold': '\033[{0}m\033[1m'.format(COLOR_CODES['red']),
    },
}

# ###--------------------------------------------------------------------------------------------
# ###--------------------------------------------------------------------------------------------

# def decode_color_codes(s):
#     r = re.findall("{0}(.*?){1}(.*?){2}".format(re.escape('<?'), re.escape('>'), re.escape('</?>')), s)
#     for c in r:
#         d = format_text(c[1], c[0])
#         s = s.replace('<?{0}>{1}</?>'.format(c[0], c[1]), d)
#     return s


###--------------------------------------------------------------------------------------------
###--------------------------------------------------------------------------------------------


def format_text(msg, color):
    """Given a string add necessary codes to format the string."""
    style = 'bold' if BOLD_LOGS else 'normal'
    if COLORIZE_LOGS:
        return '{0}{1}{2}'.format(color_codes[color][style], msg, style_codes['reset'])
    else:
        return '{0}{1}{2}'.format(color_codes['uncolored'][style], msg, style_codes['reset'])

###--------------------------------------------------------------------------------------------
###--------------------------------------------------------------------------------------------


class LoggerClass():

    @property
    def level(self):
        return int(self.__level)

    def __init__(self, log_level):
        self.__level = log_level
        log_format = ''
        if TIMESTAMP_LOGS: log_format += '%(asctime)s'
        if LABEL_LOG_LEVELS: log_format += ' [%(levelname)-7s]'
        log_format += ' %(message)s'
        logging.basicConfig(format=log_format, datefmt='%Y-%m-%d %H:%M:%S', level=logger_verbosity_map[str(log_level)])

    def set_verbosity(self, log_level):
        self.__level = log_level
        logging.basicConfig(level=logger_verbosity_map[str(log_level)])

    def error(self, msg, force=True):
        if force or self.level >= log_levels['error']: 
            saveLevel = logging.root.level
            try:
                logging.root.level=logging.DEBUG
                logging.error(format_text(msg, 'error'))
            finally:
                logging.root.level=saveLevel

    def warn(self, msg, force=False):
        if force or self.level >= log_levels['warning']: 
            saveLevel = logging.root.level
            try:
                logging.root.level=logging.DEBUG
                logging.warning(format_text(msg, 'warning'))
            finally:
                logging.root.level=saveLevel

    def info(self, msg, stress=True, force=False):
        if force or self.level >= log_levels['info']: 
            saveLevel = logging.root.level
            try:
                logging.root.level=logging.DEBUG
                logging.info(format_text(msg, 'info'))
            finally:
                logging.root.level=saveLevel

    ###--------------------------------------------------------------------------------------------

    ### log debug message if (requested) log_level is greater than LOG_LEVEL_debug
    def debug(self, msg, force=False):
        if force or self.level >= log_levels['debug']: 
            saveLevel = logging.root.level
            try:
                logging.root.level=logging.DEBUG
                logging.debug(format_text(msg, 'debug'))
            finally:
                logging.root.level=saveLevel

    ###--------------------------------------------------------------------------------------------

    # ### always log
    # def force(self, msg, stress=True):
    #     saveLevel = logging.root.level
    #     try:
    #         logging.root.level=logging.DEBUG
    #         logging.info(format_text(msg, 'bold' if stress else 'normal'))
    #     finally:
    #         logging.root.level=saveLevel


###--------------------------------------------------------------------------------------------
###--------------------------------------------------------------------------------------------

# boto3.set_stream_logger('boto3.resources', logging.ERROR)

Logger = LoggerClass(log_levels['warning'])

