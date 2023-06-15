import logging
import datetime

from .io_client import get_logfile

# Calculate the time adjustment
time_adjustment = datetime.timedelta(hours=9)
current_time = datetime.datetime.now()
adjusted_time = current_time + time_adjustment
time_format = adjusted_time.strftime('%Y-%m-%d %H:%M:%S')

formatter = logging.Formatter('%(levelname)s (%(asctime)s) : %(module)-17s : %(message)s', datefmt=time_format)

# Get logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Get logfile name & setup file handler
file_handler = logging.FileHandler(get_logfile())
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.WARN)

# Setup stream handler
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)

# Add handlers
logger.addHandler(file_handler)
logger.addHandler(stream_handler)












# import logging
# import datetime

# from .io_client import get_logfile

# # Calculate the time adjustment
# time_adjustment = datetime.timedelta(hours=9)
# current_time = datetime.datetime.now()
# adjusted_time = current_time + time_adjustment
# time_format = adjusted_time.strftime('%Y-%m-%d %H:%M:%S')

# formatter = logging.Formatter('%(module)-15s : %(levelname)-8s : %(asctime)s : %(message)s', datefmt=time_format)

# # Get logger
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)

# # Get logfile name & setup file handler
# file_handler = logging.FileHandler(get_logfile())
# file_handler.setFormatter(formatter)
# file_handler.setLevel(logging.WARN)

# # Setup stream handler
