# coding: utf-8

"""
    Hydrogen Nucleus API

    The Hydrogen Nucleus API  # noqa: E501

    OpenAPI spec version: 1.9.0
    Contact: info@hydrogenplatform.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from nucleus_api.configuration import Configuration


class ClientBusinessCardVO(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'business_details': 'BusinessDetailsVO',
        'card_details': 'list[CardDetailsVO]',
        'client_details': 'ClientCardVO',
        'total_balance': 'list[ClientBusinessTotalCardBalanceVO]'
    }

    attribute_map = {
        'business_details': 'business_details',
        'card_details': 'card_details',
        'client_details': 'client_details',
        'total_balance': 'total_balance'
    }

    def __init__(self, business_details=None, card_details=None, client_details=None, total_balance=None, _configuration=None):  # noqa: E501
        """ClientBusinessCardVO - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._business_details = None
        self._card_details = None
        self._client_details = None
        self._total_balance = None
        self.discriminator = None

        if business_details is not None:
            self.business_details = business_details
        if card_details is not None:
            self.card_details = card_details
        if client_details is not None:
            self.client_details = client_details
        if total_balance is not None:
            self.total_balance = total_balance

    @property
    def business_details(self):
        """Gets the business_details of this ClientBusinessCardVO.  # noqa: E501

        businessDetails  # noqa: E501

        :return: The business_details of this ClientBusinessCardVO.  # noqa: E501
        :rtype: BusinessDetailsVO
        """
        return self._business_details

    @business_details.setter
    def business_details(self, business_details):
        """Sets the business_details of this ClientBusinessCardVO.

        businessDetails  # noqa: E501

        :param business_details: The business_details of this ClientBusinessCardVO.  # noqa: E501
        :type: BusinessDetailsVO
        """

        self._business_details = business_details

    @property
    def card_details(self):
        """Gets the card_details of this ClientBusinessCardVO.  # noqa: E501

        cardDetails  # noqa: E501

        :return: The card_details of this ClientBusinessCardVO.  # noqa: E501
        :rtype: list[CardDetailsVO]
        """
        return self._card_details

    @card_details.setter
    def card_details(self, card_details):
        """Sets the card_details of this ClientBusinessCardVO.

        cardDetails  # noqa: E501

        :param card_details: The card_details of this ClientBusinessCardVO.  # noqa: E501
        :type: list[CardDetailsVO]
        """

        self._card_details = card_details

    @property
    def client_details(self):
        """Gets the client_details of this ClientBusinessCardVO.  # noqa: E501

        clientDetails  # noqa: E501

        :return: The client_details of this ClientBusinessCardVO.  # noqa: E501
        :rtype: ClientCardVO
        """
        return self._client_details

    @client_details.setter
    def client_details(self, client_details):
        """Sets the client_details of this ClientBusinessCardVO.

        clientDetails  # noqa: E501

        :param client_details: The client_details of this ClientBusinessCardVO.  # noqa: E501
        :type: ClientCardVO
        """

        self._client_details = client_details

    @property
    def total_balance(self):
        """Gets the total_balance of this ClientBusinessCardVO.  # noqa: E501

        totalBalance  # noqa: E501

        :return: The total_balance of this ClientBusinessCardVO.  # noqa: E501
        :rtype: list[ClientBusinessTotalCardBalanceVO]
        """
        return self._total_balance

    @total_balance.setter
    def total_balance(self, total_balance):
        """Sets the total_balance of this ClientBusinessCardVO.

        totalBalance  # noqa: E501

        :param total_balance: The total_balance of this ClientBusinessCardVO.  # noqa: E501
        :type: list[ClientBusinessTotalCardBalanceVO]
        """

        self._total_balance = total_balance

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(ClientBusinessCardVO, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ClientBusinessCardVO):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ClientBusinessCardVO):
            return True

        return self.to_dict() != other.to_dict()
