# =============================================================================
# Minet CLI Utils
# =============================================================================
#
# Miscellaneous helpers used by the CLI tools.
#
import csv
from collections import namedtuple
from tqdm import tqdm


def safe_index(l, e):
    try:
        return l.index(e)
    except ValueError:
        return None


def custom_reader(f, target_header):

    reader = csv.reader(f)

    headers = next(reader, None)

    if isinstance(target_header, tuple):
        HeaderPositions = namedtuple('HeaderPositions', target_header)
        position = HeaderPositions(**{t: safe_index(headers, t) for t in target_header})
    else:
        position = safe_index(headers, target_header)

    return headers, position, reader


class DummyTqdmFile(object):
    """
    Dummy file-like that will write to tqdm. Taken straight from the lib's
    documentation: https://github.com/tqdm/tqdm but modified for minet use
    case regarding stdout piping.
    """
    file = None

    def __init__(self, file):
        self.file = file

    def write(self, x):
        # Avoid print() second call (useless \n)
        tqdm.write(x, file=self.file, end='')

    def flush(self):
        return self.file.flush()

    def close(self):
        pass
