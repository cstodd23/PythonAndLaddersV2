import logging
from datetime import datetime
import atexit


class AggregationHandler(logging.Handler):
    def __init__(self, stream=None):
        super().__init__()
        self.record = None
        self.current_message = 'No current Messages'
        self.last_message = 'No Last Messages'
        self.count = 0
        self.stream = stream or logging.StreamHandler().stream
        self.terminator = '\n'
        atexit.register(self.flush)

    def emit(self, record):
        try:
            self.record = record
            self.flush()
        except Exception:
            self.handleError(record)

    def flush(self):
        try:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S ')
            current_message = self.format(self.record)
            if self.last_message == current_message:
                self.count += 1
            else:
                self.count += 1
                if self.count > 1:
                    output_message = f'{self.last_message} (x{self.count})'
                else:
                    output_message = self.last_message
                self.last_message = current_message
                self.stream.write(current_time + output_message + self.terminator)
                self.stream.flush()
                self.count = 0
                # self.message_counts.clear()
        except Exception as e:
            print(f"DEBUG: flush exception - {e}")


class ColorFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[94m',
        'INFO': '\033[93m',
        'WARNING': '\033[95m',
        'ERROR': '\033[31m',
        'CRITICAL': '\033[91m',
        'ENDC': '\033[0m',
    }

    def format(self, record):
        color = self.COLORS.get(record.levelname, self.COLORS['ENDC'])
        record.msg = f"{color}{record.msg}{self.COLORS['ENDC']}"
        return super().format(record)


def setup_logger(name, debug=False):
    log = logging.getLogger(name)
    if debug:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)

    agg_handler = AggregationHandler()
    agg_handler.setLevel(logging.DEBUG)

    formatter = ColorFormatter('%(name)s - %(levelname)s - %(message)s')
    agg_handler.setFormatter(formatter)

    log.addHandler(agg_handler)
    return log


def func_logger(f, c, m):
    logger.debug(f'File: {f}, In Class: {c}, Using Method: {m}')


logger = setup_logger(__name__, debug=True)
