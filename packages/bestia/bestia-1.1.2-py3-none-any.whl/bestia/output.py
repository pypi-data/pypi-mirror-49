from sys import getsizeof, stdout
from os.path import join as PATH_JOIN
from os import sep as PATH_SEPARATOR
from os import popen
from time import sleep

from termcolor import colored

from bestia.iterate import string_to_list, iterable_to_string, unique_random_items
from bestia.misc import command_output
from bestia.error import *

CHAR_SIZE = getsizeof('A')
ENCODING = 'utf-8'


def dquoted(s):
    return '"{}"'.format(s)


def clear_screen():
    ''' clears terminal '''
    print('\033[H\033[J')


def obfuscate_random_chars(input_string, amount=None, obfuscator='_'):
    ''' returns input string with amount of random chars obfuscated '''
    amount = len(input_string) - 4 if not amount or amount >= len(input_string) else amount

    string_indexes = [
        i for i in range(
            len(str(input_string))
        )
    ]

    string_as_list = string_to_list(input_string)
    for random_index in unique_random_items(string_indexes, amount):
        string_as_list[random_index] = obfuscator

    return iterable_to_string(string_as_list)


_STTY_BIN = command_output('which', 'stty').decode().strip()


def tty_size():
    ''' dinamically returns size of current terminal  '''
    if not _STTY_BIN:
        raise SttyBinMissing('stty bin NOT found')

    proc = popen('{} size'.format(_STTY_BIN), 'r')
    rows, columns = proc.read().split()
    return (int(rows), int(columns))


def tty_rows():
    ''' dinamically returns rows of current terminal '''
    return tty_size()[0]


def tty_columns():
    ''' dinamically returns columns of current terminal '''
    return tty_size()[1]


class Row():

    def __init__(self, *input_strings, width=None):

        self.fixed_width = width
        self.output_string = ''
        self.input_strings = list(input_strings)

        # input(self.width())

        # convert all to fstrings
        for i, string in enumerate(self.input_strings):
            if type(string) != FString:
                self.input_strings[i] = FString(string)

        # calculate TOTAL size left for adaptive strings 
        leftover_size = self.width()
        for fstring in self.input_strings:
            if fstring._explicit_size:
                # what if static_size strings remove more size than instantiated?
                leftover_size -= fstring.output_size

        # input(leftover_size)

        # gather adaptive strings
        adaptive_fstrings_count = len(
            [ fs for fs in self.adaptive_fstrings() ]
        )

        # calculate INDIVIDUAL size for each adaptive string + any leftover spaces
        if adaptive_fstrings_count:
            adaptive_fstrings_size, leftover_spaces = divmod(leftover_size, adaptive_fstrings_count)

        # input(adaptive_fstrings_count)
        # input(adaptive_fstrings_size)
        # input(leftover_spaces)

        # resize adaptive strings
        for i, _ in enumerate(self.input_strings):
            if not self.input_strings[i]._explicit_size:
                self.input_strings[i].resize(
                    adaptive_fstrings_size
                )

        # deal leftover_spaces to adaptive_strings 1 by 1
        while leftover_spaces:

            for i, _ in enumerate(self.input_strings):

                if self.input_strings[i]._explicit_size:
                    continue

                self.input_strings[i].resize(
                    self.input_strings[i].output_size +1
                )
                # self.input_strings[i].echo()
                # input(self.input_strings[i].output_size)
                leftover_spaces -= 1
                if not leftover_spaces:
                    break

        # build output_string
        for fs in self.input_strings:
            self.output_string = self.output_string + '{}'.format(fs)

    def adaptive_fstrings(self):
        for fs in self.input_strings:
            if not fs._explicit_size:
                yield fs

    def width(self):
        return self.fixed_width if self.fixed_width else tty_columns()

    def echo(self, *args, **kwargs):
        echo(self.output_string, *args, **kwargs)

    def append(self, string):
        if type(string) != FString:
            string = FString(string)
        self.output_string = self.output_string + '{}'.format(string)

    def __str__(self):
        return self.output_string


class echo():

    modes = (
        # first item is default
        'modern',
        'retro',
    )

    def __init__(self, input_string='', *args, **kwargs):
        self.output = input_string
        self.input_args = args

        self.__mode = self.modes[0]
        if 'mode' in kwargs.keys():
            if kwargs['mode'] in self.modes:
                self.__mode = kwargs['mode']

        self.set_colors()
        self()
        
    def __call__(self):
        if self.mode == 'modern':
            print(self.output)
        elif self.mode == 'retro':
            retro_put_string(self.output)

    @property
    def mode(self):
        return self.__mode

    def set_colors(self):
        self.fg_color = None
        self.bg_color = None

        available_colors = (
            'red',
            'green',
            'yellow',
            'blue',
            'grey',
            'white',
            'cyan',
            'magenta'
        )
        self.input_colors = [
            arg for arg in self.input_args if arg in available_colors
        ]

        if len(self.input_colors) == 1:
            self.fg_color = self.input_colors[0]
            self.output = colored(self.output, self.fg_color)
        elif len(self.input_colors) > 1:
            self.fg_color = self.input_colors[0]
            self.bg_color = self.input_colors[1]
            self.output = colored(self.output, self.fg_color, 'on_' + self.bg_color)



class FString():
    def __init__(self, input_string, size=False, align='l', pad=None, colors=[], fx=[]):

        self._explicit_size = True if size else False

        self.input_string = ''

        self.append(input_string)
        self.resize(size)

        self.pad = str(pad)[0] if pad else ' '      # improve this shit

        self.align = align			# l, r, cl, cr
        self.set_colors(colors) 	# grey, red, green, yellow, blue, magenta, cyan, white
        self.fx = fx				# bold, dark, underline, blink, reverse, concealed

    def resize(self, size=None):
        self.output_size = int(size) if size else self.input_size # desired len of output_string

    def append(self, string):
        self.input_string = self.input_string + '{}'.format(string)
        self.set_input_size()

    def set_input_size(self):
        # calculate input_string length without color bytes
        ignore_these = [
            b'\xe2\x80\x8e', # left-to-right-mark
            b'\xe2\x80\x8b', # zero-width-space
        ]
        color_start_byte = b'\x1b'
        color_end_byte = b'm'
        self.input_size = 0
        add = True
        for char in self.input_string:
        # when encoding input_string into byte_string: byte_string will not necessarily have the same amount of bytes as characters in the input_string ( some characters will be made of several bytes ), therefore, the input_string should not be encoded but EACH INDIVIDUAL CHAR should
        # for byte in self.input_string.encode():
            byte = char.encode()
            if byte == color_start_byte and add:
                add = False
                continue
            elif byte == color_end_byte and not add:
                add = True
                continue
            if add and byte not in ignore_these:
                self.input_size += 1

    def __str__(self):
        self.set_ouput_string()
        return self.output_string

    def __len__(self):
        return self.output_size

    def __add__(self, other):
        self.set_ouput_string()
        return self.output_string + '{}'.format(other)

    def echo(self, *args, **kwargs):
        return echo(self, *args, **kwargs)

    def set_colors(self, colors):
        if len(colors) > 1:
            colors[1] = colors[1].replace('on_', '')
            colors[1] = 'on_{}'.format(colors[1])
        self.colors = colors

    def set_pads(self):
        delta_length = self.output_size - self.input_size
        excess = delta_length % 2
        exact_half = int((delta_length - excess) / 2)
        self.small_pad = self.pad * exact_half
        self.big_pad = self.pad * (exact_half + excess)

    def set_ouput_string(self):
        self.output_string = self.input_string
        self.output_string = self.output_string.replace("\t", ' ') # can't afford to have tabs in output_string as they are never displayed the same
        if self.input_size > self.output_size:
            self.resize_output_string()
        self.color_output_string()
        if self.output_size > self.input_size:
            self.align_output_string()

    def resize_output_string(self):
        delta_length = self.input_size - self.output_size
        self.output_string = self.output_string[:0-delta_length]

    def align_output_string(self):
        self.set_pads()
        uno, due, tre = self.output_string, self.small_pad, self.big_pad
        # ASSUME "l" to avoid nasty fail...
        # but I should Raise an Exception if I pass invalid value "w"
        if self.align == 'cl' or self.align == 'lc' or self.align == 'c':
            uno, due, tre = self.small_pad, self.output_string, self.big_pad
        elif self.align == 'cr' or self.align == 'rc':
            uno, due, tre = self.big_pad, self.output_string, self.small_pad
        elif self.align == 'r':
            uno, due, tre = self.small_pad, self.big_pad, self.output_string

        self.output_string = '{}{}{}'.format(uno, due, tre)

    def color_output_string(self):
        if len(self.colors) == 1:
            self.output_string = colored(self.output_string, self.colors[0], attrs=self.fx)
        elif len(self.colors) == 2:
            self.output_string = colored(self.output_string, self.colors[0], self.colors[1], attrs=self.fx)


def expand_seconds(input_seconds, output_string=False):
    ''' expands input_seconds into a dict with as less keys as needed: 
            seconds, minutes, hours, days, weeks

        can also return string
    '''
    expanded_time = {}
    expanded_time['minutes'], expanded_time['seconds'] = divmod(input_seconds, 60)
    expanded_time['hours'], expanded_time['minutes'] = divmod(expanded_time['minutes'], 60)
    expanded_time['days'], expanded_time['hours'] = divmod(expanded_time['hours'], 24)
    expanded_time['weeks'], expanded_time['days'] = divmod(expanded_time['days'], 7)

    if output_string:
        seconds = ' {} seconds'.format(round(expanded_time['seconds'], 2))
        minutes = ' {} minutes'.format(int(expanded_time['minutes'])) if expanded_time['minutes'] else ''
        hours = ' {} hours'.format(int(expanded_time['hours'])) if expanded_time['hours'] else ''
        days = ' {} days'.format(int(expanded_time['days'])) if expanded_time['days'] else ''
        weeks = ' {} weeks'.format(int(expanded_time['weeks'])) if expanded_time['weeks'] else ''
        return '{}{}{}{}{}'.format(weeks, days, hours, minutes, seconds).strip()

    return expanded_time


def remove_path(input_path, deepness=-1):
    ''' removes directories from file path
        supports various levels of dir removal
    '''
    try:
        if deepness > 0:
            deepness = 0 - deepness
        elif deepness == 0:
            deepness = -1
        levels = []
        while deepness <= -1:
            levels.append(input_path.split(PATH_SEPARATOR)[deepness])
            deepness += 1
        return PATH_JOIN(*levels)
    except IndexError:
        return remove_path(input_path, deepness=deepness+1)


def replace_special_chars(t):
    ''' https://www.i18nqa.com/debug/utf8-debug.html
        some of the chars here im not sure are correct,
        check dumbo dublat romana translation
    '''
    special_chars = {
        # 'Äƒ': 'Ã',
        # 'Äƒ': 'ă',
        'Ã¢': 'â',
        'Ã¡': 'á', 'ã¡': 'á',
        'Ã ': 'à',
        'Ã¤': 'ä',
        'Å£': 'ã',
        # 'ÅŸ': 'ß',
        'ÃŸ': 'ß',
        'Ã©': 'é', 'ã©': 'é',
        'Ã¨': 'è',
        'Ã' : 'É', 'Ã‰': 'É',
        'Ã­': 'í',
        'Ã': 'Í',
        # 'Ã®': 'î',
        'Ã³': 'ó',
        'Ã“': 'Ó',
        'Ã¶': 'ö',
        'Ãº': 'ú',
        'Ã¹': 'ù',
        'Ã¼': 'ü',
        'Ã±': 'ñ',
        'Ã‘': 'Ñ',
        'Â´': '\'',
        '´': '\'',
        'â€ž': '“',
        'â€œ': '”',
        'â€¦': '…',
        b'\xe2\x80\x8e'.decode() : '', # left-to-right-mark
        b'\xe2\x80\x8b'.decode() : '',	# zero-width-space
        '&amp' : '&',
        '&;': '&',
        '【': '[',
        '】': ']',
        'â€“': '-',
    }

    for o, i in special_chars.items():
        t = t.replace(o, i)
    return t


def retro_put_char(char, lag=0):
    # randomize slightly
    sleep(lag)
    stdout.write(char)
    stdout.flush()


def retro_put_string(string):
    for c in [char for char in str(string)]:
        retro_put_char(c, lag=0.0005)
    retro_put_char('\n', lag=0.0005)


def screen(string='\n', color=None):
    if not DEBUG:
        return

    __colors = {
        'red' : '\033[31m',
        'green' : '\033[32m',
        'yellow' : '\033[33m',
        'blue' : '\033[34m',
        'magenta' : '\033[35m',
        'cyan' : '\033[36m',
        'reset': '\033[00m',
    }

    if color in __colors.keys():
        screen(__colors[color])

    for char in str(string):
        stdout.write(char)
        stdout.flush()

    if color in __colors.keys():
        screen(__colors['reset'])
