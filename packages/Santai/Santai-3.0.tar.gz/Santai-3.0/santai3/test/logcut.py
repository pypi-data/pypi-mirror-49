__author__ = 'zoulida' #日志循环覆盖
import glob
import logging
import logging.handlers
LOG_FILENAME='logging_rotatingfile_example.out'
# Set up a specific logger with our desired output level
my_logger = logging.getLogger('MyLogger')
my_logger.setLevel(logging.DEBUG)
# Add the log message handler to the logger
handler = logging.handlers.RotatingFileHandler(LOG_FILENAME,
            maxBytes=50,#每个文件最大的size
            backupCount=5,#最大备份文件数量
           )
my_logger.addHandler(handler)
# Log some messages
for i in range(100):
    my_logger.debug('i = %d' % i)
    # See what files are created
    logfiles = glob.glob('%s*' % LOG_FILENAME)
for filename in logfiles:
    print (filename)