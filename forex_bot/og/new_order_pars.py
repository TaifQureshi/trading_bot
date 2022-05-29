from bot import ExecReport, NewOrder
from typing import Any


class NewOrderPars(object):
    @staticmethod
    def parser(order: NewOrder, response):
        if order.exchange == 'mt5':
            return Mt5NewOrder.pars(order, response)


class Mt5NewOrder(object):
    @staticmethod
    def pars(order: NewOrder, response: Any) -> ExecReport:
        exec = None
        if 'error' in response:
            exec = ExecReport(client_id=order.client_id,
                              side=order.side,
                              symbol=order.symbol,
                              price=order.price,
                              qty=order.qty,
                              exchange='mt5',
                              order_id=0,
                              error=response['error'],
                              status='new_reject')
        else:
            exec = ExecReport(client_id=order.client_id,
                              side=order.side,
                              symbol=order.symbol,
                              price=order.price,
                              qty=order.qty,
                              exchange='mt5',
                              order_id=response['order_id'],
                              status='new')

        return exec
