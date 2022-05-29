from . import BasePayload


class CancelOrder(BasePayload):
    def __int__(self,
                client_id: int,
                order_id: int,
                side: str,
                symbol: str,
                price: float,
                qty: float,
                exchange: str = 'mt5',
                *args, **kwargs):
        super(CancelOrder, self).__int__(*args, **kwargs)
        self.client_id = client_id
        self.order_id = order_id
        self.side = side
        self.symbol = symbol
        self.price = price
        self.qty = qty
        self.exchange = exchange
