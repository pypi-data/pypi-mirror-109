# encoding: utf-8
# set key、token、pkg_name、platform
import config


class Credentials(object):

    def set_key(self, ak):
        config.ACCESS_KEY = ak

    def set_token(self, token):
        config.ACCESS_TOKEN = token

    def set_pkgname(self, pkg):
        config.PKG_NAME = pkg

    def set_platform(self, platform):
        config.PLATFORM = platform
