import unittest
import datetime
import redis
from monarch import Config, Lock

class LockTest(unittest.TestCase):

    def setUp(self):
        self.config = Config(host='localhost', port='6379', db=0)
        self.config.namespace = "dnd_test"
        self.config.cache_size = 99
        self.lock = Lock(self.config, pattern="%s:l:c:%s:u:%s:t:%s")

    def tearDown(self):
        keys = self.lock.list()
        for key in keys:
            self.config.redis.delete(key)

    def test_lock_add(self):
        now = datetime.datetime.now()
        self.lock.add("notification", 12345, "promo", now)
        key = self.lock.key("notification", 12345, "promo")

        self.assertTrue(self.config.redis.exists(key))

    def test_invalid_lock_add(self):
        with self.assertRaises(TypeError):
            self.lock.add(None, 12345, "promo")

    def test_construct_lock_key(self):
        key = self.lock.key("channel", 12345, "category")
        self.assertEqual(key, 'dnd_test:l:c:channel:u:12345:t:category')

    def test_get_lock(self):
        now = datetime.datetime.now()
        self.lock.add("notification", 12345, "promo", now)

        self.assertNotEqual(self.lock.get("notification", 12345, "promo"), None)

    def test_get_non_existent_lock(self):
        self.assertEqual(self.lock.get("unknown", 00000, "promo"), None)

    def test_get_list_of_locks(self):
        now = datetime.datetime.now()
        self.lock.add("notification", 12345, "promo", now)
        self.lock.add("notification", 12345, "promo", now)
        self.lock.add("email", 12345, "promo", now)
        self.lock.add("sms", 22222, "promo", now)

        self.assertEqual(len(self.lock.list()), 3)

    def test_remove_rules(self):
        now = datetime.datetime.now()
        self.lock.add("notification", 12345, "promo", now)
        self.lock.add("notification", 12345, "promo", now)
        self.lock.add("email", 12345, "promo", now)
        self.lock.add("sms", 22222, "promo", now)
        self.lock.remove("sms", 22222, "promo")

        self.assertEqual(len(self.lock.list()), 2)

if __name__ == '__main__':
    unittest.main()
