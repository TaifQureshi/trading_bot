from bot import TcpServer, Header, NewOrder, CancelOrder, MT5Connection, ExecReport
import logging
from .new_order_pars import NewOrderPars
from .cancel_order_pars import CancelOrderParser

logger = logging.getLogger('og')


class OGServer(object):
    def __init__(self, host: str, port: int,config):
        self.name = 'og'
        self.config = config
        self.server = TcpServer(host, port,
                                callbacks={"on_connect": self.on_connect,
                                           "on_data": self.on_data,
                                           "on_disconnect": self.on_disconnect})
        self.placer = MT5Connection(self.config)

    def start(self):
        logger.info("starting the og server")
        self.server.start()
        self.placer.start()

    def stop(self):
        logger.info('stopping the server')
        self.server.stop()
        self.placer.stop()

    @staticmethod
    def on_connect(connection):
        logger.info(f"Connection to raspberrypi")

    def on_data(self, connection, data):
        header = Header.de_json(data)
        data = header.payload
        exec_report = None
        if header.payload_type == 'NewOrder':
            exec_report = self.on_new_order(data)
            connection.send_data(Header('ExecReport', exec_report))
        elif header.payload_type == 'CancelOrder':
            exec_report = self.on_cancel_order(data)

        if exec_report:
            connection.send_data(Header('ExecReport', exec_report))

    def on_new_order(self, order: NewOrder):
        response = None
        if order.side == 'buy':
            if order.price == 0:
                response = self.placer.market_buy(order.symbol, order.qty, order.sl, order.tp, order.client_id)
            else:
                response = self.placer.limit_buy(order.symbol, order.price,order.qty, order.sl, order.tp, order.client_id)
        elif order.side == 'sell':
            if order.price == 0:
                response = self.placer.market_sell(order.symbol, order.qty, order.sl, order.tp, order.client_id)
            else:
                response = self.placer.limit_sell(order.symbol, order.price, order.qty, order.sl, order.tp, order.client_id)

        exec_report = NewOrderPars.parser(order, response)
        return exec_report

    def on_cancel_order(self, order: CancelOrder):
        response = self.placer.close_order(order.order_id, order.side, order.side, order.price, order.qty, order.client_id)

        exec_report = CancelOrderParser.parser(order, response)

        return exec_report

    @staticmethod
    def on_disconnect(connection, reason):
        logger.info("Client disconnected")
        logger.info(reason)
