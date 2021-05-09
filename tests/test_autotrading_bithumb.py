import unittest
import pybithumb

from autotrading.machine.autotrading_bithumb import AutotradingBithumb

class AutotradingBithumbTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.trader = AutotradingBithumb()

    def tearDown(self) -> None:
        del self.trader

    # test for public APIs
    def _test_get_all_tickers(self):
        tickers = self.trader.get_all_tickers()
        assert tickers
        print(tickers)
        print(len(tickers))

    def _test_get_current_price(self):
        ticker = 'XRP'
        current_price = self.trader.get_current_price(ticker)
        assert current_price
        print(ticker, current_price)

    def _test_get_all_prices(self):
        all_prices = self.trader.get_all_prices()
        assert all_prices
        print(all_prices)

    # test for private APIs
    def _test_get_balance(self):
        balance = self.trader.get_balance('XRP')
        assert balance
        print("balance : ", format(balance, 'f'))

    def _test_get_my_money(self):
        my_money = self.trader.get_my_money()
        assert my_money
        print("my_money : ", my_money)

    def _test_buy_order(self):
        buy_price = self.trader.buy_order('XRP')
        assert buy_price
        print("buy_price : ", buy_price)

    def _test_make_buy_price(self):
        tickers = ['ETC', 'BTC']
        buy_prices = []
        for ticker in tickers:
            current_price = self.trader.get_current_price(ticker)
            buy_price = self.trader.make_buy_price(ticker, current_price)
            assert buy_price
            buy_prices.append((current_price, buy_price))
        print("buy_prices : ", buy_prices)

    def _test_get_buy_count(self):
        ticker = 'ETC'
        current_price = self.trader.get_current_price(ticker)
        buy_count = self.trader.get_buy_count(current_price)
        assert buy_count
        print("buy_count : ", buy_count)

    def _test_sell_order(self):
        ticker = 'XRP'
        sell_order = self.trader.sell_order(ticker)
        assert sell_order
        print("sell_order: ", sell_order)

    def _test_make_sell_price(self):
        ticker = 'XRP'
        last_buy_prices = [100, 20000]
        sell_prices = []
        for buy_price in last_buy_prices:
            self.trader.last_buy_price = buy_price
            sell_price = self.trader.make_sell_price(ticker)
            assert sell_price
            sell_prices.append(sell_price)
        print("sell_prices : ", sell_prices)

    def _test_get_sell_count(self):
        ticker = 'XRP'
        sell_count = self.trader.get_sell_count(ticker)
        assert sell_count
        print("sell_count : ", sell_count)

    def test_auto_trade(self):
        buy_price = self.trader.auto_trade('XRP')

