from abc import abstractmethod, ABCMeta
import logging


class Exchange(metaclass=ABCMeta):
    def __init__(self, name, config):
        self.logger = logging.getLogger(name)
        self.name = name
        self.config = config.get(name)

    def start(self):
        pass

    @staticmethod
    def stop():
        pass

    @abstractmethod
    def close_order(self, order_id: int, side: str, symbol: str, price: float, qty: float, client_id: int = 12345):
        pass

    @abstractmethod
    def market_buy(self, symbol: str, qty: float = 0.1, sl=0.0, tp=0.0, client_id=1234):
        pass

    @abstractmethod
    def market_sell(self, symbol: str,qty: float = 0.1, sl=0.0, tp=0.0, client_id=1234):
        pass

    @abstractmethod
    def limit_buy(self, symbol: str, price: float, qty: float = 0.1, sl=0.0, tp=0.0, client_id=1234):
        pass

    @abstractmethod
    def limit_sell(self, symbol: str, price: float, qty: float = 0.1, sl=0.0, tp=0.0, client_id=1234):
        pass

    @abstractmethod
    def send_order(self, order):
        pass
