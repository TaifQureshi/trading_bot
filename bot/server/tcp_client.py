from twisted.internet import reactor
from twisted.internet.protocol import ReconnectingClientFactory as ClFactory
from typing import Dict, Callable
import logging
from . import Connection


class TcpClient(ClFactory):
    def __init__(self, config, callbacks: Dict[str, Callable],
                 *args, **kwargs):
        super(TcpClient, self).__init__(*args, **kwargs)
        self.port = config.get("host")
        self.host = config.get("port")
        self.callbacks = callbacks
        self.connector = None
        self.logger = logging.getLogger("tcp_client")

    def start(self):
        self.connector = reactor.connectTCP(
            self.host,
            self.port,
            self
        )

    def stop(self):
        self.connector.disconnect()

    def clientConnectionLost(self, connector, unused_reason):
        if self.retries > 0:
            self.logger.info(f"retry attempt : {self.retries}, "
                             f"next retry in {int(round(self.delay))} seconds")
        self.retry(connector)

    def clientConnectionFailed(self, connector, reason):
        if self.retries > 0:
            self.logger.info(f"retry attempt : {self.retries}, "
                             f"next retry in {int(round(self.delay))} seconds")
        self.retry(connector)

    def buildProtocol(self, addr):
        self.resetDelay()
        return Connection(self.callbacks)
