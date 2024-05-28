import unittest
from unittest.mock import patch
import main
import mongomock

class TestInsertCounterData(unittest.TestCase):
    def setUp(self):
        # Імітуємо колекцію MongoDB
        self.db = mongomock.MongoClient().db
        self.db.Prices.insert_one({
            "day_price": 4,
            "night_price": 2,
            "addition_day": 100,
            "addition_night": 50
        })

    def test_new_counter(self):
        # Тест додавання нового лічильника
        with patch.object(main, 'db', new=self.db):
            main.insert_counter_data(123, '2022-01-01', 15, 25)
            
            latest_price_doc = self.db.Prices.find_one()
            
            expected_total = latest_price_doc['addition_day'] + latest_price_doc['addition_night']
            
            expected_price = float(latest_price_doc['day_price'] * latest_price_doc['addition_day'] + latest_price_doc['night_price'] * latest_price_doc['addition_night'])
            
            counter_doc = self.db.Counter.find_one({'number': 123, 'date': '2022-01-01'})
            self.assertEqual({
                    'number': counter_doc['number'],
                    'day': counter_doc['day'],
                    'night': counter_doc['night'],
                    'total': counter_doc['total'],
                    'date': counter_doc['date'],
                    'price': counter_doc['price']
                },
                {
                    'number': 123,
                    'day': 15,
                    'night': 25,
                    'total': expected_total,
                    'date': '2022-01-01',
                    'price': expected_price
                }
            )


    def test_lower_night_reading(self):
        # Тест із нажчинеми нічними показниками
        with patch.object(main, 'db', new=self.db):
            self.db.Counter.insert_one({'number': 123, 'day': 10, 'night': 30})
            main.insert_counter_data(123, '2022-01-01', 15, 25)
            
            latest_price_doc = self.db.Prices.find_one()
            
            expected_total = latest_price_doc['addition_day'] + latest_price_doc['addition_night']
            
            expected_price = float(latest_price_doc['day_price'] * latest_price_doc['addition_day'] + latest_price_doc['night_price'] * latest_price_doc['addition_night'])
            
            counter_doc = self.db.Counter.find_one({'number': 123, 'date': '2022-01-01'})
            self.assertEqual({
                    'number': counter_doc['number'],
                    'day': counter_doc['day'],
                    'night': counter_doc['night'],
                    'total': counter_doc['total'],
                    'date': counter_doc['date'],
                    'price': counter_doc['price']
                },
                {
                    'number': 123,
                    'day': 15,
                    'night': 25,
                    'total': expected_total,
                    'date': '2022-01-01',
                    'price': expected_price})


    def test_lower_day_reading(self):
        # Тест із нажчими денними денними показниками
        with patch.object(main, 'db', new=self.db):
            self.db.Counter.insert_one({'number': 123, 'day': 20, 'night': 20})
            main.insert_counter_data(123, '2022-01-01', 15, 25)
            
            latest_price_doc = self.db.Prices.find_one()
            
            expected_total = latest_price_doc['addition_day'] + latest_price_doc['addition_night']
            
            expected_price = float(latest_price_doc['day_price'] * latest_price_doc['addition_day'] + latest_price_doc['night_price'] * latest_price_doc['addition_night'])
            
            counter_doc = self.db.Counter.find_one({'number': 123, 'date': '2022-01-01'})
            self.assertEqual({
                    'number': counter_doc['number'],
                    'day': counter_doc['day'],
                    'night': counter_doc['night'],
                    'total': counter_doc['total'],
                    'date': counter_doc['date'],
                    'price': counter_doc['price']
                },
                {
                    'number': 123,
                    'day': 15,
                    'night': 25,
                    'total': expected_total,
                    'date': '2022-01-01',
                    'price': expected_price})

    def test_lower_day_and_night_readings(self):
    # Тест із нажчинеми денними і нічними показниками
        with patch.object(main, 'db', new=self.db):
            self.db.Counter.insert_one({'number': 123, 'day': 20, 'night': 30})
            main.insert_counter_data(123, '2022-01-01', 15, 25)
            
            latest_price_doc = self.db.Prices.find_one()
            
            expected_total = latest_price_doc['addition_day'] + latest_price_doc['addition_night']
            
            expected_price = float(latest_price_doc['day_price'] * latest_price_doc['addition_day'] + latest_price_doc['night_price'] * latest_price_doc['addition_night'])
            
            counter_doc = self.db.Counter.find_one({'number': 123, 'date': '2022-01-01'})
            self.assertEqual({
                    'number': counter_doc['number'],
                    'day': counter_doc['day'],
                    'night': counter_doc['night'],
                    'total': counter_doc['total'],
                    'date': counter_doc['date'],
                    'price': counter_doc['price']
                },
                {
                    'number': 123,
                    'day': 15,
                    'night': 25,
                    'total': expected_total,
                    'date': '2022-01-01',
                    'price': expected_price})

if __name__ == '__main__':
    unittest.main()
