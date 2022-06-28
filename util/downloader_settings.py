from PyQt5.QtCore import QSettings
from util.const import *
from util.logger import send_to_log

DEFAULT_SETTINGS = {"destiny_folder": Paths.DOWNLOAD_DIR,
                    "max_workers": AppSettings.WORKERS,
                    "max_threads": AppSettings.THREADS,
                    "attemps_limit": AppSettings.RETRY,
                    "if_file_exists": 0,
                    "on_stop": 0,
                    "alert_on_finish": True,
                    "alert_sound": Paths.DOWNLOAD_DIR}
# QSettings object
DOWNLOADER_SETTINGS = QSettings(AppInfo.ID, "Download Manager")


# Save settings method
def save_settings(key, value):
    DOWNLOADER_SETTINGS.setValue(key, value)
    DOWNLOADER_SETTINGS.sync()


# Restore by default settings method
def restore_by_default():
    try:
        for key in DEFAULT_SETTINGS.keys():
            if DOWNLOADER_SETTINGS.value(key) is None:
                save_settings(key, DEFAULT_SETTINGS[key])
    except Exception as e:
        print("Error reestableciendo configuracion")
        send_to_log(f"Reestableciendo configuracion {e.args}")


restore_by_default()


def restore_one_by_default(setting: str):
    try:
        save_settings(setting, DEFAULT_SETTINGS[setting])
    except Exception as e:
        print(f"Error reestableciendo configuracion para {setting}")
        send_to_log(f"Error reestableciendo configuracion para {setting}")
