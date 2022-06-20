from PyQt5.QtCore import QSettings
from util.const import APP_ID
from util.logger import SENT_TO_LOG

DEFAULT_SETTINGS = {"last_modification_date":""}
# QSettings object
GENERAL_SETTINGS = QSettings(APP_ID)
# Save settings method
def SAVE_SETTINGS(key, value):
    GENERAL_SETTINGS.setValue(key, value)
    GENERAL_SETTINGS.sync()
# Restore by default settings method
def RESTORE_BY_DEFAULT():
    try:
        for key in DEFAULT_SETTINGS.keys():
            if GENERAL_SETTINGS.value(key) is None:
                SAVE_SETTINGS(key, DEFAULT_SETTINGS[key])
    except Exception as e:
        print("Error reestableciendo configuracion")
        SENT_TO_LOG(f"Reestableciendo configuracion {e.args}")
RESTORE_BY_DEFAULT()
def RESTORE_ONE_BY_DEFAULT(setting:str):
    try:
        SAVE_SETTINGS(setting, DEFAULT_SETTINGS[setting])
    except Exception as e:
        print(f"Error reestableciendo configuracion para {setting}")
        SENT_TO_LOG(f"Error reestableciendo configuracion para {setting}")