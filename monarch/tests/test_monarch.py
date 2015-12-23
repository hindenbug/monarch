from unittest import TestCase
from ludibrio import Stub

import io
import monarch
import datetime

class TestDoNotDisturb(TestCase):
    def setUp(self):
        with monarch.configure('localhost', 6379, 0) as config:
            config.namespace = 'dnd_test'
            config.cache_size = 99


    def test_basic_dnd(self):
        monarch.config.rule.add('notification', 'promotion', 60)
        array = []
        with monarch.throttle('notification', 10, 'promotion') as pipe:
            if pipe: array.append(1)
        with monarch.throttle('notification', 10, 'promotion') as pipe:
            if pipe: array.append(2)
        self.assertTrue(array==[1])


    def test_basic_communication(self):
        monarch.config.rule.add('notification', 'deal', 1)
        now = datetime.datetime.now()

        now_2 = now + datetime.timedelta(minutes=2)
        now_4 = now + datetime.timedelta(minutes=4)
        array = []

        with monarch.throttle('notification', 10, 'deal') as pipe:
            if pipe: array.append(1)

        with Stub(proxy=datetime.datetime.now()) as new_now:
            from datetime import datetime as new_datetime
            new_datetime.now() >> now_2

        with monarch.throttle('notification', 10, 'deal') as pipe:
            if pipe: array.append(2)

        with Stub(proxy=datetime.datetime.now()) as new_now:
            from datetime import datetime as new_datetime
            new_datetime.now() >> now_4

        with monarch.throttle('notification', 10, 'deal') as pipe:
            if pipe: array.append(3)

        self.assertTrue(array==[1,2,3])


    def tearDown(self):
        keys1 = monarch.config.rule.list()
        for key in keys1: monarch.config.redis.delete(key)
        keys2 = monarch.config.lock.list()
        for key in keys2: monarch.config.redis.delete(key)

if __name__ == '__main__':
    unittest.main()
