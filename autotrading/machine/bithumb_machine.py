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
        print("client id : ", self.CLIENT_ID)
        print("client secret : ", self.CLIENT_SECRET)
        print("user name : ", self.USER_NAME)

    def get_ticker(self, currency_type=None, payment_currency="KRW"):
        """
        method for getting info of ticker
        using API:
            GET https://api.bithumb.com/public/ticker/{order_currency}_{payment_currency}
                - {order_currency} = 주문 통화(코인), ALL(전체), 기본값 : BTC
                - {payment_currency} = 결제 통화(마켓), 입력값 : KRW 혹은 BTC
        :param currency_type: be defined at TRADE_CURRENCY_TYPE
        :return: ticker info (using dict)
        - status	결과 상태 코드 (정상: 0000, 그 외 에러 코드 참조)	String
        - opening_price	시가 00시 기준	Number (String)
        - closing_price	종가 00시 기준	Number (String)
        - min_price	저가 00시 기준	Number (String)
        - max_price	고가 00시 기준	Number (String)
        - units_traded	거래량 00시 기준	Number (String)
        - acc_trade_value	거래금액 00시 기준	Number (String)
        - prev_closing_price	전일종가	Number (String)
        - units_traded_24H	최근 24시간 거래량	Number (String)
        - acc_trade_value_24H	최근 24시간 거래금액	Number (String)
        - fluctate_24H	최근 24시간 변동가	Number (String)
        - fluctate_rate_24H	최근 24시간 변동률	Number (String)
        - date	타임 스탬프	Integer(String)
            : e.g of results
            'opening_price': '1316000',
            'closing_price': '1311000',
            'min_price': '1202000',
            'max_price': '1333000',
            'units_traded': '139114.51770526',
            'acc_trade_value': '178629817597.9549',
            'prev_closing_price': '1316000',
            'units_traded_24H': '199045.86455813',
            'acc_trade_value_24H': '258306418284.3253',
            'fluctate_24H': '-5000',
            'fluctate_rate_24H': '-0.38',
            'timestamp': '1610781322490'
        """
        if currency_type is None:
            raise Exception('Need to currency type')
        if currency_type not in self.TRADE_CURRENCY_TYPE:
            raise Exception('Not support currency type')
        time.sleep(1)

        ticker_api_path = "/public/ticker/{currency}_{payment_currency}".format(currency=currency_type, payment_currency=payment_currency)
        # e.g : https://apidocs.bithumb.com/docs/ticker
        url_path = self.BASE_API_URL + ticker_api_path
        res = requests.get(url_path)
        response_json = res.json()
        result={}
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

    def get_transaction_history(self, currency_type=None, payment_currency="KRW"):
        """
        method for getting info of transaction history
        using API:
            GET https://api.bithumb.com/public/transaction_history/{order_currency}_{payment_currency}
                - {order_currency} = 주문 통화(코인), 기본값 : BTC
                - {payment_currency} = 결제 통화(마켓), 입력값 : KRW 혹은 BTC
        :param currency_type: be defined at TRADE_CURRENCY_TYPE
        :return: recently 100 trasaction history (using list of dict)
            - status	결과 상태 코드 (정상: 0000, 그 외 에러 코드 참조)	String
            - transaction_date	거래 체결 시간 타임 스탬프 (YYYY-MM-DD HH:MM:SS)	Integer (String)
            - type	거래 유형
            - bid : 매수 ask : 매도	String
            - units_traded	Currency 거래량	Number (String)
            - price	Currency 거래가	Number (String)
            - total	총 거래 금액	Number (String)
            : e.g of results
            {'transaction_date': '2021-01-16 16:12:12', 'type': 'bid', 'units_traded': '0.8764', 'price': '1313000', 'total': '1150713'}
        """
        if currency_type is None:
            raise Exception("Need to currency_type")
        if currency_type not in self.TRADE_CURRENCY_TYPE:
            raise Exception("Not support currency type")
        time.sleep(1)
        params = {'offset':0, 'count':100}
        orders_api_path = "/public/transaction_history/{currency}_{payment_currency}".format(currency=currency_type, payment_currency=payment_currency)
        # e.g : https://api.bithumb.com/public/transaction_history/ETH_KRW
        url_path = self.BASE_API_URL + orders_api_path
        print(url_path)
        res = requests.get(url_path, params=params)
        response_json = res.json()
        results = []
        for r in response_json['data']:
            results.append(r)

        return results
