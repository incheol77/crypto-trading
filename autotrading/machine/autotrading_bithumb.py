import configparser
import math
import time
from typing import List

import pybithumb


class AutotradingBithumb():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('conf/config.ini')
        self.CLIENT_ID = config['BITHUMB']['connect_key']
        self.CLIENT_SECRET = config['BITHUMB']['secret_key']
        self.USER_NAME = config['BITHUMB']['username']
        self.bithumb = pybithumb.Bithumb(self.CLIENT_ID, self.CLIENT_SECRET)
        self.BUY_PRICE_RATE = 0.000001
        self.SELL_PRICE_RATE = 0.002
        self.last_buy_price = 0

    # public APIs
    def get_all_tickers(self):
        tickers = pybithumb.get_tickers()
        return tickers

    def get_current_price(self, ticker):
        current_price = pybithumb.get_current_price(ticker)
        return current_price

    def get_all_prices(self) -> List:
        tickers = self.get_all_tickers()
        all_prices = []
        for ticker in tickers:
            price = self.get_current_price(ticker)
            all_prices.append((ticker, price))
        return all_prices

    # private APIs
    def get_balance(self, ticker):
        balance = self.bithumb.get_balance(ticker)[0]
        return balance

    def get_my_money(self):
        my_money = self.bithumb.get_balance('BTC')[2]
        return int(my_money)

    def buy_order(self, ticker):
        current_price = self.get_current_price(ticker)
        buy_price = self.make_buy_price(ticker, current_price)
        buy_count = self.make_buy_count(buy_price)
        print("current_price : ", current_price)
        print("buy_price : ", buy_price)
        print("buy_count : ", buy_count)
        buy_order = self.bithumb.buy_limit_order(ticker, buy_price, buy_count)
        print("buy_order : ", buy_order)
        if isinstance(buy_order, tuple):
            self.last_buy_price = buy_price
            print("Succeed to set last_buy_price : ", self.last_buy_price)
        else:
            self.last_buy_price = 0
            print("Fail to buy -", ticker)
        return buy_count

    def make_buy_price(self, ticker, current_price):
        buy_price = self.calculate_buy_price(current_price)
        adjusted_buy_price = self.adjust_price_digit(ticker, buy_price)
        return int(adjusted_buy_price)

    def make_buy_count(self, buy_price):
        my_money = self.get_my_money()
        buy_count = my_money / buy_price
        total_cost = self.calculate_total_cost(buy_price, buy_count)
        print("*** my_money : ", float(my_money))
        print("*** total_cost : ", total_cost)
        while total_cost > my_money:
            print("Over balance: total_cost, my_money : ", total_cost, my_money)
            buy_count = math.ceil(buy_count - buy_count * 0.02)
            total_cost = buy_price * buy_count
            print("resize : total_cost, my_money : ", total_cost, my_money)
        return round(buy_count, 0)

    def calculate_buy_price(self, current_price):
        # buy_price = current_price - math.ceil(current_price * self.BUY_PRICE_RATE)
        buy_price = current_price - 1
        return buy_price

    def calculate_total_cost(self, buy_price, buy_count):
        fee = self.calculate_bithumb_fee(buy_price * buy_count)
        total_cost = math.ceil(buy_price * buy_count + fee)
        print("~~~ buy_price, buy_count, fee, total_cost : ",
              buy_price, buy_count, fee, total_cost)
        return round(total_cost, 0)

    def calculate_bithumb_fee(self, transaction_cost):
        return math.ceil(transaction_cost * 0.0005)

    def adjust_price_digit(self, ticker, price):
        # for coin using 100 KRW transaction unit
        adjusted_buy_price = price
        if self.is_two_zero_ticker(ticker):
            adjusted_buy_price = price - math.ceil(price % 100)
        elif self.is_one_zero_ticker(ticker):
            adjusted_buy_price = price - math.ceil(price % 10)
        return adjusted_buy_price

    def is_one_zero_ticker(self, ticker):
        return (
            (ticker == 'EOS')
            or (ticker == 'QTUM')
            or (ticker == 'LINK')
        )

    def is_two_zero_ticker(self, ticker):
        return (
                (ticker == 'ETC')
        )

    def count_digits(self, price):
        count = 0
        while price > 0:
            price = price // 10
            count += 1
        return count

    def sell_order(self, ticker):
        # error codes
        # sell_order:  {'status': '5600', 'message': '주문량이 사용가능 XRP을 초과하였습니다.'}
        # sell_order:  {'status': '5600', 'message': '입력값을 확인해주세요.'}
        sell_price = int(self.make_sell_price(ticker))
        print("sell_price : ", sell_price)
        sell_count = int(self.get_sell_count(ticker))
        print("sell_count : ", sell_count)
        sell_order = self.bithumb.sell_limit_order(ticker, sell_price, sell_count)
        return sell_count

    def make_sell_price(self, ticker):
        current_price = self.get_current_price(ticker)
        print("current_price : ", current_price)
        if current_price > self.last_buy_price:
            sell_price = current_price
        else:
            profit = self.last_buy_price * self.SELL_PRICE_RATE
            sell_price = self.last_buy_price + profit
        return sell_price

    def get_sell_count(self, ticker):
        sell_count = self.get_balance(ticker)
        return math.floor(sell_count)

    def auto_trade(self, ticker):
        trade_count = 1
        for i in range (trade_count):
            before_money = self.get_my_money()
            print("Before money : ", before_money)
            before_buy_balance = self.get_balance(ticker)
            buy_count = self.buy_order(ticker)
            after_buy_balance = before_buy_balance + buy_count
            while self.get_balance(ticker) < after_buy_balance:
                time.sleep(1)
            sell_count = self.sell_order(ticker)
            before_sell_balance = self.get_balance(ticker)
            after_sell_balance = before_sell_balance + sell_count
            while self.get_balance(ticker) > after_sell_balance:
                time.sleep(1)

            after_money = self.get_my_money()
            print("After money : ", after_money)





