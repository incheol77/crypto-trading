import configparser
import pybithumb

class AutotradingBithumb():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('conf/config.ini')
        self.CLIENT_ID = config['BITHUMB']['connect_key']
        self.CLIENT_SECRET = config['BITHUMB']['secret_key']
        self.USER_NAME = config['BITHUMB']['username']
        print("client id : ", self.CLIENT_ID)
        print("client secret : ", self.CLIENT_SECRET)
        print("user name : ", self.USER_NAME)

    def get_balance(self):
        bithumb = pybithumb.Bithumb(self.CLIENT_ID, self.CLIENT_SECRET)
        balance = bithumb.get_balance("BTC")
        return balance