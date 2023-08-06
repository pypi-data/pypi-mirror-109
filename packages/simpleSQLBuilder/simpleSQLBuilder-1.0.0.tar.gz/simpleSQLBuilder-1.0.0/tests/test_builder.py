import unittest
from simpleSQLBuilder.QueryBuilder import QueryBuilder


class BuilderTest(unittest.TestCase):

    def test_builder_v1(self):
        self.assertEqual(
            QueryBuilder().from_('users').select('id').select(
                'name', 'email').where('id < 3').build().result,
            'SELECT id,name,email FROM users WHERE id < 3'
        )

    def test_builder_v2(self):
        self.assertEqual(
            QueryBuilder().from_('users').select('id').select('name', 'email').where('id < 3').select('coin').where('coin > 100').build().result,
            'SELECT id,name,email,coin FROM users WHERE id < 3 AND coin > 100'
        )

    def test_builder_v3(self):
        self.assertEqual(
            QueryBuilder().from_('users').where('id < 3').where('coin > 100').build().result,
            'SELECT * FROM users WHERE id < 3 AND coin > 100'
        )