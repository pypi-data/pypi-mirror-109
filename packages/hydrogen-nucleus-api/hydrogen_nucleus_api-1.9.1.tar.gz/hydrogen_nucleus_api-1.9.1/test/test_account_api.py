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
from nucleus_api.api.account_api import AccountApi  # noqa: E501
from nucleus_api.rest import ApiException


class TestAccountApi(unittest.TestCase):
    """AccountApi unit test stubs"""

    def setUp(self):
        self.api = nucleus_api.api.account_api.AccountApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_account_allocation_mapping_using_post(self):
        """Test case for create_account_allocation_mapping_using_post

        Create an account allocation  # noqa: E501
        """
        pass

    def test_create_account_status_using_post(self):
        """Test case for create_account_status_using_post

        Create an account status  # noqa: E501
        """
        pass

    def test_create_account_type_using_post(self):
        """Test case for create_account_type_using_post

        Create an account type  # noqa: E501
        """
        pass

    def test_create_account_using_post(self):
        """Test case for create_account_using_post

        Create an account  # noqa: E501
        """
        pass

    def test_delete_account_allocation_mapping_using_delete(self):
        """Test case for delete_account_allocation_mapping_using_delete

        Delete an account allocation  # noqa: E501
        """
        pass

    def test_delete_account_permission_using_delete(self):
        """Test case for delete_account_permission_using_delete

        Delete an account permission  # noqa: E501
        """
        pass

    def test_delete_account_status_using_delete(self):
        """Test case for delete_account_status_using_delete

        Delete an account status  # noqa: E501
        """
        pass

    def test_delete_account_type_using_delete(self):
        """Test case for delete_account_type_using_delete

        Delete an account type  # noqa: E501
        """
        pass

    def test_delete_account_using_delete(self):
        """Test case for delete_account_using_delete

        Delete an account  # noqa: E501
        """
        pass

    def test_get_account_all_using_get(self):
        """Test case for get_account_all_using_get

        List all accounts  # noqa: E501
        """
        pass

    def test_get_account_allocation_mapping_all_using_get(self):
        """Test case for get_account_allocation_mapping_all_using_get

        List all account allocations  # noqa: E501
        """
        pass

    def test_get_account_allocation_mapping_using_get(self):
        """Test case for get_account_allocation_mapping_using_get

        Retrieve an account allocation  # noqa: E501
        """
        pass

    def test_get_account_asset_size_agg_all_using_get(self):
        """Test case for get_account_asset_size_agg_all_using_get

        List all account asset sizes  # noqa: E501
        """
        pass

    def test_get_account_overview_using_get(self):
        """Test case for get_account_overview_using_get

        List all Account overview  # noqa: E501
        """
        pass

    def test_get_account_permission_using_get(self):
        """Test case for get_account_permission_using_get

        Get an account permission  # noqa: E501
        """
        pass

    def test_get_account_status_all_using_get(self):
        """Test case for get_account_status_all_using_get

        List all account statuses  # noqa: E501
        """
        pass

    def test_get_account_status_using_get(self):
        """Test case for get_account_status_using_get

        Retrieve an account status  # noqa: E501
        """
        pass

    def test_get_account_type_all_using_get(self):
        """Test case for get_account_type_all_using_get

        List all account types  # noqa: E501
        """
        pass

    def test_get_account_type_using_get(self):
        """Test case for get_account_type_using_get

        Get an Account Type  # noqa: E501
        """
        pass

    def test_get_account_using_get(self):
        """Test case for get_account_using_get

        Retrieve an account  # noqa: E501
        """
        pass

    def test_get_all_account_permission_using_get(self):
        """Test case for get_all_account_permission_using_get

        List all account permission  # noqa: E501
        """
        pass

    def test_get_portfolio_holding_agg_all_using_get(self):
        """Test case for get_portfolio_holding_agg_all_using_get

        List all account holdings  # noqa: E501
        """
        pass

    def test_get_portfolio_transaction_agg_all_using_get(self):
        """Test case for get_portfolio_transaction_agg_all_using_get

        List all account transactions  # noqa: E501
        """
        pass

    def test_insert_account_and_related_permission_using_post(self):
        """Test case for insert_account_and_related_permission_using_post

        create an account permission  # noqa: E501
        """
        pass

    def test_subscribe_account_using_post(self):
        """Test case for subscribe_account_using_post

        Subscribe an account  # noqa: E501
        """
        pass

    def test_update_account_allocation_mapping_using_put(self):
        """Test case for update_account_allocation_mapping_using_put

        Update an account allocation  # noqa: E501
        """
        pass

    def test_update_account_status_using_put(self):
        """Test case for update_account_status_using_put

        Update an account status  # noqa: E501
        """
        pass

    def test_update_account_type_using_put(self):
        """Test case for update_account_type_using_put

        Update an account type  # noqa: E501
        """
        pass

    def test_update_account_using_put(self):
        """Test case for update_account_using_put

        Update an account  # noqa: E501
        """
        pass

    def test_update_client_account_permission_using_put(self):
        """Test case for update_client_account_permission_using_put

        Update an account permission  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
