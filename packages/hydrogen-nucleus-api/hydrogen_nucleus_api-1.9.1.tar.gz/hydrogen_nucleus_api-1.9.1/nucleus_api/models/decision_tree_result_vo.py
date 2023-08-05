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


class DecisionTreeResultVO(object):
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
        'entity_id': 'list[str]',
        'entity_type': 'str'
    }

    attribute_map = {
        'entity_id': 'entity_id',
        'entity_type': 'entity_type'
    }

    def __init__(self, entity_id=None, entity_type=None, _configuration=None):  # noqa: E501
        """DecisionTreeResultVO - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._entity_id = None
        self._entity_type = None
        self.discriminator = None

        if entity_id is not None:
            self.entity_id = entity_id
        if entity_type is not None:
            self.entity_type = entity_type

    @property
    def entity_id(self):
        """Gets the entity_id of this DecisionTreeResultVO.  # noqa: E501


        :return: The entity_id of this DecisionTreeResultVO.  # noqa: E501
        :rtype: list[str]
        """
        return self._entity_id

    @entity_id.setter
    def entity_id(self, entity_id):
        """Sets the entity_id of this DecisionTreeResultVO.


        :param entity_id: The entity_id of this DecisionTreeResultVO.  # noqa: E501
        :type: list[str]
        """

        self._entity_id = entity_id

    @property
    def entity_type(self):
        """Gets the entity_type of this DecisionTreeResultVO.  # noqa: E501


        :return: The entity_type of this DecisionTreeResultVO.  # noqa: E501
        :rtype: str
        """
        return self._entity_type

    @entity_type.setter
    def entity_type(self, entity_type):
        """Sets the entity_type of this DecisionTreeResultVO.


        :param entity_type: The entity_type of this DecisionTreeResultVO.  # noqa: E501
        :type: str
        """

        self._entity_type = entity_type

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
        if issubclass(DecisionTreeResultVO, dict):
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
        if not isinstance(other, DecisionTreeResultVO):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DecisionTreeResultVO):
            return True

        return self.to_dict() != other.to_dict()
