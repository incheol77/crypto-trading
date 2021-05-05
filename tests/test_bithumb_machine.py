import time
import unittest
from datetime import datetime

from autotrading.machine.bithumb_machine import BithumbMachine
import inspect

class BithumbMachineTestCase(unittest.TestCase):

    def setUp(self):
        self.bm = BithumbMachine()

    def _test_get_ticker(self):
        print(inspect.stack()[0][3])
        ticker = self.bm.get_ticker("ETC")
        assert ticker
        for key, value in ticker.items():
            print(key, ": ", value)

    def _test_get_current_price(self):
        currency = "ETC"
        current_price = self.bm.get_current_price(currency)
        assert current_price
        print("\n *** ", currency, " ***")
        for key, value in current_price.items():
            print(key, ": ", value)

    def _test_get_current_price_periodic(self):
        currency = "ETC"
        for i in range(5):
            current_price = self.bm.get_current_price(currency)
            assert current_price
            print("\n *** ", currency, " ***")
            for key, value in current_price.items():
                print(key, ": ", value)
            time.sleep(1)

    def _test_get_all_current_prices(self):
        for currency in self.bm.TRADE_CURRENCY_TYPE:
            current_price = self.bm.get_current_price(currency)
            assert current_price
            print("\n *** ", currency, " ***")
            for key, value in current_price.items():
                print("   -- ", key, ": ", value)

    def test_convert_timestamp_to_datetime(self):
        # given
        timestamp_time = 1620209418084
        answer = datetime(2021, 5, 5, 19, 10, 18, 84000)

        # when
        datetime_obj = self.bm.convert_timestamp_to_datetime(timestamp_time)

        # then
        assert datetime_obj
        self.assertEqual(answer, datetime_obj)

    def _test_get_transaction_history(self):
        print(inspect.stack()[0][3])
        tran_hist = self.bm.get_transaction_history("ETC")
        assert tran_hist
        for i in range(10):
            print(tran_hist[i])

    def _test_get_order_request(self):
        print(inspect.stack()[0][3])
        order_req = self.bm.get_order_request("ETC")
        assert order_req
        print(order_req)

    def test_get_wallet_status(self):
        print(inspect.stack()[0][3])
        wallet_status = self.bm.get_wallet_status("ETC")
        assert wallet_status
        print(wallet_status)

    def tearDown(self):
        pass