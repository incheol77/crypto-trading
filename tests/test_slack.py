import unittest
from autotrading.pusher.slack import PushSlack

class TestSlacker(unittest.TestCase):
    def setUp(self):
        self.pusher = PushSlack()

    def test_send_message(self):
        self.pusher.send_message("#코인정보공유", "하이루 하니야아~~")

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()