from . import BasePayload


class NewOrder(BasePayload):
    def __int__(self,
                client_id: int,
                side: str,
                symbol: str,
                price: float,
                qty: float,
                sl: float = 0,
                tp: float = 0,
                exchange: str = 'mt5',
                *args, **kwargs):
        super(NewOrder, self).__int__(*args, **kwargs)
        self.client_id = client_id
        self.side = side
        self.symbol = symbol
        self.price = price
        self.qty = qty
        self.sl = sl
        self.tp = tp
        self.exchange = exchange
