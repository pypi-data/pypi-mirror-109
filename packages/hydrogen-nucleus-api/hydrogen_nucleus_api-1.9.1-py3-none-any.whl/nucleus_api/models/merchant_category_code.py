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


class MerchantCategoryCode(object):
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
        'category': 'str',
        'description': 'str',
        'mcc': 'int',
        'subcategory': 'str',
        'transaction_category_id': 'str'
    }

    attribute_map = {
        'category': 'category',
        'description': 'description',
        'mcc': 'mcc',
        'subcategory': 'subcategory',
        'transaction_category_id': 'transaction_category_id'
    }

    def __init__(self, category=None, description=None, mcc=None, subcategory=None, transaction_category_id=None, _configuration=None):  # noqa: E501
        """MerchantCategoryCode - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._category = None
        self._description = None
        self._mcc = None
        self._subcategory = None
        self._transaction_category_id = None
        self.discriminator = None

        if category is not None:
            self.category = category
        if description is not None:
            self.description = description
        if mcc is not None:
            self.mcc = mcc
        if subcategory is not None:
            self.subcategory = subcategory
        self.transaction_category_id = transaction_category_id

    @property
    def category(self):
        """Gets the category of this MerchantCategoryCode.  # noqa: E501

        category  # noqa: E501

        :return: The category of this MerchantCategoryCode.  # noqa: E501
        :rtype: str
        """
        return self._category

    @category.setter
    def category(self, category):
        """Sets the category of this MerchantCategoryCode.

        category  # noqa: E501

        :param category: The category of this MerchantCategoryCode.  # noqa: E501
        :type: str
        """

        self._category = category

    @property
    def description(self):
        """Gets the description of this MerchantCategoryCode.  # noqa: E501

        description  # noqa: E501

        :return: The description of this MerchantCategoryCode.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this MerchantCategoryCode.

        description  # noqa: E501

        :param description: The description of this MerchantCategoryCode.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def mcc(self):
        """Gets the mcc of this MerchantCategoryCode.  # noqa: E501

        mcc  # noqa: E501

        :return: The mcc of this MerchantCategoryCode.  # noqa: E501
        :rtype: int
        """
        return self._mcc

    @mcc.setter
    def mcc(self, mcc):
        """Sets the mcc of this MerchantCategoryCode.

        mcc  # noqa: E501

        :param mcc: The mcc of this MerchantCategoryCode.  # noqa: E501
        :type: int
        """

        self._mcc = mcc

    @property
    def subcategory(self):
        """Gets the subcategory of this MerchantCategoryCode.  # noqa: E501

        subcategory  # noqa: E501

        :return: The subcategory of this MerchantCategoryCode.  # noqa: E501
        :rtype: str
        """
        return self._subcategory

    @subcategory.setter
    def subcategory(self, subcategory):
        """Sets the subcategory of this MerchantCategoryCode.

        subcategory  # noqa: E501

        :param subcategory: The subcategory of this MerchantCategoryCode.  # noqa: E501
        :type: str
        """

        self._subcategory = subcategory

    @property
    def transaction_category_id(self):
        """Gets the transaction_category_id of this MerchantCategoryCode.  # noqa: E501

        TransactionCategory id  # noqa: E501

        :return: The transaction_category_id of this MerchantCategoryCode.  # noqa: E501
        :rtype: str
        """
        return self._transaction_category_id

    @transaction_category_id.setter
    def transaction_category_id(self, transaction_category_id):
        """Sets the transaction_category_id of this MerchantCategoryCode.

        TransactionCategory id  # noqa: E501

        :param transaction_category_id: The transaction_category_id of this MerchantCategoryCode.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and transaction_category_id is None:
            raise ValueError("Invalid value for `transaction_category_id`, must not be `None`")  # noqa: E501

        self._transaction_category_id = transaction_category_id

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
        if issubclass(MerchantCategoryCode, dict):
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
        if not isinstance(other, MerchantCategoryCode):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, MerchantCategoryCode):
            return True

        return self.to_dict() != other.to_dict()
