
import unittest 
from unittest import TestCase
from unittest.mock import patch # what does this do
from peewee import *

import db_config
test_db_path = 'test_peewee_chainsaw.sqlite'
db_config.database_path = test_db_path 

import chainsaw_juggling_peewee
from chainsaw_juggling_peewee import Juggler

class TestJuggler(TestCase):

    test_db_url = 'test_peewee_chainsaw.sqlite'

    """
    Before running these test, create test_peewee_chainsaw.sqlite
    Create expected juggler table
    """

    # The name of this method is important - the test runner will look for it
    def setUp(self):
        # clear and remake juggler table in test db based on Juggler 
        self.db = SqliteDatabase(test_db_path)
        self.db.drop_tables([Juggler])
        self.db.create_tables([Juggler])

    def test_add_one_juggler(self):
        chainsaw_juggling_peewee.add_juggler('Test Juggler', 'Test Country', 123)
        juggler = Juggler.get_or_none(Juggler.name=='Test Juggler', Juggler.country=='Test Country', Juggler.catches==123)
        self.assertIsNotNone(juggler)

    def test_edit_one_juggler(self):
        chainsaw_juggling_peewee.add_juggler('Test Juggler', 'Test Country', 123)
        chainsaw_juggling_peewee.edit_juggler('Test Juggler', 456)
        juggler = Juggler.get_or_none(Juggler.name=='Test Juggler', Juggler.country=='Test Country', Juggler.catches==456)
        self.assertIsNotNone(juggler)
        
    def test_delete_juggler(self):
        chainsaw_juggling_peewee.add_juggler('Test Juggler', 'Test Country', 123)
        chainsaw_juggling_peewee.delete_juggler('Test Juggler')
        juggler = Juggler.get_or_none(Juggler.name=='Test Juggler', Juggler.country=='Test Country', Juggler.catches==456)
        self.assertIsNone(juggler)

    def test_try_to_delete_juggler_not_in_database(self):
        chainsaw_juggling_peewee.add_juggler('Test Juggler', 'Test Country', 123)
        chainsaw_juggling_peewee.delete_juggler('Test2 Juggler2')
        # could have program raise a custom exception in order to test this ?
        # other ways to test? could modify function to return the error message instead of printing directly ?




if __name__ == '__main__':
    unittest.main()