from . import BasePayload


class ExecReport(BasePayload):
    def __int__(self,
                client_id: int,
                side: str,
                symbol: str,
                price: float,
                qty: float,
                exchange: str = 'mt5',
                order_id: int = None,
                status='',
                error:str = '',
                *args, **kwargs
                ):
        self.client_id = client_id
        self.side = side
        self.symbol = symbol
        self.price = price
        self.qty = qty
        self.order_id = order_id
        self.exchange = exchange
        self.status = status
        self.error = error
        super(ExecReport, self).__int__(*args, **kwargs)
