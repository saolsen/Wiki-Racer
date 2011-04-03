#!/usr/bin/env python
# This is the test suite for the wikiparse scripts used to parese the wikipedia
# xml db dump into a redis database.

import wikiparse # Parses the db dump into a flat file of nodes
import unittest2

class parsePageTestCase(unittest2.TestCase):
    def setUp(self):
        f = open('./testdata/anarchism.page', 'r')
        self.testRealPage = "".join(f.readlines())
        f.close()
        f = open('./testdata/testpage.page', 'r')
        self.testFakePage = "".join(f.readlines())
        f.close()    

    def testReal(self):
        pass

    def testFake(self):
        self.fakeNode = wikiparse.parsePage(self.testFakePage)
        result = 'Test Page|link one,link two,there,how about another link'
        self.assertEqual(self.fakeNode, result)

class parseRedirectTestCase(unittest2.TestCase):
    def setUp(self):
        f = open('./testdata/accessablecomputing.redirect', 'r')
        self.testRedirect = f.readlines()
        f.close()
 
    def testRedirect(self):
        self.redirect = wikiparse.parseRedirect(self.testRedirect)
        result = 'AccessibleComputing:Computer accessibility'
        self.assertEqual(self.redirect, result)

class checkTypeTestCase(unittest2.TestCase):
    pass

class mainTestCase(unittest2.TestCase):
    pass

if __name__ == '__main__':
    unittest2.main()
