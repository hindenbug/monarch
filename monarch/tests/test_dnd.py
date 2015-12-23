from unittest import TestCase
from ludibrio import Stub

import io
import dnd
import datetime

class TestDoNotDisturb(TestCase):
    def setUp(self):
        with dnd.configure('localhost', 6379, 0) as config:
            config.namespace = 'dnd_test'
            config.cache_size = 99


    def test_basic_dnd(self):
        dnd.config.rule.add('notification', 'promotion', 60)
        array = []
        with dnd.throttle('notification', 10, 'promotion') as pipe:
            if pipe: array.append(1)
        with dnd.throttle('notification', 10, 'promotion') as pipe:
            if pipe: array.append(2)
        self.assertTrue(array==[1])


    def test_basic_communication(self):
        dnd.config.rule.add('notification', 'deal', 1)
        now = datetime.datetime.now()

        now_2 = now + datetime.timedelta(minutes=2)
        now_4 = now + datetime.timedelta(minutes=4)
        array = []

        with dnd.throttle('notification', 10, 'deal') as pipe:
            if pipe: array.append(1)

        with Stub(proxy=datetime.datetime.now()) as new_now:
            from datetime import datetime as new_datetime
            new_datetime.now() >> now_2

        with dnd.throttle('notification', 10, 'deal') as pipe:
            if pipe: array.append(2)

        with Stub(proxy=datetime.datetime.now()) as new_now:
            from datetime import datetime as new_datetime
            new_datetime.now() >> now_4

        with dnd.throttle('notification', 10, 'deal') as pipe:
            if pipe: array.append(3)

        self.assertTrue(array==[1,2,3])


    def tearDown(self):
        keys1 = dnd.config.rule.list()
        for key in keys1: dnd.config.redis.delete(key)
        keys2 = dnd.config.lock.list()
        for key in keys2: dnd.config.redis.delete(key)
