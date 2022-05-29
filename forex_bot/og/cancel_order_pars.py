from bot import ExecReport, CancelOrder
from typing import Any


class CancelOrderParser(object):
    @staticmethod
    def parser(order: CancelOrder, response):
        if order.exchange == 'mt5':
            return Mt5CancelOrder.pars(order, response)


class Mt5CancelOrder(object):
    @staticmethod
    def pars(order: CancelOrder, response: Any):
        exec_report = None
        if 'error' in response:
            exec_report = ExecReport(client_id=order.client_id,
                                     side=order.side,
                                     symbol=order.symbol,
                                     price=order.price,
                                     qty=order.qty,
                                     exchange='mt5',
                                     order_id=0,
                                     status='cancel_reject',
                                     error=response['error'])
        else:
            ExecReport(client_id=order.client_id,
                       side=order.side,
                       symbol=order.symbol,
                       price=order.price,
                       qty=order.qty,
                       exchange='mt5',
                       order_id=response['order_id'],
                       status='canceled')

        return exec_report
