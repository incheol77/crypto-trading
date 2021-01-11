import requests
import time
import math
from autotrading.machine.base_machine import Machine
import configparser
import json
import base64
import hashlib
import hmac
import urllib

class BithumbMachine(Machine):
    BASE_API_URL = "https://api.bithumb.com"
    TRADE_CURRENCY_TYPE = ["BTC", "ETH", "DASH", "LTC", "ETC", "XRP", "BCH", "XMR", "ZEC", "QTUM", "BTG", "EOS", "XLM"]

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('conf/config.ini')
        self.CLIENT_ID = config['BITHUMB']['connect_key']
        self.CLIENT_SECRET = config['BITHUMB']['secret_key']
        self.USER_NAME = config['BITHUMB']['username']

        print(self.CLIENT_ID)
        print(self.CLIENT_SECRET)
        print(self.USER_NAME)

    def get_ticker(self, currency_type=None):
        if currency_type is None:
            raise Exception('Need to currency type')
        if currency_type not in self.TRADE_CURRENCY_TYPE:
            raise Exception('Not support currency type')
        time.sleep(1)

        ticker_api_path = "/public/ticker/{currency}".format(currency=currency_type)
        url_path = self.BASE_API_URL + ticker_api_path
        res = requests.get(url_path)
        response_json = res.json()
        result={}
        # https://apidocs.bithumb.com/docs/ticker
        result["opening_price"] = response_json['data']["opening_price"]    # 시가 00시 기준
        result["closing_price"] = response_json['data']["closing_price"]    # 종가 00시 기준
        result["min_price"] = response_json['data']["min_price"]    # 저가 00시 기준
        result["max_price"] = response_json['data']["max_price"]    # 고가 00시 기준
        result["units_traded"] = response_json['data']["units_traded"]  # 거래량 00시 기준
        result["acc_trade_value"] = response_json['data']["acc_trade_value"]    # 거래금액 00시 기준
        result["prev_closing_price"] = response_json['data']["prev_closing_price"]  # 전일 종가
        result["units_traded_24H"] = response_json['data']["units_traded_24H"]  # 최근 24시간 거래량
        result["acc_trade_value_24H"] = response_json['data']["acc_trade_value_24H"]    # 최근 24시간 거래금액
        result["fluctate_24H"] = response_json['data']["fluctate_24H"]  # 최근 24시간 변동률
        result["fluctate_rate_24H"] = response_json['data']["fluctate_rate_24H"]    # 최근 24시간 변동률
        result["timestamp"] = str(response_json['data']["date"])    # 타임 스탬프
        return result
