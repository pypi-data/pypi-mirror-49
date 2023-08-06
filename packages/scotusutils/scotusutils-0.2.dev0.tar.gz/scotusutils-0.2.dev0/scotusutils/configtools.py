import os
import warnings
import configparser

from scotusutils import _CONFIG_DIR as CONFIG_DIR


SQLITE_CONFIG = "sqlite_db_config.ini"


def _get_sqlite_config_path():
    """Get default SQLite configuration file path"""
    return os.path.join(CONFIG_DIR, SQLITE_CONFIG)


def _load_default_sqlite_config():
    """Load the SQLite configuration file"""
    path = _get_sqlite_config_path()
    if os.path.exists(path):
        config = configparser.ConfigParser()
        config.read(path)
        return config
    else:
        err_msg = "SQLite config file '{}' does not exist".format(path)
        raise FileNotFoundError(err_msg)


def _save_default_sqlite_config(config):
    """Save the config object to the default SQLite config file path
    
    Parameters
    ----------
    config : configparser.ConfigParser
        Active config parser to write out to default file

    """
    with open(_get_sqlite_config_path(), "w") as configfile:
        config.write(configfile)


def _add_new_db(path, name, config, force=False):
    """
    Add a new SQLite3 DB path to the configuration file

    Parameters
    ----------
    path : str
        Path to the new SQLite3 DB
    name : str
        Name of the new DB. Used for accessing in the future.
    config : configparser.ConfigParser
        Current SQLite config

    Returns
    -------
    config : configparser.ConfigParser
        Updated config with new DB path added

    Raises
    ------
    ValueError
        If the name for the new DB is already used, an error is raised
        and the DB is not added to the config

    """
    if "DBPATHS" not in config.keys():
        config["DBPATHS"] = {}

    if force is False and name in config["DBPATHS"].keys():
        err_msg = "SCOTUS DB with name '{}' exists".format(name)
        raise ValueError(err_msg)

    config["DBPATHS"][name] = path


class ConfigHandle(object):
    """
    Interface to the config file.
    """

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(ConfigHandle, cls).__new__(cls)
        else:
            cls.instance.write_and_close()
        return cls.instance

    def __init__(self, config_path=_get_sqlite_config_path()):
        self._config_path = config_path
        self._config = _load_default_sqlite_config()

    def __getitem__(self, key):
        try:
            return self._config["DBPATHS"][key]
        except KeyError as kerr:
            err_msg = f"Specified instance '{key}' does not exist"
            raise ValueError(err_msg) from kerr

    def __setitem__(self, key, value):
        self._add_db(key, value)

    def _add_db(self, name, path):
        """
        Add a new DB to the config file.
        """
        try:
            _add_new_db(path, name, self._config)
        except ValueError:
            warnings.warn(
                f"Attempted to overwrite existing DB name '{name}'", UserWarning
            )

    def write_and_close(self):
        """
        Write current state of config to default path & close to addl edits.
        """
        _save_default_sqlite_config(self._config)
        self._config = None
