import os
import configparser

default_settings = {
    "GENERAL": {
        "always_ask_to_conform_the_destination_folder": "True",
        "import_cookies_from": "nowhere",  # firefox, opera, ...
    },
    "VIDEO": {
        "download_folder": ".",
        "max_resolution": "720p",  # 480p or 720p or 1080p
    },
    "AUDIO": {
        "download_folder": ".",
        "convert_to_mp3": "True",
        "mp3_bitrate": "96 kbps",  # 96, 128, 192
    },
}
CONF_DIR_NAME = "tubic"
CONF_FILE_NAME = "tubic_settings.ini"


def _get_conf_path():
    if os.path.isfile(CONF_FILE_NAME):
        return CONF_FILE_NAME

    default_config_path = None
    if "APPDATA" in os.environ:
        default_config_path = os.environ["APPDATA"]
    elif "XDG_CONFIG_HOME" in os.environ:
        default_config_path = os.environ["XDG_CONFIG_HOME"]
    else:
        return CONF_FILE_NAME

    config_dir_path = os.path.join(default_config_path, CONF_DIR_NAME)
    if not os.path.isdir(config_dir_path):
        os.mkdir(config_dir_path)

    config_path = os.path.join(config_dir_path, CONF_FILE_NAME)
    return config_path


CONFIG_PATH = _get_conf_path()


def save_settings(config: configparser.ConfigParser):
    with open(CONFIG_PATH, "w") as configfile:
        config.write(configfile)


def _get_config():
    config = configparser.ConfigParser()
    if not os.path.exists(CONFIG_PATH):
        config.read_dict(default_settings)
        save_settings(config)
    config.read(CONFIG_PATH)
    return config


SETTINGS = _get_config()


def get_settings_by_path(path: str, type=str, default=None) -> str | bool | int | None:
    path = path.split(".")
    val = SETTINGS
    for p in path[:-1]:
        val = val[p]
    if type == str:
        return val.get(path[-1], default)
    elif type == bool:
        return val.getboolean(path[-1], default)
    elif type == int:
        return val.getint(path[-1], default)


def set_settings_by_path(path: str, val: str) -> None:
    path = path.split(".")
    cur = SETTINGS
    for p in path[:-1]:
        cur = cur[p]
    cur[path[-1]] = val
