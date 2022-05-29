from forex_bot.og.og_server import OGServer
from twisted.internet import reactor
from bot import Config

config = Config()


def og(input_args):
    config.initialize(['accounts.yml', 'ports.yml'])
    host = config.get('og')['host']
    port = config.get('og')['port']
    order_gate = OGServer(host,port, config)
    order_gate.start()
    reactor.addSystemEventTrigger('before', 'shutdown', order_gate.stop)
    reactor.run()
