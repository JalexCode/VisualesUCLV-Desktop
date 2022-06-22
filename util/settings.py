from PyQt5.QtCore import QSettings

from util.const import AppInfo
from util.logger import send_to_log

DEFAULT_SETTINGS = {"last_modification_date": ""}
# QSettings object
GENERAL_SETTINGS = QSettings(AppInfo.ID, "Explorer")


# Save settings method
def save_settings(key, value):
    GENERAL_SETTINGS.setValue(key, value)
    GENERAL_SETTINGS.sync()


# Restore by default settings method
def restore_by_default():
    try:
        for key in DEFAULT_SETTINGS.keys():
            if GENERAL_SETTINGS.value(key) is None:
                save_settings(key, DEFAULT_SETTINGS[key])
    except Exception as e:
        print("Error reestableciendo configuracion")
        send_to_log(f"Reestableciendo configuracion {e.args}")


def restore_one_by_default(setting: str):
    try:
        save_settings(setting, DEFAULT_SETTINGS[setting])
    except Exception as e:
        print(f"Error reestableciendo configuracion para {setting}")
        send_to_log(f"Error reestableciendo configuracion para {setting}")


restore_by_default()
