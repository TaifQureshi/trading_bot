from math import isclose
from . import BasePayload


class TickData(BasePayload):
    def __init__(self,
                 time=None,
                 bid=None,
                 ask=None,
                 last=None,
                 volume=None,
                 time_msc=None,
                 flags=None,
                 volume_real=None,
                 *args, **kwargs):
        super(TickData, self).__init__(*args, **kwargs)
        self.time = time
        self.bid = bid
        self.ask = ask
        self.last = last
        self.volume = volume
        self.time_msc = time_msc
        self.flags = flags
        self.volume_real = volume_real

    def is_equal(self, other):
        match = False
        if self.bid and other.bid and isclose(self.bid, other.bid):
            match = True

        if self.ask and other.bid and isclose(self.ask, other.ask):
            match = True

        return match

    def send(self):
        return {"time": int(self.time), "bid": float(self.bid), "ask": float(self.ask), "volume": float(self.volume),
                "volume_real": float(self.volume_real), "flags": int(self.flags)}

    def __str__(self):
        return str(self.send())
