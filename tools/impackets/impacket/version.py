# SECUREAUTH LABS. Copyright 2019 SecureAuth Corporation. All rights reserved.
#
# This software is provided under under a slightly modified version
# of the Apache Software License. See the accompanying LICENSE file
# for more information.
#
import pkg_resources
from impacket import __path__


try:
    version = pkg_resources.get_distribution('impacket').version
except pkg_resources.DistributionNotFound:
    version = "?"
    print("Cannot determine Impacket version. "
          "If running from source you should at least run \"python setup.py egg_info\"")
BANNER = "Impacket v{} - Copyright 2020 SecureAuth Corporation\n".format(version)

def getInstallationPath():
    return 'Impacket Library Installation Path: {}'.format(__path__[0])
