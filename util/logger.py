# >-------------------------------------------------- LOGGER ---------------------------------------------------------<
import logging

# create a directory if it does not exist
import os

from util.const import AppInfo

# log file address
log_file = os.path.join(os.getcwd(), f'{AppInfo.ID}.log')

if not os.path.isfile(log_file):
    with open(log_file, "w") as log_f:
        log_f.write("")

# define logging object
log_obj = logging.getLogger(AppInfo.NAME)
log_obj.setLevel(logging.INFO)

# create a file handler
handler = logging.FileHandler(log_file)
handler.setLevel(logging.DEBUG)

# create a logging format
logging.basicConfig(
    format='%(asctime)s %(levelname)s: %(message)s'
           ' - %(lineno)s: %(module)s',
    datefmt='%Y/%m/%d %H:%M:%S',
    filename=log_file, level=logging.INFO
)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
log_obj.addHandler(handler)


# print logs in the logfile
def send_to_log(text="", type="ERROR"):
    if type == "INFO":
        log_obj.info(text)
    elif type == "ERROR":
        log_obj.error(text)
    elif type == "CRITICAL":
        log_obj.critical(text)
    elif type == "DEBUG":
        log_obj.debug(text)
    else:
        log_obj.warning(text)


# print logs on console
def show_console_log(order, text, tab=0):
    strg = f"[{order}] {text}"

    if tab:
        strg = "\t" * tab + "- " + strg

    print(strg)
# > ------------------------------------------------------------------------------------------------------------------
