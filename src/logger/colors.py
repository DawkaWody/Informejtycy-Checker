import sys
use_colors = sys.stdout.isatty()

class Color:
    NORMAL = "\033[0m" if use_colors else ""
    FROM = "\033[38:5:247m" if use_colors else ""

    SPAM = "\033[38:5:70m" if use_colors else ""
    SPAM_ID = 0
    DEBUG = "\033[38:5:207m" if use_colors else ""
    DEBUG_ID = 1
    WARNING = "\033[38:5:99m" if use_colors else ""
    WARNING_ID = 2
    ALERT = "\033[38:5:214m" if use_colors else ""
    ALERT_ID = 3
    ERROR = "\033[38:5:160m" if use_colors else ""
    ERROR_ID = 4
    INFO = "\033[38:5:27m" if use_colors else ""
    INFO_ID = 5
