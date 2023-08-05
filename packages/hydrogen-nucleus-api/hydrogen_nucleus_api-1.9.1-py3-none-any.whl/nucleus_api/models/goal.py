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


class Goal(object):
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
        'accumulation_horizon': 'float',
        'category': 'str',
        'client_id': 'str',
        'create_date': 'datetime',
        'decumulation_horizon': 'float',
        'goal_amount': 'float',
        'id': 'str',
        'image': 'str',
        'is_active': 'bool',
        'is_decumulation': 'bool',
        'metadata': 'dict(str, str)',
        'name': 'str',
        'parent_goal_id': 'str',
        'questionnaire_id': 'str',
        'secondary_id': 'str',
        'type': 'str',
        'update_date': 'datetime'
    }

    attribute_map = {
        'accumulation_horizon': 'accumulation_horizon',
        'category': 'category',
        'client_id': 'client_id',
        'create_date': 'create_date',
        'decumulation_horizon': 'decumulation_horizon',
        'goal_amount': 'goal_amount',
        'id': 'id',
        'image': 'image',
        'is_active': 'is_active',
        'is_decumulation': 'is_decumulation',
        'metadata': 'metadata',
        'name': 'name',
        'parent_goal_id': 'parent_goal_id',
        'questionnaire_id': 'questionnaire_id',
        'secondary_id': 'secondary_id',
        'type': 'type',
        'update_date': 'update_date'
    }

    def __init__(self, accumulation_horizon=None, category=None, client_id=None, create_date=None, decumulation_horizon=None, goal_amount=None, id=None, image=None, is_active=None, is_decumulation=None, metadata=None, name=None, parent_goal_id=None, questionnaire_id=None, secondary_id=None, type=None, update_date=None, _configuration=None):  # noqa: E501
        """Goal - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._accumulation_horizon = None
        self._category = None
        self._client_id = None
        self._create_date = None
        self._decumulation_horizon = None
        self._goal_amount = None
        self._id = None
        self._image = None
        self._is_active = None
        self._is_decumulation = None
        self._metadata = None
        self._name = None
        self._parent_goal_id = None
        self._questionnaire_id = None
        self._secondary_id = None
        self._type = None
        self._update_date = None
        self.discriminator = None

        if accumulation_horizon is not None:
            self.accumulation_horizon = accumulation_horizon
        if category is not None:
            self.category = category
        if client_id is not None:
            self.client_id = client_id
        if create_date is not None:
            self.create_date = create_date
        if decumulation_horizon is not None:
            self.decumulation_horizon = decumulation_horizon
        if goal_amount is not None:
            self.goal_amount = goal_amount
        if id is not None:
            self.id = id
        if image is not None:
            self.image = image
        if is_active is not None:
            self.is_active = is_active
        if is_decumulation is not None:
            self.is_decumulation = is_decumulation
        if metadata is not None:
            self.metadata = metadata
        self.name = name
        if parent_goal_id is not None:
            self.parent_goal_id = parent_goal_id
        if questionnaire_id is not None:
            self.questionnaire_id = questionnaire_id
        if secondary_id is not None:
            self.secondary_id = secondary_id
        if type is not None:
            self.type = type
        if update_date is not None:
            self.update_date = update_date

    @property
    def accumulation_horizon(self):
        """Gets the accumulation_horizon of this Goal.  # noqa: E501


        :return: The accumulation_horizon of this Goal.  # noqa: E501
        :rtype: float
        """
        return self._accumulation_horizon

    @accumulation_horizon.setter
    def accumulation_horizon(self, accumulation_horizon):
        """Sets the accumulation_horizon of this Goal.


        :param accumulation_horizon: The accumulation_horizon of this Goal.  # noqa: E501
        :type: float
        """

        self._accumulation_horizon = accumulation_horizon

    @property
    def category(self):
        """Gets the category of this Goal.  # noqa: E501

        category  # noqa: E501

        :return: The category of this Goal.  # noqa: E501
        :rtype: str
        """
        return self._category

    @category.setter
    def category(self, category):
        """Sets the category of this Goal.

        category  # noqa: E501

        :param category: The category of this Goal.  # noqa: E501
        :type: str
        """

        self._category = category

    @property
    def client_id(self):
        """Gets the client_id of this Goal.  # noqa: E501


        :return: The client_id of this Goal.  # noqa: E501
        :rtype: str
        """
        return self._client_id

    @client_id.setter
    def client_id(self, client_id):
        """Sets the client_id of this Goal.


        :param client_id: The client_id of this Goal.  # noqa: E501
        :type: str
        """

        self._client_id = client_id

    @property
    def create_date(self):
        """Gets the create_date of this Goal.  # noqa: E501


        :return: The create_date of this Goal.  # noqa: E501
        :rtype: datetime
        """
        return self._create_date

    @create_date.setter
    def create_date(self, create_date):
        """Sets the create_date of this Goal.


        :param create_date: The create_date of this Goal.  # noqa: E501
        :type: datetime
        """

        self._create_date = create_date

    @property
    def decumulation_horizon(self):
        """Gets the decumulation_horizon of this Goal.  # noqa: E501


        :return: The decumulation_horizon of this Goal.  # noqa: E501
        :rtype: float
        """
        return self._decumulation_horizon

    @decumulation_horizon.setter
    def decumulation_horizon(self, decumulation_horizon):
        """Sets the decumulation_horizon of this Goal.


        :param decumulation_horizon: The decumulation_horizon of this Goal.  # noqa: E501
        :type: float
        """

        self._decumulation_horizon = decumulation_horizon

    @property
    def goal_amount(self):
        """Gets the goal_amount of this Goal.  # noqa: E501


        :return: The goal_amount of this Goal.  # noqa: E501
        :rtype: float
        """
        return self._goal_amount

    @goal_amount.setter
    def goal_amount(self, goal_amount):
        """Sets the goal_amount of this Goal.


        :param goal_amount: The goal_amount of this Goal.  # noqa: E501
        :type: float
        """

        self._goal_amount = goal_amount

    @property
    def id(self):
        """Gets the id of this Goal.  # noqa: E501


        :return: The id of this Goal.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Goal.


        :param id: The id of this Goal.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def image(self):
        """Gets the image of this Goal.  # noqa: E501

        image  # noqa: E501

        :return: The image of this Goal.  # noqa: E501
        :rtype: str
        """
        return self._image

    @image.setter
    def image(self, image):
        """Sets the image of this Goal.

        image  # noqa: E501

        :param image: The image of this Goal.  # noqa: E501
        :type: str
        """

        self._image = image

    @property
    def is_active(self):
        """Gets the is_active of this Goal.  # noqa: E501

        isActive  # noqa: E501

        :return: The is_active of this Goal.  # noqa: E501
        :rtype: bool
        """
        return self._is_active

    @is_active.setter
    def is_active(self, is_active):
        """Sets the is_active of this Goal.

        isActive  # noqa: E501

        :param is_active: The is_active of this Goal.  # noqa: E501
        :type: bool
        """

        self._is_active = is_active

    @property
    def is_decumulation(self):
        """Gets the is_decumulation of this Goal.  # noqa: E501

        isDecumulation  # noqa: E501

        :return: The is_decumulation of this Goal.  # noqa: E501
        :rtype: bool
        """
        return self._is_decumulation

    @is_decumulation.setter
    def is_decumulation(self, is_decumulation):
        """Sets the is_decumulation of this Goal.

        isDecumulation  # noqa: E501

        :param is_decumulation: The is_decumulation of this Goal.  # noqa: E501
        :type: bool
        """

        self._is_decumulation = is_decumulation

    @property
    def metadata(self):
        """Gets the metadata of this Goal.  # noqa: E501


        :return: The metadata of this Goal.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this Goal.


        :param metadata: The metadata of this Goal.  # noqa: E501
        :type: dict(str, str)
        """

        self._metadata = metadata

    @property
    def name(self):
        """Gets the name of this Goal.  # noqa: E501

        Goal name  # noqa: E501

        :return: The name of this Goal.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Goal.

        Goal name  # noqa: E501

        :param name: The name of this Goal.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def parent_goal_id(self):
        """Gets the parent_goal_id of this Goal.  # noqa: E501

        Goal Parent Goal Id  # noqa: E501

        :return: The parent_goal_id of this Goal.  # noqa: E501
        :rtype: str
        """
        return self._parent_goal_id

    @parent_goal_id.setter
    def parent_goal_id(self, parent_goal_id):
        """Sets the parent_goal_id of this Goal.

        Goal Parent Goal Id  # noqa: E501

        :param parent_goal_id: The parent_goal_id of this Goal.  # noqa: E501
        :type: str
        """

        self._parent_goal_id = parent_goal_id

    @property
    def questionnaire_id(self):
        """Gets the questionnaire_id of this Goal.  # noqa: E501

        questionnaire_id  # noqa: E501

        :return: The questionnaire_id of this Goal.  # noqa: E501
        :rtype: str
        """
        return self._questionnaire_id

    @questionnaire_id.setter
    def questionnaire_id(self, questionnaire_id):
        """Sets the questionnaire_id of this Goal.

        questionnaire_id  # noqa: E501

        :param questionnaire_id: The questionnaire_id of this Goal.  # noqa: E501
        :type: str
        """

        self._questionnaire_id = questionnaire_id

    @property
    def secondary_id(self):
        """Gets the secondary_id of this Goal.  # noqa: E501


        :return: The secondary_id of this Goal.  # noqa: E501
        :rtype: str
        """
        return self._secondary_id

    @secondary_id.setter
    def secondary_id(self, secondary_id):
        """Sets the secondary_id of this Goal.


        :param secondary_id: The secondary_id of this Goal.  # noqa: E501
        :type: str
        """

        self._secondary_id = secondary_id

    @property
    def type(self):
        """Gets the type of this Goal.  # noqa: E501

        type  # noqa: E501

        :return: The type of this Goal.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this Goal.

        type  # noqa: E501

        :param type: The type of this Goal.  # noqa: E501
        :type: str
        """

        self._type = type

    @property
    def update_date(self):
        """Gets the update_date of this Goal.  # noqa: E501


        :return: The update_date of this Goal.  # noqa: E501
        :rtype: datetime
        """
        return self._update_date

    @update_date.setter
    def update_date(self, update_date):
        """Sets the update_date of this Goal.


        :param update_date: The update_date of this Goal.  # noqa: E501
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
        if issubclass(Goal, dict):
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
        if not isinstance(other, Goal):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Goal):
            return True

        return self.to_dict() != other.to_dict()
