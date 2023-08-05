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
from nucleus_api.api.utils_api import UtilsApi  # noqa: E501
from nucleus_api.rest import ApiException


class TestUtilsApi(unittest.TestCase):
    """UtilsApi unit test stubs"""

    def setUp(self):
        self.api = nucleus_api.api.utils_api.UtilsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_application_using_post(self):
        """Test case for create_application_using_post

        Create an application  # noqa: E501
        """
        pass

    def test_create_audit_log_using_post(self):
        """Test case for create_audit_log_using_post

        Create a audit log  # noqa: E501
        """
        pass

    def test_create_feature_track_using_post(self):
        """Test case for create_feature_track_using_post

        Create a Feature Track  # noqa: E501
        """
        pass

    def test_create_feature_using_post(self):
        """Test case for create_feature_using_post

        Create a  Feature  # noqa: E501
        """
        pass

    def test_create_notification_client_using_post(self):
        """Test case for create_notification_client_using_post

        Create a Notification Client  # noqa: E501
        """
        pass

    def test_create_notification_setting_using_post(self):
        """Test case for create_notification_setting_using_post

        Create a Notification Setting  # noqa: E501
        """
        pass

    def test_create_notification_using_post(self):
        """Test case for create_notification_using_post

        Create a Notification  # noqa: E501
        """
        pass

    def test_create_reason_code_using_post(self):
        """Test case for create_reason_code_using_post

        Create a reason code  # noqa: E501
        """
        pass

    def test_create_stage_using_post(self):
        """Test case for create_stage_using_post

        Create an account stage  # noqa: E501
        """
        pass

    def test_create_transaction_code_using_post(self):
        """Test case for create_transaction_code_using_post

        Create a transaction code  # noqa: E501
        """
        pass

    def test_delete_application_using_delete(self):
        """Test case for delete_application_using_delete

        Delete an Application  # noqa: E501
        """
        pass

    def test_delete_feature_track_using_delete(self):
        """Test case for delete_feature_track_using_delete

        Delete a Feature Track  # noqa: E501
        """
        pass

    def test_delete_feature_using_delete(self):
        """Test case for delete_feature_using_delete

        Delete a Feature  # noqa: E501
        """
        pass

    def test_delete_notification_client_using_delete(self):
        """Test case for delete_notification_client_using_delete

        Delete a Notification Client  # noqa: E501
        """
        pass

    def test_delete_notification_setting_using_delete(self):
        """Test case for delete_notification_setting_using_delete

        Delete a Notification Setting  # noqa: E501
        """
        pass

    def test_delete_notification_using_delete(self):
        """Test case for delete_notification_using_delete

        Delete a Notification  # noqa: E501
        """
        pass

    def test_delete_reason_code_using_delete(self):
        """Test case for delete_reason_code_using_delete

        Delete a reason code  # noqa: E501
        """
        pass

    def test_delete_stage_using_delete(self):
        """Test case for delete_stage_using_delete

        Delete an account stage  # noqa: E501
        """
        pass

    def test_delete_transaction_code_using_delete(self):
        """Test case for delete_transaction_code_using_delete

        Delete a transaction code  # noqa: E501
        """
        pass

    def test_get_application_all_using_get(self):
        """Test case for get_application_all_using_get

        List all Application  # noqa: E501
        """
        pass

    def test_get_application_using_get(self):
        """Test case for get_application_using_get

        Retrieve an Application  # noqa: E501
        """
        pass

    def test_get_audit_log_all_using_get(self):
        """Test case for get_audit_log_all_using_get

        List all audit log  # noqa: E501
        """
        pass

    def test_get_audit_log_using_get(self):
        """Test case for get_audit_log_using_get

        Retrieve a audit log  # noqa: E501
        """
        pass

    def test_get_feature_all_using_get(self):
        """Test case for get_feature_all_using_get

        List all Feature  # noqa: E501
        """
        pass

    def test_get_feature_track_all_using_get(self):
        """Test case for get_feature_track_all_using_get

        List all Feature track  # noqa: E501
        """
        pass

    def test_get_feature_track_using_get(self):
        """Test case for get_feature_track_using_get

        Retrieve a Feature track  # noqa: E501
        """
        pass

    def test_get_feature_using_get(self):
        """Test case for get_feature_using_get

        Retrieve a Feature  # noqa: E501
        """
        pass

    def test_get_notification_all_using_get(self):
        """Test case for get_notification_all_using_get

        Get All Notifications  # noqa: E501
        """
        pass

    def test_get_notification_client_all_using_get(self):
        """Test case for get_notification_client_all_using_get

        List all Notification Client  # noqa: E501
        """
        pass

    def test_get_notification_client_using_get(self):
        """Test case for get_notification_client_using_get

        Retrieve a Notification Client  # noqa: E501
        """
        pass

    def test_get_notification_setting_all_using_get(self):
        """Test case for get_notification_setting_all_using_get

        List all Notification Setting  # noqa: E501
        """
        pass

    def test_get_notification_setting_using_get(self):
        """Test case for get_notification_setting_using_get

        Retrieve a Notification Setting  # noqa: E501
        """
        pass

    def test_get_notification_using_get(self):
        """Test case for get_notification_using_get

        Get a Notification  # noqa: E501
        """
        pass

    def test_get_reason_code_all_using_get(self):
        """Test case for get_reason_code_all_using_get

        List all reason codes  # noqa: E501
        """
        pass

    def test_get_reason_code_using_get(self):
        """Test case for get_reason_code_using_get

        Retrieve a reason code  # noqa: E501
        """
        pass

    def test_get_stage_all_using_get(self):
        """Test case for get_stage_all_using_get

        List all account stages  # noqa: E501
        """
        pass

    def test_get_stage_using_get(self):
        """Test case for get_stage_using_get

        Retrieve an account stage  # noqa: E501
        """
        pass

    def test_get_transaction_code_all_using_get(self):
        """Test case for get_transaction_code_all_using_get

        List all transaction codes  # noqa: E501
        """
        pass

    def test_get_transaction_code_using_get(self):
        """Test case for get_transaction_code_using_get

        Retrieve a transaction code  # noqa: E501
        """
        pass

    def test_update_application_using_put(self):
        """Test case for update_application_using_put

        Update an Application  # noqa: E501
        """
        pass

    def test_update_feature_track_using_put(self):
        """Test case for update_feature_track_using_put

        Update a Feature Track  # noqa: E501
        """
        pass

    def test_update_feature_using_put(self):
        """Test case for update_feature_using_put

        Update a Feature  # noqa: E501
        """
        pass

    def test_update_notification_client_using_put(self):
        """Test case for update_notification_client_using_put

        Update a Notification Client  # noqa: E501
        """
        pass

    def test_update_notification_setting_using_put(self):
        """Test case for update_notification_setting_using_put

        Update a Notification Setting  # noqa: E501
        """
        pass

    def test_update_notification_using_put(self):
        """Test case for update_notification_using_put

        Update a Notification  # noqa: E501
        """
        pass

    def test_update_reason_code_using_put(self):
        """Test case for update_reason_code_using_put

        Update a reason code  # noqa: E501
        """
        pass

    def test_update_stage_using_put(self):
        """Test case for update_stage_using_put

        Update an account stage  # noqa: E501
        """
        pass

    def test_update_transaction_code_using_put(self):
        """Test case for update_transaction_code_using_put

        Update a transaction code  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
