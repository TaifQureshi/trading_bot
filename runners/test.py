from twisted.internet import reactor
import MetaTrader5 as mt5


def test(inputs):
    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        quit()
