import configparser


class ConfigParser(configparser.ConfigParser):
    def __init__(self, *args, **kwargs):
        """
        Initiliaze a parser to load a config file

        :param args:
        :param kwargs:
        """
        super(ConfigParser, self).__init__(*args, **kwargs)

    def eval(self, value):
        """
        Eval boolean values

        :param value:
        :return object:
        """
        if value == "false":
            value = "False"
        elif value == "true":
            value = "True"
        return eval(value)

    def convert_types(self, key):
        """
        Eval keys in dict

        :param key:
        :return dictionary:
        """
        config = dict(self[key])
        for key in list(config.keys()):
            config[key] = self.eval(config[key])
        return config
