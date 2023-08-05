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


class BusinessAddress(object):
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
        'address_line1': 'str',
        'address_line2': 'str',
        'city': 'str',
        'country': 'str',
        'is_primary': 'bool',
        'postalcode': 'str',
        'state': 'str',
        'type': 'str'
    }

    attribute_map = {
        'address_line1': 'address_line1',
        'address_line2': 'address_line2',
        'city': 'city',
        'country': 'country',
        'is_primary': 'is_primary',
        'postalcode': 'postalcode',
        'state': 'state',
        'type': 'type'
    }

    def __init__(self, address_line1=None, address_line2=None, city=None, country=None, is_primary=None, postalcode=None, state=None, type=None, _configuration=None):  # noqa: E501
        """BusinessAddress - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._address_line1 = None
        self._address_line2 = None
        self._city = None
        self._country = None
        self._is_primary = None
        self._postalcode = None
        self._state = None
        self._type = None
        self.discriminator = None

        self.address_line1 = address_line1
        if address_line2 is not None:
            self.address_line2 = address_line2
        self.city = city
        self.country = country
        if is_primary is not None:
            self.is_primary = is_primary
        if postalcode is not None:
            self.postalcode = postalcode
        self.state = state
        self.type = type

    @property
    def address_line1(self):
        """Gets the address_line1 of this BusinessAddress.  # noqa: E501

        addressLine1  # noqa: E501

        :return: The address_line1 of this BusinessAddress.  # noqa: E501
        :rtype: str
        """
        return self._address_line1

    @address_line1.setter
    def address_line1(self, address_line1):
        """Sets the address_line1 of this BusinessAddress.

        addressLine1  # noqa: E501

        :param address_line1: The address_line1 of this BusinessAddress.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and address_line1 is None:
            raise ValueError("Invalid value for `address_line1`, must not be `None`")  # noqa: E501

        self._address_line1 = address_line1

    @property
    def address_line2(self):
        """Gets the address_line2 of this BusinessAddress.  # noqa: E501

        addressLine2  # noqa: E501

        :return: The address_line2 of this BusinessAddress.  # noqa: E501
        :rtype: str
        """
        return self._address_line2

    @address_line2.setter
    def address_line2(self, address_line2):
        """Sets the address_line2 of this BusinessAddress.

        addressLine2  # noqa: E501

        :param address_line2: The address_line2 of this BusinessAddress.  # noqa: E501
        :type: str
        """

        self._address_line2 = address_line2

    @property
    def city(self):
        """Gets the city of this BusinessAddress.  # noqa: E501

        city  # noqa: E501

        :return: The city of this BusinessAddress.  # noqa: E501
        :rtype: str
        """
        return self._city

    @city.setter
    def city(self, city):
        """Sets the city of this BusinessAddress.

        city  # noqa: E501

        :param city: The city of this BusinessAddress.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and city is None:
            raise ValueError("Invalid value for `city`, must not be `None`")  # noqa: E501

        self._city = city

    @property
    def country(self):
        """Gets the country of this BusinessAddress.  # noqa: E501

        country  # noqa: E501

        :return: The country of this BusinessAddress.  # noqa: E501
        :rtype: str
        """
        return self._country

    @country.setter
    def country(self, country):
        """Sets the country of this BusinessAddress.

        country  # noqa: E501

        :param country: The country of this BusinessAddress.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and country is None:
            raise ValueError("Invalid value for `country`, must not be `None`")  # noqa: E501

        self._country = country

    @property
    def is_primary(self):
        """Gets the is_primary of this BusinessAddress.  # noqa: E501

         is_primary  # noqa: E501

        :return: The is_primary of this BusinessAddress.  # noqa: E501
        :rtype: bool
        """
        return self._is_primary

    @is_primary.setter
    def is_primary(self, is_primary):
        """Sets the is_primary of this BusinessAddress.

         is_primary  # noqa: E501

        :param is_primary: The is_primary of this BusinessAddress.  # noqa: E501
        :type: bool
        """

        self._is_primary = is_primary

    @property
    def postalcode(self):
        """Gets the postalcode of this BusinessAddress.  # noqa: E501

        postalcode  # noqa: E501

        :return: The postalcode of this BusinessAddress.  # noqa: E501
        :rtype: str
        """
        return self._postalcode

    @postalcode.setter
    def postalcode(self, postalcode):
        """Sets the postalcode of this BusinessAddress.

        postalcode  # noqa: E501

        :param postalcode: The postalcode of this BusinessAddress.  # noqa: E501
        :type: str
        """

        self._postalcode = postalcode

    @property
    def state(self):
        """Gets the state of this BusinessAddress.  # noqa: E501

        state  # noqa: E501

        :return: The state of this BusinessAddress.  # noqa: E501
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this BusinessAddress.

        state  # noqa: E501

        :param state: The state of this BusinessAddress.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and state is None:
            raise ValueError("Invalid value for `state`, must not be `None`")  # noqa: E501

        self._state = state

    @property
    def type(self):
        """Gets the type of this BusinessAddress.  # noqa: E501

        type  # noqa: E501

        :return: The type of this BusinessAddress.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this BusinessAddress.

        type  # noqa: E501

        :param type: The type of this BusinessAddress.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501

        self._type = type

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
        if issubclass(BusinessAddress, dict):
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
        if not isinstance(other, BusinessAddress):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, BusinessAddress):
            return True

        return self.to_dict() != other.to_dict()
