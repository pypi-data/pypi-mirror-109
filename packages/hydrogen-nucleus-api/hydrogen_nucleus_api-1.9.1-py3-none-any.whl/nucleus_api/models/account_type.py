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


class AccountType(object):
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
        'code': 'str',
        'create_date': 'datetime',
        'id': 'str',
        'is_active': 'bool',
        'is_asset': 'bool',
        'is_business': 'bool',
        'is_cash': 'bool',
        'is_investment': 'bool',
        'is_taxable': 'bool',
        'metadata': 'dict(str, str)',
        'name': 'str',
        'secondary_id': 'str',
        'short_name': 'str',
        'subcategory': 'str',
        'update_date': 'datetime'
    }

    attribute_map = {
        'category': 'category',
        'code': 'code',
        'create_date': 'create_date',
        'id': 'id',
        'is_active': 'is_active',
        'is_asset': 'is_asset',
        'is_business': 'is_business',
        'is_cash': 'is_cash',
        'is_investment': 'is_investment',
        'is_taxable': 'is_taxable',
        'metadata': 'metadata',
        'name': 'name',
        'secondary_id': 'secondary_id',
        'short_name': 'short_name',
        'subcategory': 'subcategory',
        'update_date': 'update_date'
    }

    def __init__(self, category=None, code=None, create_date=None, id=None, is_active=None, is_asset=None, is_business=None, is_cash=None, is_investment=None, is_taxable=None, metadata=None, name=None, secondary_id=None, short_name=None, subcategory=None, update_date=None, _configuration=None):  # noqa: E501
        """AccountType - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._category = None
        self._code = None
        self._create_date = None
        self._id = None
        self._is_active = None
        self._is_asset = None
        self._is_business = None
        self._is_cash = None
        self._is_investment = None
        self._is_taxable = None
        self._metadata = None
        self._name = None
        self._secondary_id = None
        self._short_name = None
        self._subcategory = None
        self._update_date = None
        self.discriminator = None

        if category is not None:
            self.category = category
        if code is not None:
            self.code = code
        if create_date is not None:
            self.create_date = create_date
        if id is not None:
            self.id = id
        if is_active is not None:
            self.is_active = is_active
        if is_asset is not None:
            self.is_asset = is_asset
        if is_business is not None:
            self.is_business = is_business
        if is_cash is not None:
            self.is_cash = is_cash
        if is_investment is not None:
            self.is_investment = is_investment
        if is_taxable is not None:
            self.is_taxable = is_taxable
        if metadata is not None:
            self.metadata = metadata
        self.name = name
        if secondary_id is not None:
            self.secondary_id = secondary_id
        if short_name is not None:
            self.short_name = short_name
        if subcategory is not None:
            self.subcategory = subcategory
        if update_date is not None:
            self.update_date = update_date

    @property
    def category(self):
        """Gets the category of this AccountType.  # noqa: E501

        category  # noqa: E501

        :return: The category of this AccountType.  # noqa: E501
        :rtype: str
        """
        return self._category

    @category.setter
    def category(self, category):
        """Sets the category of this AccountType.

        category  # noqa: E501

        :param category: The category of this AccountType.  # noqa: E501
        :type: str
        """

        self._category = category

    @property
    def code(self):
        """Gets the code of this AccountType.  # noqa: E501

        code  # noqa: E501

        :return: The code of this AccountType.  # noqa: E501
        :rtype: str
        """
        return self._code

    @code.setter
    def code(self, code):
        """Sets the code of this AccountType.

        code  # noqa: E501

        :param code: The code of this AccountType.  # noqa: E501
        :type: str
        """

        self._code = code

    @property
    def create_date(self):
        """Gets the create_date of this AccountType.  # noqa: E501


        :return: The create_date of this AccountType.  # noqa: E501
        :rtype: datetime
        """
        return self._create_date

    @create_date.setter
    def create_date(self, create_date):
        """Sets the create_date of this AccountType.


        :param create_date: The create_date of this AccountType.  # noqa: E501
        :type: datetime
        """

        self._create_date = create_date

    @property
    def id(self):
        """Gets the id of this AccountType.  # noqa: E501


        :return: The id of this AccountType.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this AccountType.


        :param id: The id of this AccountType.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def is_active(self):
        """Gets the is_active of this AccountType.  # noqa: E501

        isActive  # noqa: E501

        :return: The is_active of this AccountType.  # noqa: E501
        :rtype: bool
        """
        return self._is_active

    @is_active.setter
    def is_active(self, is_active):
        """Sets the is_active of this AccountType.

        isActive  # noqa: E501

        :param is_active: The is_active of this AccountType.  # noqa: E501
        :type: bool
        """

        self._is_active = is_active

    @property
    def is_asset(self):
        """Gets the is_asset of this AccountType.  # noqa: E501

        isAsset  # noqa: E501

        :return: The is_asset of this AccountType.  # noqa: E501
        :rtype: bool
        """
        return self._is_asset

    @is_asset.setter
    def is_asset(self, is_asset):
        """Sets the is_asset of this AccountType.

        isAsset  # noqa: E501

        :param is_asset: The is_asset of this AccountType.  # noqa: E501
        :type: bool
        """

        self._is_asset = is_asset

    @property
    def is_business(self):
        """Gets the is_business of this AccountType.  # noqa: E501

        isBusiness  # noqa: E501

        :return: The is_business of this AccountType.  # noqa: E501
        :rtype: bool
        """
        return self._is_business

    @is_business.setter
    def is_business(self, is_business):
        """Sets the is_business of this AccountType.

        isBusiness  # noqa: E501

        :param is_business: The is_business of this AccountType.  # noqa: E501
        :type: bool
        """

        self._is_business = is_business

    @property
    def is_cash(self):
        """Gets the is_cash of this AccountType.  # noqa: E501

        isCash  # noqa: E501

        :return: The is_cash of this AccountType.  # noqa: E501
        :rtype: bool
        """
        return self._is_cash

    @is_cash.setter
    def is_cash(self, is_cash):
        """Sets the is_cash of this AccountType.

        isCash  # noqa: E501

        :param is_cash: The is_cash of this AccountType.  # noqa: E501
        :type: bool
        """

        self._is_cash = is_cash

    @property
    def is_investment(self):
        """Gets the is_investment of this AccountType.  # noqa: E501

        isInvestment  # noqa: E501

        :return: The is_investment of this AccountType.  # noqa: E501
        :rtype: bool
        """
        return self._is_investment

    @is_investment.setter
    def is_investment(self, is_investment):
        """Sets the is_investment of this AccountType.

        isInvestment  # noqa: E501

        :param is_investment: The is_investment of this AccountType.  # noqa: E501
        :type: bool
        """

        self._is_investment = is_investment

    @property
    def is_taxable(self):
        """Gets the is_taxable of this AccountType.  # noqa: E501

        isTaxable  # noqa: E501

        :return: The is_taxable of this AccountType.  # noqa: E501
        :rtype: bool
        """
        return self._is_taxable

    @is_taxable.setter
    def is_taxable(self, is_taxable):
        """Sets the is_taxable of this AccountType.

        isTaxable  # noqa: E501

        :param is_taxable: The is_taxable of this AccountType.  # noqa: E501
        :type: bool
        """

        self._is_taxable = is_taxable

    @property
    def metadata(self):
        """Gets the metadata of this AccountType.  # noqa: E501


        :return: The metadata of this AccountType.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this AccountType.


        :param metadata: The metadata of this AccountType.  # noqa: E501
        :type: dict(str, str)
        """

        self._metadata = metadata

    @property
    def name(self):
        """Gets the name of this AccountType.  # noqa: E501

        name  # noqa: E501

        :return: The name of this AccountType.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this AccountType.

        name  # noqa: E501

        :param name: The name of this AccountType.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def secondary_id(self):
        """Gets the secondary_id of this AccountType.  # noqa: E501


        :return: The secondary_id of this AccountType.  # noqa: E501
        :rtype: str
        """
        return self._secondary_id

    @secondary_id.setter
    def secondary_id(self, secondary_id):
        """Sets the secondary_id of this AccountType.


        :param secondary_id: The secondary_id of this AccountType.  # noqa: E501
        :type: str
        """

        self._secondary_id = secondary_id

    @property
    def short_name(self):
        """Gets the short_name of this AccountType.  # noqa: E501

        shortName  # noqa: E501

        :return: The short_name of this AccountType.  # noqa: E501
        :rtype: str
        """
        return self._short_name

    @short_name.setter
    def short_name(self, short_name):
        """Sets the short_name of this AccountType.

        shortName  # noqa: E501

        :param short_name: The short_name of this AccountType.  # noqa: E501
        :type: str
        """

        self._short_name = short_name

    @property
    def subcategory(self):
        """Gets the subcategory of this AccountType.  # noqa: E501

        subcategory  # noqa: E501

        :return: The subcategory of this AccountType.  # noqa: E501
        :rtype: str
        """
        return self._subcategory

    @subcategory.setter
    def subcategory(self, subcategory):
        """Sets the subcategory of this AccountType.

        subcategory  # noqa: E501

        :param subcategory: The subcategory of this AccountType.  # noqa: E501
        :type: str
        """

        self._subcategory = subcategory

    @property
    def update_date(self):
        """Gets the update_date of this AccountType.  # noqa: E501


        :return: The update_date of this AccountType.  # noqa: E501
        :rtype: datetime
        """
        return self._update_date

    @update_date.setter
    def update_date(self, update_date):
        """Sets the update_date of this AccountType.


        :param update_date: The update_date of this AccountType.  # noqa: E501
        :type: datetime
        """

        self._update_date = update_date

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
        if issubclass(AccountType, dict):
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
        if not isinstance(other, AccountType):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AccountType):
            return True

        return self.to_dict() != other.to_dict()
