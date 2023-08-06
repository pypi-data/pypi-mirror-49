""" tools to configure modules used in an uppercut system """
from redis import Redis
import constants
import json

def Register(name,description):
    """ registers register the module's particulars on the in mem repo """
    _redis = Redis(host=constants.EnvVars.MOD_REG_SERVER)
    modInfo = {'name':name, 'description':description}
    _redis.lpush(constants.Keys.MOD_LIST,json.dumps(modInfo))


def GetModules():
    _redis = Redis(host=constants.MOD_REG_SERVER)
    modList = _redis.lrange(constants.Keys.MOD_LIST,0,-1)
    modList = json.loads(modList)
    return modList