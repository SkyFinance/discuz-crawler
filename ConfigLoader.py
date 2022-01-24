from yaml import load, FullLoader
from Utils.CookieUtil import CookieUtil


class ConfigLoader:
    def __init__(self) -> None:
        with open('config.yml') as f:
            self.data = load(f, Loader=FullLoader)

    def GetSiteCookie(self) -> str:
        return CookieUtil.CookiesToDict(self.data['cookies']['site'])

    def GetFeiMaoCookie(self) -> str:
        return CookieUtil.CookiesToDict(self.data['cookies']['feimao'])

    def GetDriverType(self):
        return self.data['driver']['type']

    def GetDriverPath(self) -> str:
        return self.data['driver']['path']

    def GetEdgePath(self) -> str:
        return self.data['edge']['bin_path']
