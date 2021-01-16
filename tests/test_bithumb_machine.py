import unittest
from autotrading.machine.bithumb_machine import BithumbMachine
import inspect

class BithumbMachineTestCase(unittest.TestCase):

    def setUp(self):
        self.bithumb_machine = BithumbMachine()

    def test_get_ticker(self):
        print(inspect.stack()[0][3])
        ticker = self.bithumb_machine.get_ticker("ETH")
        assert ticker
        for key, value in ticker.items():
            print(key, ": ", value)

    def test_get_transaction_history(self):
        print(inspect.stack()[0][3])
        tran_hist = self.bithumb_machine.get_transaction_history("ETH")
        assert tran_hist
        for i in range(10):
            print(tran_hist[i])

    def test_get_order_request(self):
        print(inspect.stack()[0][3])
        order_req = self.bithumb_machine.get_order_request("ETH")
        assert order_req
        print(order_req)

    def tearDown(self):
        pass