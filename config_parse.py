import ConfigParser, os
from os.path import expanduser
import platform


def getConfig(section, key):
    config = ConfigParser.ConfigParser()
    home = expanduser("~")
    osstr=platform.system()
    if (osstr == "Windows"):
        config_path=home+'\\.oci\\configuration'
    else:
        config_path=home+'/.oci/configuration'
    config.read(config_path)
    return config.get(section,key)


if __name__ == '__main__':
    user_id=getConfig("User","user_id")
    print user_id


