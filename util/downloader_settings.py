from PyQt5.QtCore import QSettings
from util.const import *
from util.logger import SENT_TO_LOG

DEFAULT_SETTINGS = {"destiny_folder": DOWNLOAD_DIR,
                    "max_workers": WORKERS,
                    "max_threads": THREADS,
                    "attemps_limit": RETRY,
                    "if_file_exists": 0,
                    "on_stop": 0,
                    "alert_on_finish": True,
                    "alert_sound": DOWNLOAD_DIR}
# QSettings object
DOWNLOADER_SETTINGS = QSettings(APP_ID, "Download Manager")


# Save settings method
def SAVE_SETTINGS(key, value):
    DOWNLOADER_SETTINGS.setValue(key, value)
    DOWNLOADER_SETTINGS.sync()


# Restore by default settings method
def RESTORE_BY_DEFAULT():
    try:
        for key in DEFAULT_SETTINGS.keys():
            if DOWNLOADER_SETTINGS.value(key) is None:
                SAVE_SETTINGS(key, DEFAULT_SETTINGS[key])
    except Exception as e:
        print("Error reestableciendo configuracion")
        SENT_TO_LOG(f"Reestableciendo configuracion {e.args}")


RESTORE_BY_DEFAULT()


def RESTORE_ONE_BY_DEFAULT(setting: str):
    try:
        SAVE_SETTINGS(setting, DEFAULT_SETTINGS[setting])
    except Exception as e:
        print(f"Error reestableciendo configuracion para {setting}")
        SENT_TO_LOG(f"Error reestableciendo configuracion para {setting}")
