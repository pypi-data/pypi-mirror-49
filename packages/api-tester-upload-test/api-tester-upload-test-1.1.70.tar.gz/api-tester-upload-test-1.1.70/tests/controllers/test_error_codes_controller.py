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
from api_tester_upload_test.exceptions.exception_with_date_exception import ExceptionWithDateException
from api_tester_upload_test.exceptions.exception_with_uuid_exception import ExceptionWithUUIDException
from api_tester_upload_test.exceptions.exception_with_dynamic_exception import ExceptionWithDynamicException
from api_tester_upload_test.exceptions.exception_with_precision_exception import ExceptionWithPrecisionException
from api_tester_upload_test.exceptions.exception_with_boolean_exception import ExceptionWithBooleanException
from api_tester_upload_test.exceptions.exception_with_long_exception import ExceptionWithLongException
from api_tester_upload_test.exceptions.exception_with_number_exception import ExceptionWithNumberException
from api_tester_upload_test.exceptions.exception_with_string_exception import ExceptionWithStringException
from api_tester_upload_test.exceptions.custom_error_response_exception import CustomErrorResponseException
from api_tester_upload_test.exceptions.exception_with_rfc_3339_date_time_exception import ExceptionWithRfc3339DateTimeException
from api_tester_upload_test.exceptions.unix_time_stamp_exception import UnixTimeStampException
from api_tester_upload_test.exceptions.rfc_1123_exception import Rfc1123Exception
from api_tester_upload_test.exceptions.local_test_exception import LocalTestException
from api_tester_upload_test.exceptions.nested_model_exception import NestedModelException
from api_tester_upload_test.exceptions.global_test_exception import GlobalTestException


class ErrorCodesControllerTests(ControllerTestBase):

    @classmethod
    def setUpClass(cls):
        super(ErrorCodesControllerTests, cls).setUpClass()
        cls.controller = cls.api_client.error_codes

    # Todo: Add description for test test_date_in_exception
    def test_date_in_exception(self):

        # Perform the API call through the SDK function
        with self.assertRaises(ExceptionWithDateException):
            result = self.controller.date_in_exception()

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 444)

    # Todo: Add description for test test_uuid_in_exception
    def test_uuid_in_exception(self):

        # Perform the API call through the SDK function
        with self.assertRaises(ExceptionWithUUIDException):
            result = self.controller.uuid_in_exception()

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 444)

    # Todo: Add description for test test_dynamic_in_exception
    def test_dynamic_in_exception(self):

        # Perform the API call through the SDK function
        with self.assertRaises(ExceptionWithDynamicException):
            result = self.controller.dynamic_in_exception()

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 444)

    # Todo: Add description for test test_precision_in_exception
    def test_precision_in_exception(self):

        # Perform the API call through the SDK function
        with self.assertRaises(ExceptionWithPrecisionException):
            result = self.controller.precision_in_exception()

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 444)

    # Todo: Add description for test test_boolean_in_exception
    def test_boolean_in_exception(self):

        # Perform the API call through the SDK function
        with self.assertRaises(ExceptionWithBooleanException):
            result = self.controller.boolean_in_exception()

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 444)

    # Todo: Add description for test test_long_in_exception
    def test_long_in_exception(self):

        # Perform the API call through the SDK function
        with self.assertRaises(ExceptionWithLongException):
            result = self.controller.long_in_exception()

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 444)

    # Todo: Add description for test test_number_in_exception
    def test_number_in_exception(self):

        # Perform the API call through the SDK function
        with self.assertRaises(ExceptionWithNumberException):
            result = self.controller.number_in_exception()

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 444)

    # Todo: Add description for test test_exception_with_string
    def test_exception_with_string(self):

        # Perform the API call through the SDK function
        with self.assertRaises(ExceptionWithStringException):
            result = self.controller.get_exception_with_string()

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 444)

    # Todo: Add description for test test_check_endpoint_level_exception
    def test_check_endpoint_level_exception(self):

        # Perform the API call through the SDK function
        with self.assertRaises(CustomErrorResponseException):
            result = self.controller.receive_endpoint_level_exception()

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 451)

    # Todo: Add description for test test_check_global_level_exception
    def test_check_global_level_exception(self):

        # Perform the API call through the SDK function
        with self.assertRaises(CustomErrorResponseException):
            result = self.controller.receive_global_level_exception()

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 450)

    # Todo: Add description for test test_test_rfc_3339_date_time_exception
    def test_test_rfc_3339_date_time_exception(self):

        # Perform the API call through the SDK function
        with self.assertRaises(ExceptionWithRfc3339DateTimeException):
            result = self.controller.receive_exception_with_rfc_3339_datetime()

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 444)

    # Todo: Add description for test test_receive_unix_timestamp_exception
    def test_receive_unix_timestamp_exception(self):

        # Perform the API call through the SDK function
        with self.assertRaises(UnixTimeStampException):
            result = self.controller.receive_exception_with_unixtimestamp_exception()

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 444)

    # Todo: Add description for test test_receive_rfc_1123_exception
    def test_receive_rfc_1123_exception(self):

        # Perform the API call through the SDK function
        with self.assertRaises(Rfc1123Exception):
            result = self.controller.receive_exception_with_rfc_1123_datetime()

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 444)

    # Todo: Add description for test test_get_501
    def test_get_501(self):

        # Perform the API call through the SDK function
        with self.assertRaises(NestedModelException):
            result = self.controller.get_501()

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 501)

    # Todo: Add description for test test_get_400
    def test_get_400(self):

        # Perform the API call through the SDK function
        with self.assertRaises(GlobalTestException):
            result = self.controller.get_400()

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 400)

    # Todo: Add description for test test_get_500
    def test_get_500(self):

        # Perform the API call through the SDK function
        with self.assertRaises(GlobalTestException):
            result = self.controller.get_500()

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 500)

    # Todo: Add description for test test_get_412_global_exception
    def test_get_412_global_exception(self):

        # Perform the API call through the SDK function
        with self.assertRaises(NestedModelException):
            result = self.controller.catch_412_global_error()

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 412)

