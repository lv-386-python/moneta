'''Module, that contain diferent utils (getting configs) '''

import configparser
from www.settings.settings import DATABASES

def get_db_config():
    "function for getting database and pool manager configs"
    conf_dict = {}
    conf = configparser.SafeConfigParser()
    conf.read(DATABASES['default']['OPTIONS']['read_default_file'])
    for i in conf.sections():
    	conf_dict[i] = {}
    	for j in  conf.options(i):
    		param = conf.get(i, j)
    		if param.startswith('eval'):
    			param = eval(param[5:-1])
    		conf_dict[i][j] = param
    return conf_dict
