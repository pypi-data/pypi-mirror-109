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
from nucleus_api.api.household_api import HouseholdApi  # noqa: E501
from nucleus_api.rest import ApiException


class TestHouseholdApi(unittest.TestCase):
    """HouseholdApi unit test stubs"""

    def setUp(self):
        self.api = nucleus_api.api.household_api.HouseholdApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_household_using_post(self):
        """Test case for create_household_using_post

        Create a Household  # noqa: E501
        """
        pass

    def test_delete_household_using_delete(self):
        """Test case for delete_household_using_delete

        Delete a Household  # noqa: E501
        """
        pass

    def test_get_household_all_using_get(self):
        """Test case for get_household_all_using_get

        List all household  # noqa: E501
        """
        pass

    def test_get_household_client_asset_size_using_get(self):
        """Test case for get_household_client_asset_size_using_get

        List all household client asset sizes  # noqa: E501
        """
        pass

    def test_get_household_client_holding_using_get(self):
        """Test case for get_household_client_holding_using_get

        List all household's clientIds holdings  # noqa: E501
        """
        pass

    def test_get_household_client_transaction_using_get(self):
        """Test case for get_household_client_transaction_using_get

        List all household's client ids transactions  # noqa: E501
        """
        pass

    def test_get_household_using_get(self):
        """Test case for get_household_using_get

        Retrieve a Household  # noqa: E501
        """
        pass

    def test_update_household_using_put(self):
        """Test case for update_household_using_put

        Update a Household  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
