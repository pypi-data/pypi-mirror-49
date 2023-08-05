# -*- coding: utf-8 -*-

"""
    api_tester_upload_test

    This file was automatically generated for Stamplay by APIMATIC v2.0 ( https://apimatic.io ).
"""

import jsonpickle
import dateutil.parser
from .controller_test_base import ControllerTestBase
from ..test_helper import TestHelper
from api_tester_upload_test.api_helper import APIHelper


class QueryParamsControllerTests(ControllerTestBase):

    @classmethod
    def setUpClass(cls):
        super(QueryParamsControllerTests, cls).setUpClass()
        cls.controller = cls.api_client.query_params

    # Todo: Add description for test test_boolean_as_optional_in_query
    def test_boolean_as_optional_in_query(self):
        # Parameters for the API call
        boolean = True
        boolean_1 = True

        # Perform the API call through the SDK function
        result = self.controller.boolean_as_optional(boolean, boolean_1)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_rfc_1123_datetime_as_optional_in_query
    def test_rfc_1123_datetime_as_optional_in_query(self):
        # Parameters for the API call
        date_time = APIHelper.HttpDateTime.from_value('Sun, 06 Nov 1994 08:49:37 GMT').datetime
        date_time_1 = APIHelper.HttpDateTime.from_value('Sun, 06 Nov 1994 08:49:37 GMT').datetime

        # Perform the API call through the SDK function
        result = self.controller.rfc_1123_datetime_as_optional(date_time, date_time_1)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_rfc_3339_as_optional_in_query
    def test_rfc_3339_as_optional_in_query(self):
        # Parameters for the API call
        date_time = APIHelper.RFC3339DateTime.from_value('1994-02-13T14:01:54.9571247Z').datetime
        date_time_1 = APIHelper.RFC3339DateTime.from_value('1994-02-13T14:01:54.9571247Z').datetime

        # Perform the API call through the SDK function
        result = self.controller.rfc_3339_datetime_as_optional(date_time, date_time_1)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_date_as_optional_in_query
    def test_date_as_optional_in_query(self):
        # Parameters for the API call
        date = dateutil.parser.parse('1994-02-13').date()
        date_1 = dateutil.parser.parse('1994-02-13').date()

        # Perform the API call through the SDK function
        result = self.controller.send_date_as_optional(date, date_1)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_string_as_optional_in_query
    def test_string_as_optional_in_query(self):
        # Parameters for the API call
        string = 'test'
        string_1 = 'test'

        # Perform the API call through the SDK function
        result = self.controller.send_string_as_optional(string, string_1)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_unixtimestamp_as_optional_in_query
    def test_unixtimestamp_as_optional_in_query(self):
        # Parameters for the API call
        date_time = APIHelper.UnixDateTime.from_value(1484719381).datetime
        date_time_1 = APIHelper.UnixDateTime.from_value(1484719381).datetime

        # Perform the API call through the SDK function
        result = self.controller.unixdatetime_as_optional(date_time, date_time_1)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_number_as_optional_in_query
    def test_number_as_optional_in_query(self):
        # Parameters for the API call
        number = 1
        number_1 = 1

        # Perform the API call through the SDK function
        result = self.controller.send_number_as_optional(number, number_1)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_long_as_optional_in_query
    def test_long_as_optional_in_query(self):
        # Parameters for the API call
        long = 123123
        long_1 = 123123

        # Perform the API call through the SDK function
        result = self.controller.send_long_as_optional(long, long_1)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_precision_as_optional_in_query
    def test_precision_as_optional_in_query(self):
        # Parameters for the API call
        precision = 1.23
        precision_1 = 1.23

        # Perform the API call through the SDK function
        result = self.controller.precision_as_optional(precision, precision_1)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


