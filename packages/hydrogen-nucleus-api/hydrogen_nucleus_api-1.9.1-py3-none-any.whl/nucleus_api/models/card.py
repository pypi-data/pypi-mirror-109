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


class Card(object):
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
        'address': 'list[CardAddress]',
        'business_id': 'str',
        'card_holder_name': 'str',
        'card_image': 'str',
        'card_issuance': 'str',
        'card_name': 'str',
        'card_network': 'str',
        'card_program_id': 'str',
        'card_type': 'str',
        'client_id': 'str',
        'create_date': 'datetime',
        'credit_limit': 'float',
        'currency_code': 'str',
        'expiry_date': 'date',
        'fulfillment': 'str',
        'id': 'str',
        'institution_id': 'str',
        'institution_name': 'str',
        'is_active': 'bool',
        'is_pin_set': 'bool',
        'is_primary': 'bool',
        'is_reloadable': 'bool',
        'mask': 'str',
        'metadata': 'dict(str, str)',
        'phone_number': 'str',
        'portfolio_id': 'str',
        'prepaid_amount': 'float',
        'secondary_id': 'str',
        'status': 'str',
        'update_date': 'datetime'
    }

    attribute_map = {
        'address': 'address',
        'business_id': 'business_id',
        'card_holder_name': 'card_holder_name',
        'card_image': 'card_image',
        'card_issuance': 'card_issuance',
        'card_name': 'card_name',
        'card_network': 'card_network',
        'card_program_id': 'card_program_id',
        'card_type': 'card_type',
        'client_id': 'client_id',
        'create_date': 'create_date',
        'credit_limit': 'credit_limit',
        'currency_code': 'currency_code',
        'expiry_date': 'expiry_date',
        'fulfillment': 'fulfillment',
        'id': 'id',
        'institution_id': 'institution_id',
        'institution_name': 'institution_name',
        'is_active': 'is_active',
        'is_pin_set': 'is_pin_set',
        'is_primary': 'is_primary',
        'is_reloadable': 'is_reloadable',
        'mask': 'mask',
        'metadata': 'metadata',
        'phone_number': 'phone_number',
        'portfolio_id': 'portfolio_id',
        'prepaid_amount': 'prepaid_amount',
        'secondary_id': 'secondary_id',
        'status': 'status',
        'update_date': 'update_date'
    }

    def __init__(self, address=None, business_id=None, card_holder_name=None, card_image=None, card_issuance=None, card_name=None, card_network=None, card_program_id=None, card_type=None, client_id=None, create_date=None, credit_limit=None, currency_code=None, expiry_date=None, fulfillment=None, id=None, institution_id=None, institution_name=None, is_active=None, is_pin_set=None, is_primary=None, is_reloadable=None, mask=None, metadata=None, phone_number=None, portfolio_id=None, prepaid_amount=None, secondary_id=None, status=None, update_date=None, _configuration=None):  # noqa: E501
        """Card - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._address = None
        self._business_id = None
        self._card_holder_name = None
        self._card_image = None
        self._card_issuance = None
        self._card_name = None
        self._card_network = None
        self._card_program_id = None
        self._card_type = None
        self._client_id = None
        self._create_date = None
        self._credit_limit = None
        self._currency_code = None
        self._expiry_date = None
        self._fulfillment = None
        self._id = None
        self._institution_id = None
        self._institution_name = None
        self._is_active = None
        self._is_pin_set = None
        self._is_primary = None
        self._is_reloadable = None
        self._mask = None
        self._metadata = None
        self._phone_number = None
        self._portfolio_id = None
        self._prepaid_amount = None
        self._secondary_id = None
        self._status = None
        self._update_date = None
        self.discriminator = None

        if address is not None:
            self.address = address
        if business_id is not None:
            self.business_id = business_id
        self.card_holder_name = card_holder_name
        if card_image is not None:
            self.card_image = card_image
        self.card_issuance = card_issuance
        self.card_name = card_name
        if card_network is not None:
            self.card_network = card_network
        if card_program_id is not None:
            self.card_program_id = card_program_id
        self.card_type = card_type
        if client_id is not None:
            self.client_id = client_id
        if create_date is not None:
            self.create_date = create_date
        if credit_limit is not None:
            self.credit_limit = credit_limit
        if currency_code is not None:
            self.currency_code = currency_code
        if expiry_date is not None:
            self.expiry_date = expiry_date
        if fulfillment is not None:
            self.fulfillment = fulfillment
        if id is not None:
            self.id = id
        if institution_id is not None:
            self.institution_id = institution_id
        if institution_name is not None:
            self.institution_name = institution_name
        if is_active is not None:
            self.is_active = is_active
        if is_pin_set is not None:
            self.is_pin_set = is_pin_set
        if is_primary is not None:
            self.is_primary = is_primary
        if is_reloadable is not None:
            self.is_reloadable = is_reloadable
        if mask is not None:
            self.mask = mask
        if metadata is not None:
            self.metadata = metadata
        if phone_number is not None:
            self.phone_number = phone_number
        self.portfolio_id = portfolio_id
        if prepaid_amount is not None:
            self.prepaid_amount = prepaid_amount
        if secondary_id is not None:
            self.secondary_id = secondary_id
        if status is not None:
            self.status = status
        if update_date is not None:
            self.update_date = update_date

    @property
    def address(self):
        """Gets the address of this Card.  # noqa: E501


        :return: The address of this Card.  # noqa: E501
        :rtype: list[CardAddress]
        """
        return self._address

    @address.setter
    def address(self, address):
        """Sets the address of this Card.


        :param address: The address of this Card.  # noqa: E501
        :type: list[CardAddress]
        """

        self._address = address

    @property
    def business_id(self):
        """Gets the business_id of this Card.  # noqa: E501

        businessId  # noqa: E501

        :return: The business_id of this Card.  # noqa: E501
        :rtype: str
        """
        return self._business_id

    @business_id.setter
    def business_id(self, business_id):
        """Sets the business_id of this Card.

        businessId  # noqa: E501

        :param business_id: The business_id of this Card.  # noqa: E501
        :type: str
        """

        self._business_id = business_id

    @property
    def card_holder_name(self):
        """Gets the card_holder_name of this Card.  # noqa: E501

        cardHolderName  # noqa: E501

        :return: The card_holder_name of this Card.  # noqa: E501
        :rtype: str
        """
        return self._card_holder_name

    @card_holder_name.setter
    def card_holder_name(self, card_holder_name):
        """Sets the card_holder_name of this Card.

        cardHolderName  # noqa: E501

        :param card_holder_name: The card_holder_name of this Card.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and card_holder_name is None:
            raise ValueError("Invalid value for `card_holder_name`, must not be `None`")  # noqa: E501

        self._card_holder_name = card_holder_name

    @property
    def card_image(self):
        """Gets the card_image of this Card.  # noqa: E501

        card_image  # noqa: E501

        :return: The card_image of this Card.  # noqa: E501
        :rtype: str
        """
        return self._card_image

    @card_image.setter
    def card_image(self, card_image):
        """Sets the card_image of this Card.

        card_image  # noqa: E501

        :param card_image: The card_image of this Card.  # noqa: E501
        :type: str
        """

        self._card_image = card_image

    @property
    def card_issuance(self):
        """Gets the card_issuance of this Card.  # noqa: E501

        cardIssuance  # noqa: E501

        :return: The card_issuance of this Card.  # noqa: E501
        :rtype: str
        """
        return self._card_issuance

    @card_issuance.setter
    def card_issuance(self, card_issuance):
        """Sets the card_issuance of this Card.

        cardIssuance  # noqa: E501

        :param card_issuance: The card_issuance of this Card.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and card_issuance is None:
            raise ValueError("Invalid value for `card_issuance`, must not be `None`")  # noqa: E501

        self._card_issuance = card_issuance

    @property
    def card_name(self):
        """Gets the card_name of this Card.  # noqa: E501

        cardName  # noqa: E501

        :return: The card_name of this Card.  # noqa: E501
        :rtype: str
        """
        return self._card_name

    @card_name.setter
    def card_name(self, card_name):
        """Sets the card_name of this Card.

        cardName  # noqa: E501

        :param card_name: The card_name of this Card.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and card_name is None:
            raise ValueError("Invalid value for `card_name`, must not be `None`")  # noqa: E501

        self._card_name = card_name

    @property
    def card_network(self):
        """Gets the card_network of this Card.  # noqa: E501

        cardNetwork  # noqa: E501

        :return: The card_network of this Card.  # noqa: E501
        :rtype: str
        """
        return self._card_network

    @card_network.setter
    def card_network(self, card_network):
        """Sets the card_network of this Card.

        cardNetwork  # noqa: E501

        :param card_network: The card_network of this Card.  # noqa: E501
        :type: str
        """

        self._card_network = card_network

    @property
    def card_program_id(self):
        """Gets the card_program_id of this Card.  # noqa: E501

        cardProgramId  # noqa: E501

        :return: The card_program_id of this Card.  # noqa: E501
        :rtype: str
        """
        return self._card_program_id

    @card_program_id.setter
    def card_program_id(self, card_program_id):
        """Sets the card_program_id of this Card.

        cardProgramId  # noqa: E501

        :param card_program_id: The card_program_id of this Card.  # noqa: E501
        :type: str
        """

        self._card_program_id = card_program_id

    @property
    def card_type(self):
        """Gets the card_type of this Card.  # noqa: E501

        cardType  # noqa: E501

        :return: The card_type of this Card.  # noqa: E501
        :rtype: str
        """
        return self._card_type

    @card_type.setter
    def card_type(self, card_type):
        """Sets the card_type of this Card.

        cardType  # noqa: E501

        :param card_type: The card_type of this Card.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and card_type is None:
            raise ValueError("Invalid value for `card_type`, must not be `None`")  # noqa: E501

        self._card_type = card_type

    @property
    def client_id(self):
        """Gets the client_id of this Card.  # noqa: E501

        clientId  # noqa: E501

        :return: The client_id of this Card.  # noqa: E501
        :rtype: str
        """
        return self._client_id

    @client_id.setter
    def client_id(self, client_id):
        """Sets the client_id of this Card.

        clientId  # noqa: E501

        :param client_id: The client_id of this Card.  # noqa: E501
        :type: str
        """

        self._client_id = client_id

    @property
    def create_date(self):
        """Gets the create_date of this Card.  # noqa: E501


        :return: The create_date of this Card.  # noqa: E501
        :rtype: datetime
        """
        return self._create_date

    @create_date.setter
    def create_date(self, create_date):
        """Sets the create_date of this Card.


        :param create_date: The create_date of this Card.  # noqa: E501
        :type: datetime
        """

        self._create_date = create_date

    @property
    def credit_limit(self):
        """Gets the credit_limit of this Card.  # noqa: E501

        creditLimit  # noqa: E501

        :return: The credit_limit of this Card.  # noqa: E501
        :rtype: float
        """
        return self._credit_limit

    @credit_limit.setter
    def credit_limit(self, credit_limit):
        """Sets the credit_limit of this Card.

        creditLimit  # noqa: E501

        :param credit_limit: The credit_limit of this Card.  # noqa: E501
        :type: float
        """

        self._credit_limit = credit_limit

    @property
    def currency_code(self):
        """Gets the currency_code of this Card.  # noqa: E501

        currencyCode  # noqa: E501

        :return: The currency_code of this Card.  # noqa: E501
        :rtype: str
        """
        return self._currency_code

    @currency_code.setter
    def currency_code(self, currency_code):
        """Sets the currency_code of this Card.

        currencyCode  # noqa: E501

        :param currency_code: The currency_code of this Card.  # noqa: E501
        :type: str
        """

        self._currency_code = currency_code

    @property
    def expiry_date(self):
        """Gets the expiry_date of this Card.  # noqa: E501

        expiryDate  # noqa: E501

        :return: The expiry_date of this Card.  # noqa: E501
        :rtype: date
        """
        return self._expiry_date

    @expiry_date.setter
    def expiry_date(self, expiry_date):
        """Sets the expiry_date of this Card.

        expiryDate  # noqa: E501

        :param expiry_date: The expiry_date of this Card.  # noqa: E501
        :type: date
        """

        self._expiry_date = expiry_date

    @property
    def fulfillment(self):
        """Gets the fulfillment of this Card.  # noqa: E501

        fulfillment  # noqa: E501

        :return: The fulfillment of this Card.  # noqa: E501
        :rtype: str
        """
        return self._fulfillment

    @fulfillment.setter
    def fulfillment(self, fulfillment):
        """Sets the fulfillment of this Card.

        fulfillment  # noqa: E501

        :param fulfillment: The fulfillment of this Card.  # noqa: E501
        :type: str
        """

        self._fulfillment = fulfillment

    @property
    def id(self):
        """Gets the id of this Card.  # noqa: E501


        :return: The id of this Card.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Card.


        :param id: The id of this Card.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def institution_id(self):
        """Gets the institution_id of this Card.  # noqa: E501

        institutionId  # noqa: E501

        :return: The institution_id of this Card.  # noqa: E501
        :rtype: str
        """
        return self._institution_id

    @institution_id.setter
    def institution_id(self, institution_id):
        """Sets the institution_id of this Card.

        institutionId  # noqa: E501

        :param institution_id: The institution_id of this Card.  # noqa: E501
        :type: str
        """

        self._institution_id = institution_id

    @property
    def institution_name(self):
        """Gets the institution_name of this Card.  # noqa: E501

        institutionName  # noqa: E501

        :return: The institution_name of this Card.  # noqa: E501
        :rtype: str
        """
        return self._institution_name

    @institution_name.setter
    def institution_name(self, institution_name):
        """Sets the institution_name of this Card.

        institutionName  # noqa: E501

        :param institution_name: The institution_name of this Card.  # noqa: E501
        :type: str
        """

        self._institution_name = institution_name

    @property
    def is_active(self):
        """Gets the is_active of this Card.  # noqa: E501

        is_active  # noqa: E501

        :return: The is_active of this Card.  # noqa: E501
        :rtype: bool
        """
        return self._is_active

    @is_active.setter
    def is_active(self, is_active):
        """Sets the is_active of this Card.

        is_active  # noqa: E501

        :param is_active: The is_active of this Card.  # noqa: E501
        :type: bool
        """

        self._is_active = is_active

    @property
    def is_pin_set(self):
        """Gets the is_pin_set of this Card.  # noqa: E501

        is_pin_set  # noqa: E501

        :return: The is_pin_set of this Card.  # noqa: E501
        :rtype: bool
        """
        return self._is_pin_set

    @is_pin_set.setter
    def is_pin_set(self, is_pin_set):
        """Sets the is_pin_set of this Card.

        is_pin_set  # noqa: E501

        :param is_pin_set: The is_pin_set of this Card.  # noqa: E501
        :type: bool
        """

        self._is_pin_set = is_pin_set

    @property
    def is_primary(self):
        """Gets the is_primary of this Card.  # noqa: E501

        is_primary  # noqa: E501

        :return: The is_primary of this Card.  # noqa: E501
        :rtype: bool
        """
        return self._is_primary

    @is_primary.setter
    def is_primary(self, is_primary):
        """Sets the is_primary of this Card.

        is_primary  # noqa: E501

        :param is_primary: The is_primary of this Card.  # noqa: E501
        :type: bool
        """

        self._is_primary = is_primary

    @property
    def is_reloadable(self):
        """Gets the is_reloadable of this Card.  # noqa: E501

        is_reloadable  # noqa: E501

        :return: The is_reloadable of this Card.  # noqa: E501
        :rtype: bool
        """
        return self._is_reloadable

    @is_reloadable.setter
    def is_reloadable(self, is_reloadable):
        """Sets the is_reloadable of this Card.

        is_reloadable  # noqa: E501

        :param is_reloadable: The is_reloadable of this Card.  # noqa: E501
        :type: bool
        """

        self._is_reloadable = is_reloadable

    @property
    def mask(self):
        """Gets the mask of this Card.  # noqa: E501

        mask  # noqa: E501

        :return: The mask of this Card.  # noqa: E501
        :rtype: str
        """
        return self._mask

    @mask.setter
    def mask(self, mask):
        """Sets the mask of this Card.

        mask  # noqa: E501

        :param mask: The mask of this Card.  # noqa: E501
        :type: str
        """

        self._mask = mask

    @property
    def metadata(self):
        """Gets the metadata of this Card.  # noqa: E501


        :return: The metadata of this Card.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this Card.


        :param metadata: The metadata of this Card.  # noqa: E501
        :type: dict(str, str)
        """

        self._metadata = metadata

    @property
    def phone_number(self):
        """Gets the phone_number of this Card.  # noqa: E501

        phoneNumber  # noqa: E501

        :return: The phone_number of this Card.  # noqa: E501
        :rtype: str
        """
        return self._phone_number

    @phone_number.setter
    def phone_number(self, phone_number):
        """Sets the phone_number of this Card.

        phoneNumber  # noqa: E501

        :param phone_number: The phone_number of this Card.  # noqa: E501
        :type: str
        """

        self._phone_number = phone_number

    @property
    def portfolio_id(self):
        """Gets the portfolio_id of this Card.  # noqa: E501

        portfolioId  # noqa: E501

        :return: The portfolio_id of this Card.  # noqa: E501
        :rtype: str
        """
        return self._portfolio_id

    @portfolio_id.setter
    def portfolio_id(self, portfolio_id):
        """Sets the portfolio_id of this Card.

        portfolioId  # noqa: E501

        :param portfolio_id: The portfolio_id of this Card.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and portfolio_id is None:
            raise ValueError("Invalid value for `portfolio_id`, must not be `None`")  # noqa: E501

        self._portfolio_id = portfolio_id

    @property
    def prepaid_amount(self):
        """Gets the prepaid_amount of this Card.  # noqa: E501

        prepaidAmount  # noqa: E501

        :return: The prepaid_amount of this Card.  # noqa: E501
        :rtype: float
        """
        return self._prepaid_amount

    @prepaid_amount.setter
    def prepaid_amount(self, prepaid_amount):
        """Sets the prepaid_amount of this Card.

        prepaidAmount  # noqa: E501

        :param prepaid_amount: The prepaid_amount of this Card.  # noqa: E501
        :type: float
        """

        self._prepaid_amount = prepaid_amount

    @property
    def secondary_id(self):
        """Gets the secondary_id of this Card.  # noqa: E501


        :return: The secondary_id of this Card.  # noqa: E501
        :rtype: str
        """
        return self._secondary_id

    @secondary_id.setter
    def secondary_id(self, secondary_id):
        """Sets the secondary_id of this Card.


        :param secondary_id: The secondary_id of this Card.  # noqa: E501
        :type: str
        """

        self._secondary_id = secondary_id

    @property
    def status(self):
        """Gets the status of this Card.  # noqa: E501

        status  # noqa: E501

        :return: The status of this Card.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this Card.

        status  # noqa: E501

        :param status: The status of this Card.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def update_date(self):
        """Gets the update_date of this Card.  # noqa: E501


        :return: The update_date of this Card.  # noqa: E501
        :rtype: datetime
        """
        return self._update_date

    @update_date.setter
    def update_date(self, update_date):
        """Sets the update_date of this Card.


        :param update_date: The update_date of this Card.  # noqa: E501
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
        if issubclass(Card, dict):
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
        if not isinstance(other, Card):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Card):
            return True

        return self.to_dict() != other.to_dict()
