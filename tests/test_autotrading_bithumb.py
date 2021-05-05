import unittest
import pybithumb

from autotrading.machine.autotrading_bithumb import AutotradingBithumb

class AutotradingBithumbTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.trader = AutotradingBithumb()

    def _test_pybithumb_ticker(self):
        tickers =pybithumb.get_tickers()
        print(tickers)
        print(len(tickers))

    def test_get_balance(self):
        # given

        # when
        balance = self.trader.get_balance()

        # then
        print(balance)
        assert balance
