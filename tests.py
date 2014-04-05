#!/usr/bin/env python
import unittest
from pyoptionchain.google_api import *
from pyoptionchain.tk_gui import *

class TestOptionChain(unittest.TestCase):

    def test_connection_defaults(self):
        gOption = GoogleFinanceOption()        
        self.assertTrue(gOption.fetchData())

    def test_connection_fetch_puts_data(self):
        gOption = GoogleFinanceOption()
        gOption.fetchData()
        self.assertTrue(len(gOption.getPuts()) > 0)

    def test_connection_fetch_calls_data(self):
        gOption = GoogleFinanceOption()
        gOption.fetchData()
        self.assertTrue(len(gOption.getCalls()) > 0)

    def test_connection_fetch_expirations_data(self):
        gOption = GoogleFinanceOption()
        gOption.fetchData()
        self.assertTrue(len(gOption.getExpirations()) > 0)

    def test_connection_set_mdy_params(self):
        gOption = GoogleFinanceOption()
        gOption.setParameters({
            "expm": "4",
            "expd": "19",
            "expy": "2014"
        })
        gOption.fetchData()
        self.assertTrue(len(gOption.getPuts()) > 0)

if __name__ == "__main__":
    unittest.main()