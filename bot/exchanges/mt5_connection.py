import MetaTrader5 as mt5
import pytz
from datetime import datetime, timedelta
import pandas as pd
from . import Exchange


class MT5Connection(Exchange):
    def __init__(self, config):
        super(MT5Connection, self).__init__('mt5', config)
        self.period = {"1_min": mt5.TIMEFRAME_M1,
                       "2_min": mt5.TIMEFRAME_M2,
                       "3_min": mt5.TIMEFRAME_M3,
                       "4_min": mt5.TIMEFRAME_M4,
                       "5_min": mt5.TIMEFRAME_M5,
                       "6_min": mt5.TIMEFRAME_M6,
                       "10_min": mt5.TIMEFRAME_M10,
                       "12_min": mt5.TIMEFRAME_M12,
                       "15_min": mt5.TIMEFRAME_M15,
                       "30_min": mt5.TIMEFRAME_M30}

        self.order_type = {"buy": mt5.ORDER_TYPE_BUY,
                           "sell": mt5.ORDER_TYPE_SELL,
                           1: "sell",
                           0: "buy"}

        self.time_zone = pytz.timezone("Etc/UTC")

    def start(self):
        if not mt5.initialize(login=self.config.get('login'),
                              server=self.config.get('server'),
                              password=self.config.get('password')):
            self.logger.info(f"initialize() failed, error code = {mt5.last_error()}")

    @staticmethod
    def stop():
        mt5.shutdown()

    @staticmethod
    def account_balance():
        # noinspection PyProtectedMember
        account = mt5.account_info()._asdict()
        return account.get("balance")

    def get_candles(self, symbol: str, period: str, number: int):
        utc_from = datetime.now()
        rates = mt5.copy_rates_from(symbol, self.period.get(period), utc_from, number)
        return pd.DataFrame(rates)

    def market_buy(self, symbol: str, qty: float = 0.1, sl=0.0, tp=0.0, client_id=1234):
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": qty,
            "type": self.order_type.get('buy'),
            "price": mt5.symbol_info_tick(symbol).ask,
            "sl": round(sl, 3),
            "tp": round(tp, 3),
            "magic": client_id,
            "comment": "python script",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        return self.send_order(request)

    def market_sell(self, symbol: str, qty: float = 0.1, sl=0.0, tp=0.0, client_id=1234):
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": qty,
            "type": self.order_type.get('sell'),
            "price": mt5.symbol_info_tick(symbol).bid,
            "sl": round(sl, 3),
            "tp": round(tp, 3),
            "magic": client_id,
            "comment": "python script",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        return self.send_order(request)

    def limit_buy(self, symbol: str, price: float, qty: float = 0.1, sl=0.0, tp=0.0, client_id=1234):
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": qty,
            "type": self.order_type.get('buy'),
            "price": price,
            "sl": round(sl, 3),
            "tp": round(tp, 3),
            "magic": client_id,
            "comment": "python script",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        return self.send_order(request)

    def limit_sell(self, symbol: str, price: float, qty: float = 0.1, sl=0.0, tp=0.0, client_id=1234):
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": qty,
            "type": self.order_type.get('sell'),
            "price": price,
            "sl": round(sl, 3),
            "tp": round(tp, 3),
            "magic": client_id,
            "comment": "python script",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        return self.send_order(request)

    def send_order(self, request):

        # perform the check and display the result 'as is'
        result = mt5.order_send(request)

        if result.retcode != mt5.TRADE_RETCODE_DONE:
            return {"retcode": result.retcode, "error": result.comment}
        return {"retcode": result.retcode, "order_id": result.order}

    def close_order(self, order_id: int, side: str, symbol: str, price: float, qty: float, client_id: int = 12345):
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": qty,
            "type": self.order_type.get(side),
            "position": order_id,
            "price": price,
            "magic": client_id,
            "comment": "python script close",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            return {"retcode": result.retcode, "error": result.comment}
        return {"retcode": result.retcode, "order_id": result.order}

    # def close_order_by_order_id(self, order_id: int):
    #     order = mt5.orders_get(ticket=order_id)
    #     return self.close_order(order.ticket, self.order_type.get(order.type), order.symbol,
    #                             order.price_current, order.volume)
    #
    # def close_all_buy(self):
    #     results = []
    #     for i in mt5.positions_get():
    #         if i.type == 0:
    #             price = mt5.symbol_info_tick(i.symbol).ask
    #             results.append(self.close_order(i.ticket, self.order_type.get(i.type), i.symbol, price, i.volume))
    #
    #     return results
    #
    # def close_all_sell(self):
    #     results = []
    #     for i in mt5.positions_get():
    #         if i.type == 1:
    #             price = mt5.symbol_info_tick(i.symbol).bid
    #             results.append(self.close_order(i.ticket, self.order_type.get(i.type), i.symbol, price, i.volume))
    #
    #     return results
    #
    # def close_all_by_magic(self, magic: int):
    #     results = []
    #     for order in mt5.positions_get():
    #         if magic == order.magic:
    #             price = mt5.symbol_info_tick(order.symbol).bid
    #             results.append(self.close_order(order.ticket, self.order_type.get(order.type),
    #                                             order.symbol, price, order.volume))
    #     return results

    @staticmethod
    def current_price(symbol):
        utc_from = datetime.now() - timedelta(seconds=10)
        data = mt5.copy_ticks_from(symbol, utc_from, 1, mt5.COPY_TICKS_ALL)
        if len(data) > 0:
            return data

    @staticmethod
    def len_open_order():
        return mt5.positions_total()

    @staticmethod
    def open_order(symbol):
        order = mt5.positions_get(symbol=symbol)
        return order

    @staticmethod
    def close_trades(id):
        order = mt5.history_orders_get(position=id)
        return order
