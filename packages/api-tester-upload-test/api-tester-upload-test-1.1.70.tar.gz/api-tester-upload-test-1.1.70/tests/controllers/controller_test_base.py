# -*- coding: utf-8 -*-

"""
    api_tester_upload_test

    This file was automatically generated for Stamplay by APIMATIC v2.0 ( https://apimatic.io ).
"""

import unittest
from ..http_response_catcher import HttpResponseCatcher
from api_tester_upload_test.hello_from_haider import HelloFromHaider
from api_tester_upload_test.configuration import Configuration

class ControllerTestBase(unittest.TestCase):

    """All test classes inherit from this base class. It abstracts out
    common functionality and configuration variables set up."""

    @classmethod
    def setUpClass(cls):
        """Class method called once before running tests in a test class."""
        cls.api_client = HelloFromHaider()
        cls.request_timeout = 60
        cls.assert_precision = 0.1

        # Set Configuration parameters for test execution
        Configuration.port = '3000'
        Configuration.suites = 4
        Configuration.environment = Configuration.Environment.TESTING


    def setUp(self):
        """Method called once before every test in a test class."""
        self.response_catcher = HttpResponseCatcher()
        self.controller.http_call_back =  self.response_catcher

    