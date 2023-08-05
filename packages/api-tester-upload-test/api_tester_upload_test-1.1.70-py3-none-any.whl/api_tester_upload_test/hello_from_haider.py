# -*- coding: utf-8 -*-

"""
    api_tester_upload_test

    This file was automatically generated for Stamplay by APIMATIC v2.0 ( https://apimatic.io ).
"""

from api_tester_upload_test.decorators import lazy_property
from api_tester_upload_test.configuration import Configuration
from api_tester_upload_test.controllers.form_params_controller import FormParamsController
from api_tester_upload_test.controllers.query_params_controller import QueryParamsController
from api_tester_upload_test.controllers.body_params_controller import BodyParamsController
from api_tester_upload_test.controllers.error_codes_controller import ErrorCodesController
from api_tester_upload_test.controllers.response_types_controller import ResponseTypesController
from api_tester_upload_test.controllers.query_param_controller import QueryParamController
from api_tester_upload_test.controllers.template_params_controller import TemplateParamsController
from api_tester_upload_test.controllers.header_controller import HeaderController
from api_tester_upload_test.controllers.echo_controller import EchoController


class HelloFromHaider(object):

    config = Configuration

    @lazy_property
    def form_params(self):
        return FormParamsController()

    @lazy_property
    def query_params(self):
        return QueryParamsController()

    @lazy_property
    def body_params(self):
        return BodyParamsController()

    @lazy_property
    def error_codes(self):
        return ErrorCodesController()

    @lazy_property
    def response_types(self):
        return ResponseTypesController()

    @lazy_property
    def query_param(self):
        return QueryParamController()

    @lazy_property
    def template_params(self):
        return TemplateParamsController()

    @lazy_property
    def header(self):
        return HeaderController()

    @lazy_property
    def echo(self):
        return EchoController()


    def __init__(self,
                 square_version='2019-05-08',
                 auth_user_name=None,
                 auth_password=None,
                 use_hmac_authentication=False):
        if square_version is not None:
            Configuration.square_version = square_version
        if use_hmac_authentication:
            Configuration.hmac_auth_user_name = auth_user_name
            Configuration.hmac_auth_password = auth_password
        else:
            Configuration.basic_auth_user_name = auth_user_name
            Configuration.basic_auth_password = auth_password

