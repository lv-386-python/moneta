'''Module, that contain diferent utils (getting configs).'''

import configparser

from settings.settings import DATABASES  # pylint:disable = no-name-in-module, import-error


def get_config():
    "Function for getting configs."
    conf_dict = {}
    conf = configparser.SafeConfigParser()
    conf.read(DATABASES['default']['OPTIONS']['read_default_file'])
    for i in conf.sections():
        conf_dict[i] = {}
        for j in conf.options(i):
            param = conf.get(i, j)
            if param.startswith('eval'):
                param = eval(param[5:-1])  # pylint:disable = eval-used
            conf_dict[i][j] = param
    return conf_dict
