from django.conf import settings


class DRFSettings(object):

    def __init__(self):
        self.drf_settings = {
            "HIDE_DOCS": self.get_setting("HIDE_DOCS") or False,
            "APP_NAME": self.get_setting("APP_NAME") or settings.ROOT_URLCONF.split(".")[0]
        }

    def get_setting(self, name):
        try:
            return settings.DRF_DOCS[name]
        except:
            return None

    @property
    def settings(self):
        return self.drf_settings
