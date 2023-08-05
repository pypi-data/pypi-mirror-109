# coding: utf-8

"""
    Hydrogen Nucleus API

    The Hydrogen Nucleus API  # noqa: E501

    OpenAPI spec version: 1.9.0
    Contact: info@hydrogenplatform.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import unittest

import nucleus_api
from nucleus_api.api.roundup_api import RoundupApi  # noqa: E501
from nucleus_api.rest import ApiException


class TestRoundupApi(unittest.TestCase):
    """RoundupApi unit test stubs"""

    def setUp(self):
        self.api = nucleus_api.api.roundup_api.RoundupApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_roundup_settings_using_post(self):
        """Test case for create_roundup_settings_using_post

        Create a Roundup Settings  # noqa: E501
        """
        pass

    def test_create_roundup_using_post(self):
        """Test case for create_roundup_using_post

        Create a roundup  # noqa: E501
        """
        pass

    def test_delete_roundup_settings_using_delete(self):
        """Test case for delete_roundup_settings_using_delete

        Delete a roundup settings  # noqa: E501
        """
        pass

    def test_get_roundup_all_using_get(self):
        """Test case for get_roundup_all_using_get

        List all roundups  # noqa: E501
        """
        pass

    def test_get_roundup_settings_all_using_get(self):
        """Test case for get_roundup_settings_all_using_get

        List all roundup settings  # noqa: E501
        """
        pass

    def test_get_roundup_settings_using_get(self):
        """Test case for get_roundup_settings_using_get

        Retrieve a Roundup Setting  # noqa: E501
        """
        pass

    def test_get_roundup_using_get(self):
        """Test case for get_roundup_using_get

        Retrieve a Roundup  # noqa: E501
        """
        pass

    def test_update_roundup_settings_using_put(self):
        """Test case for update_roundup_settings_using_put

        Update a roundup settings  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
