from terrascript import Terrascript


class Terraobject:

    def __init__(self):
        self.priv_ts = Terrascript()
        self.priv_shared = {}

    @property
    def terrascript(self):
        return self.priv_ts

    @terrascript.setter
    def terrascript(self, value):
        self.priv_ts = value

    @property
    def shared(self):
        return self.priv_shared

    @shared.setter
    def shared(self, value):
        self.priv_shared = value