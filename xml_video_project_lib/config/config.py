import configparser
from pathlib import Path

class Config:
    """
    Singleton class to handle configuration parameters.
    """
    _instance = None
    _config = None

    def __new__(cls, config_file='../config.ini'):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._config = configparser.ConfigParser()
            cls._load_config(config_file)
        return cls._instance

    @classmethod
    def _load_config(cls, config_file):
        config_path = Path(__file__).parent.parent / config_file
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file '{config_path}' not found.")

        cls._config.read(config_path)

    def get(self, section, option, fallback=None, type_cast=str):
        """
        Retrieves a configuration value with type casting.

        Args:
            section (str): The section in the config file.
            option (str): The option/key within the section.
            fallback: The value to return if the option is not found.
            type_cast (type): The type to cast the option's value to.

        Returns:
            The configuration value cast to the specified type.
        """
        try:
            if type_cast == bool:
                return self._config.getboolean(section, option, fallback=fallback)
            elif type_cast == int:
                return self._config.getint(section, option, fallback=fallback)
            elif type_cast == float:
                return self._config.getfloat(section, option, fallback=fallback)
            else:
                return self._config.get(section, option, fallback=fallback)
        except (configparser.NoSectionError, configparser.NoOptionError) as e:
            if fallback is not None:
                return fallback
            else:
                raise e
            
    def get_all(self, section, fallback={}):
        try:
            return self._config[section]
        except (configparser.NoSectionError) as e:
            if fallback is not None:
                return fallback
            else:
                raise e

# Instantiate the Config singleton
config = Config()