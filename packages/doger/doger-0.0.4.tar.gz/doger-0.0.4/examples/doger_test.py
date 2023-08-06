# *_*coding:utf-8 *_*
'''
Descri：
'''
import datetime
import doger

LOG_FILE = "./logs/everything.log"
ERROR_LOG_FILE = "./logs/errors.log"
LOG_LEVEL = "DEBUG"
STREAM_LEVEL = "INFO"
STREAM_FORMAT = "%(color)s[LEVEL:%(levelno)s] %(message)s  \t\t\t\t--> [PID %(process)d] [%(filename)s:%(lineno)d]"
LOG_FORMAT = "[%(asctime)s] --> %(message)s <-- [%(filename)s:%(lineno)d] [%(levelname)s] [%(process)d] [%(threadName)s]"
ERROR_FORMAT = "[%(asctime)s] --> %(message)s <-- [%(filename)s:%(lineno)d] [%(levelname)s] [%(threadName)s]"


doger.setup(
    outputs=(
        doger.output.File(
            ERROR_LOG_FILE,
            level="ERROR",
            formatter=doger.formatter.ColorFormatter(
                fmt=ERROR_FORMAT
            ),
        ),
        doger.output.TimedRotatingFile(
            LOG_FILE,
            level=LOG_LEVEL,
            interval=datetime.timedelta(days=1),
            formatter=doger.formatter.ColorFormatter(
                fmt=LOG_FORMAT
            ),
        ),
        doger.output.Stream(
            level=STREAM_LEVEL,
            formatter=doger.formatter.ColorFormatter(
                fmt=STREAM_FORMAT
            ),
        ),
    ),
)

logger = doger.daiquiri(__name__)

logger.debug("the debug logger")
logger.info("only to rotating file logger")
logger.error("both log files, including errors only")
