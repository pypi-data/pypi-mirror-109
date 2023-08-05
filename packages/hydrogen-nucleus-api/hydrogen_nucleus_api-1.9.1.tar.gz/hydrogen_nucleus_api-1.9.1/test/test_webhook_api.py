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
from nucleus_api.api.webhook_api import WebhookApi  # noqa: E501
from nucleus_api.rest import ApiException


class TestWebhookApi(unittest.TestCase):
    """WebhookApi unit test stubs"""

    def setUp(self):
        self.api = nucleus_api.api.webhook_api.WebhookApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_webhook_using_post(self):
        """Test case for create_webhook_using_post

        Create a webhook  # noqa: E501
        """
        pass

    def test_delete_webhook_using_delete(self):
        """Test case for delete_webhook_using_delete

        Delete a webhook  # noqa: E501
        """
        pass

    def test_get_webhook_all_using_get(self):
        """Test case for get_webhook_all_using_get

        List all webhooks  # noqa: E501
        """
        pass

    def test_get_webhook_using_get(self):
        """Test case for get_webhook_using_get

        Retrieve a webhook  # noqa: E501
        """
        pass

    def test_update_webhook_using_put(self):
        """Test case for update_webhook_using_put

        Update a webhook  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
