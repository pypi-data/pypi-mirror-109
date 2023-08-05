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


class AllocationComposition(object):
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
        'allocation_id': 'str',
        'core': 'bool',
        'create_date': 'datetime',
        'current_weight': 'float',
        '_date': 'date',
        'id': 'str',
        'metadata': 'dict(str, str)',
        'model_id': 'str',
        'secondary_id': 'str',
        'strategic_weight': 'float',
        'update_date': 'datetime'
    }

    attribute_map = {
        'allocation_id': 'allocation_id',
        'core': 'core',
        'create_date': 'create_date',
        'current_weight': 'current_weight',
        '_date': 'date',
        'id': 'id',
        'metadata': 'metadata',
        'model_id': 'model_id',
        'secondary_id': 'secondary_id',
        'strategic_weight': 'strategic_weight',
        'update_date': 'update_date'
    }

    def __init__(self, allocation_id=None, core=None, create_date=None, current_weight=None, _date=None, id=None, metadata=None, model_id=None, secondary_id=None, strategic_weight=None, update_date=None, _configuration=None):  # noqa: E501
        """AllocationComposition - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._allocation_id = None
        self._core = None
        self._create_date = None
        self._current_weight = None
        self.__date = None
        self._id = None
        self._metadata = None
        self._model_id = None
        self._secondary_id = None
        self._strategic_weight = None
        self._update_date = None
        self.discriminator = None

        self.allocation_id = allocation_id
        if core is not None:
            self.core = core
        if create_date is not None:
            self.create_date = create_date
        self.current_weight = current_weight
        self._date = _date
        if id is not None:
            self.id = id
        if metadata is not None:
            self.metadata = metadata
        self.model_id = model_id
        if secondary_id is not None:
            self.secondary_id = secondary_id
        self.strategic_weight = strategic_weight
        if update_date is not None:
            self.update_date = update_date

    @property
    def allocation_id(self):
        """Gets the allocation_id of this AllocationComposition.  # noqa: E501

        allocationId  # noqa: E501

        :return: The allocation_id of this AllocationComposition.  # noqa: E501
        :rtype: str
        """
        return self._allocation_id

    @allocation_id.setter
    def allocation_id(self, allocation_id):
        """Sets the allocation_id of this AllocationComposition.

        allocationId  # noqa: E501

        :param allocation_id: The allocation_id of this AllocationComposition.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and allocation_id is None:
            raise ValueError("Invalid value for `allocation_id`, must not be `None`")  # noqa: E501

        self._allocation_id = allocation_id

    @property
    def core(self):
        """Gets the core of this AllocationComposition.  # noqa: E501

        core  # noqa: E501

        :return: The core of this AllocationComposition.  # noqa: E501
        :rtype: bool
        """
        return self._core

    @core.setter
    def core(self, core):
        """Sets the core of this AllocationComposition.

        core  # noqa: E501

        :param core: The core of this AllocationComposition.  # noqa: E501
        :type: bool
        """

        self._core = core

    @property
    def create_date(self):
        """Gets the create_date of this AllocationComposition.  # noqa: E501


        :return: The create_date of this AllocationComposition.  # noqa: E501
        :rtype: datetime
        """
        return self._create_date

    @create_date.setter
    def create_date(self, create_date):
        """Sets the create_date of this AllocationComposition.


        :param create_date: The create_date of this AllocationComposition.  # noqa: E501
        :type: datetime
        """

        self._create_date = create_date

    @property
    def current_weight(self):
        """Gets the current_weight of this AllocationComposition.  # noqa: E501

        currentWeight  # noqa: E501

        :return: The current_weight of this AllocationComposition.  # noqa: E501
        :rtype: float
        """
        return self._current_weight

    @current_weight.setter
    def current_weight(self, current_weight):
        """Sets the current_weight of this AllocationComposition.

        currentWeight  # noqa: E501

        :param current_weight: The current_weight of this AllocationComposition.  # noqa: E501
        :type: float
        """
        if self._configuration.client_side_validation and current_weight is None:
            raise ValueError("Invalid value for `current_weight`, must not be `None`")  # noqa: E501

        self._current_weight = current_weight

    @property
    def _date(self):
        """Gets the _date of this AllocationComposition.  # noqa: E501

        date  # noqa: E501

        :return: The _date of this AllocationComposition.  # noqa: E501
        :rtype: date
        """
        return self.__date

    @_date.setter
    def _date(self, _date):
        """Sets the _date of this AllocationComposition.

        date  # noqa: E501

        :param _date: The _date of this AllocationComposition.  # noqa: E501
        :type: date
        """
        if self._configuration.client_side_validation and _date is None:
            raise ValueError("Invalid value for `_date`, must not be `None`")  # noqa: E501

        self.__date = _date

    @property
    def id(self):
        """Gets the id of this AllocationComposition.  # noqa: E501


        :return: The id of this AllocationComposition.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this AllocationComposition.


        :param id: The id of this AllocationComposition.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def metadata(self):
        """Gets the metadata of this AllocationComposition.  # noqa: E501


        :return: The metadata of this AllocationComposition.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this AllocationComposition.


        :param metadata: The metadata of this AllocationComposition.  # noqa: E501
        :type: dict(str, str)
        """

        self._metadata = metadata

    @property
    def model_id(self):
        """Gets the model_id of this AllocationComposition.  # noqa: E501

        modelId  # noqa: E501

        :return: The model_id of this AllocationComposition.  # noqa: E501
        :rtype: str
        """
        return self._model_id

    @model_id.setter
    def model_id(self, model_id):
        """Sets the model_id of this AllocationComposition.

        modelId  # noqa: E501

        :param model_id: The model_id of this AllocationComposition.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and model_id is None:
            raise ValueError("Invalid value for `model_id`, must not be `None`")  # noqa: E501

        self._model_id = model_id

    @property
    def secondary_id(self):
        """Gets the secondary_id of this AllocationComposition.  # noqa: E501


        :return: The secondary_id of this AllocationComposition.  # noqa: E501
        :rtype: str
        """
        return self._secondary_id

    @secondary_id.setter
    def secondary_id(self, secondary_id):
        """Sets the secondary_id of this AllocationComposition.


        :param secondary_id: The secondary_id of this AllocationComposition.  # noqa: E501
        :type: str
        """

        self._secondary_id = secondary_id

    @property
    def strategic_weight(self):
        """Gets the strategic_weight of this AllocationComposition.  # noqa: E501

        strategicWeight  # noqa: E501

        :return: The strategic_weight of this AllocationComposition.  # noqa: E501
        :rtype: float
        """
        return self._strategic_weight

    @strategic_weight.setter
    def strategic_weight(self, strategic_weight):
        """Sets the strategic_weight of this AllocationComposition.

        strategicWeight  # noqa: E501

        :param strategic_weight: The strategic_weight of this AllocationComposition.  # noqa: E501
        :type: float
        """
        if self._configuration.client_side_validation and strategic_weight is None:
            raise ValueError("Invalid value for `strategic_weight`, must not be `None`")  # noqa: E501

        self._strategic_weight = strategic_weight

    @property
    def update_date(self):
        """Gets the update_date of this AllocationComposition.  # noqa: E501


        :return: The update_date of this AllocationComposition.  # noqa: E501
        :rtype: datetime
        """
        return self._update_date

    @update_date.setter
    def update_date(self, update_date):
        """Sets the update_date of this AllocationComposition.


        :param update_date: The update_date of this AllocationComposition.  # noqa: E501
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
        if issubclass(AllocationComposition, dict):
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
        if not isinstance(other, AllocationComposition):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AllocationComposition):
            return True

        return self.to_dict() != other.to_dict()
