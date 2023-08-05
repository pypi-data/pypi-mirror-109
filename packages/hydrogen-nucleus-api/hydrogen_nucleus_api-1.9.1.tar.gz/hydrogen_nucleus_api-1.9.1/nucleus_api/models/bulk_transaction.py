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


class BulkTransaction(object):
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
        'create_date': 'datetime',
        'data': 'object',
        'id': 'str',
        'secondary_id': 'str',
        'status': 'str',
        'update_date': 'datetime'
    }

    attribute_map = {
        'create_date': 'create_date',
        'data': 'data',
        'id': 'id',
        'secondary_id': 'secondary_id',
        'status': 'status',
        'update_date': 'update_date'
    }

    def __init__(self, create_date=None, data=None, id=None, secondary_id=None, status=None, update_date=None, _configuration=None):  # noqa: E501
        """BulkTransaction - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._create_date = None
        self._data = None
        self._id = None
        self._secondary_id = None
        self._status = None
        self._update_date = None
        self.discriminator = None

        if create_date is not None:
            self.create_date = create_date
        if data is not None:
            self.data = data
        if id is not None:
            self.id = id
        if secondary_id is not None:
            self.secondary_id = secondary_id
        if status is not None:
            self.status = status
        if update_date is not None:
            self.update_date = update_date

    @property
    def create_date(self):
        """Gets the create_date of this BulkTransaction.  # noqa: E501


        :return: The create_date of this BulkTransaction.  # noqa: E501
        :rtype: datetime
        """
        return self._create_date

    @create_date.setter
    def create_date(self, create_date):
        """Sets the create_date of this BulkTransaction.


        :param create_date: The create_date of this BulkTransaction.  # noqa: E501
        :type: datetime
        """

        self._create_date = create_date

    @property
    def data(self):
        """Gets the data of this BulkTransaction.  # noqa: E501


        :return: The data of this BulkTransaction.  # noqa: E501
        :rtype: object
        """
        return self._data

    @data.setter
    def data(self, data):
        """Sets the data of this BulkTransaction.


        :param data: The data of this BulkTransaction.  # noqa: E501
        :type: object
        """

        self._data = data

    @property
    def id(self):
        """Gets the id of this BulkTransaction.  # noqa: E501


        :return: The id of this BulkTransaction.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this BulkTransaction.


        :param id: The id of this BulkTransaction.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def secondary_id(self):
        """Gets the secondary_id of this BulkTransaction.  # noqa: E501


        :return: The secondary_id of this BulkTransaction.  # noqa: E501
        :rtype: str
        """
        return self._secondary_id

    @secondary_id.setter
    def secondary_id(self, secondary_id):
        """Sets the secondary_id of this BulkTransaction.


        :param secondary_id: The secondary_id of this BulkTransaction.  # noqa: E501
        :type: str
        """

        self._secondary_id = secondary_id

    @property
    def status(self):
        """Gets the status of this BulkTransaction.  # noqa: E501


        :return: The status of this BulkTransaction.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this BulkTransaction.


        :param status: The status of this BulkTransaction.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def update_date(self):
        """Gets the update_date of this BulkTransaction.  # noqa: E501


        :return: The update_date of this BulkTransaction.  # noqa: E501
        :rtype: datetime
        """
        return self._update_date

    @update_date.setter
    def update_date(self, update_date):
        """Sets the update_date of this BulkTransaction.


        :param update_date: The update_date of this BulkTransaction.  # noqa: E501
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
        if issubclass(BulkTransaction, dict):
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
        if not isinstance(other, BulkTransaction):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, BulkTransaction):
            return True

        return self.to_dict() != other.to_dict()
