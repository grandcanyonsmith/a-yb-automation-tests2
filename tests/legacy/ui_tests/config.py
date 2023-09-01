import configparser


class Config:
    _config = configparser.ConfigParser()

    @classmethod
    def load(cls, filename="config.ini"):
        cls._config.read(filename)

    @classmethod
    def get_section(cls, section):
        try:
            return dict(cls._config.items(section))
        except configparser.NoSectionError:
            return None


# Load the config file when the module is imported
Config.load()
