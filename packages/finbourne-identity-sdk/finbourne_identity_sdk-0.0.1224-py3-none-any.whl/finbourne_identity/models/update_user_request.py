# coding: utf-8

"""
    FINBOURNE Identity Service API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 0.0.1224
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

class UpdateUserRequest(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
      required_map (dict): The key is attribute name
                           and the value is whether it is 'required' or 'optional'.
    """
    openapi_types = {
        'first_name': 'str',
        'last_name': 'str',
        'email_address': 'str',
        'login': 'str',
        'roles': 'list[RoleId]'
    }

    attribute_map = {
        'first_name': 'firstName',
        'last_name': 'lastName',
        'email_address': 'emailAddress',
        'login': 'login',
        'roles': 'roles'
    }

    required_map = {
        'first_name': 'required',
        'last_name': 'required',
        'email_address': 'required',
        'login': 'required',
        'roles': 'optional'
    }

    def __init__(self, first_name=None, last_name=None, email_address=None, login=None, roles=None):  # noqa: E501
        """
        UpdateUserRequest - a model defined in OpenAPI

        :param first_name:  (required)
        :type first_name: str
        :param last_name:  (required)
        :type last_name: str
        :param email_address:  (required)
        :type email_address: str
        :param login:  The user's login username, in the form of an email address, which must be unique within the system.  For user accounts this should exactly match the user's email address. (required)
        :type login: str
        :param roles: 
        :type roles: list[finbourne_identity.RoleId]

        """  # noqa: E501

        self._first_name = None
        self._last_name = None
        self._email_address = None
        self._login = None
        self._roles = None
        self.discriminator = None

        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
        self.login = login
        self.roles = roles

    @property
    def first_name(self):
        """Gets the first_name of this UpdateUserRequest.  # noqa: E501


        :return: The first_name of this UpdateUserRequest.  # noqa: E501
        :rtype: str
        """
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        """Sets the first_name of this UpdateUserRequest.


        :param first_name: The first_name of this UpdateUserRequest.  # noqa: E501
        :type: str
        """
        if first_name is None:
            raise ValueError("Invalid value for `first_name`, must not be `None`")  # noqa: E501
        if first_name is not None and len(first_name) > 50:
            raise ValueError("Invalid value for `first_name`, length must be less than or equal to `50`")  # noqa: E501
        if first_name is not None and len(first_name) < 1:
            raise ValueError("Invalid value for `first_name`, length must be greater than or equal to `1`")  # noqa: E501
        if (first_name is not None and not re.search(r'^[\s\S]*$', first_name)):  # noqa: E501
            raise ValueError(r"Invalid value for `first_name`, must be a follow pattern or equal to `/^[\s\S]*$/`")  # noqa: E501

        self._first_name = first_name

    @property
    def last_name(self):
        """Gets the last_name of this UpdateUserRequest.  # noqa: E501


        :return: The last_name of this UpdateUserRequest.  # noqa: E501
        :rtype: str
        """
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        """Sets the last_name of this UpdateUserRequest.


        :param last_name: The last_name of this UpdateUserRequest.  # noqa: E501
        :type: str
        """
        if last_name is None:
            raise ValueError("Invalid value for `last_name`, must not be `None`")  # noqa: E501
        if last_name is not None and len(last_name) > 50:
            raise ValueError("Invalid value for `last_name`, length must be less than or equal to `50`")  # noqa: E501
        if last_name is not None and len(last_name) < 2:
            raise ValueError("Invalid value for `last_name`, length must be greater than or equal to `2`")  # noqa: E501
        if (last_name is not None and not re.search(r'^[\s\S]*$', last_name)):  # noqa: E501
            raise ValueError(r"Invalid value for `last_name`, must be a follow pattern or equal to `/^[\s\S]*$/`")  # noqa: E501

        self._last_name = last_name

    @property
    def email_address(self):
        """Gets the email_address of this UpdateUserRequest.  # noqa: E501


        :return: The email_address of this UpdateUserRequest.  # noqa: E501
        :rtype: str
        """
        return self._email_address

    @email_address.setter
    def email_address(self, email_address):
        """Sets the email_address of this UpdateUserRequest.


        :param email_address: The email_address of this UpdateUserRequest.  # noqa: E501
        :type: str
        """
        if email_address is None:
            raise ValueError("Invalid value for `email_address`, must not be `None`")  # noqa: E501
        if email_address is not None and len(email_address) > 80:
            raise ValueError("Invalid value for `email_address`, length must be less than or equal to `80`")  # noqa: E501
        if email_address is not None and len(email_address) < 5:
            raise ValueError("Invalid value for `email_address`, length must be greater than or equal to `5`")  # noqa: E501

        self._email_address = email_address

    @property
    def login(self):
        """Gets the login of this UpdateUserRequest.  # noqa: E501

        The user's login username, in the form of an email address, which must be unique within the system.  For user accounts this should exactly match the user's email address.  # noqa: E501

        :return: The login of this UpdateUserRequest.  # noqa: E501
        :rtype: str
        """
        return self._login

    @login.setter
    def login(self, login):
        """Sets the login of this UpdateUserRequest.

        The user's login username, in the form of an email address, which must be unique within the system.  For user accounts this should exactly match the user's email address.  # noqa: E501

        :param login: The login of this UpdateUserRequest.  # noqa: E501
        :type: str
        """
        if login is None:
            raise ValueError("Invalid value for `login`, must not be `None`")  # noqa: E501
        if login is not None and len(login) > 80:
            raise ValueError("Invalid value for `login`, length must be less than or equal to `80`")  # noqa: E501
        if login is not None and len(login) < 5:
            raise ValueError("Invalid value for `login`, length must be greater than or equal to `5`")  # noqa: E501
        if (login is not None and not re.search(r'^[\s\S]*$', login)):  # noqa: E501
            raise ValueError(r"Invalid value for `login`, must be a follow pattern or equal to `/^[\s\S]*$/`")  # noqa: E501

        self._login = login

    @property
    def roles(self):
        """Gets the roles of this UpdateUserRequest.  # noqa: E501


        :return: The roles of this UpdateUserRequest.  # noqa: E501
        :rtype: list[RoleId]
        """
        return self._roles

    @roles.setter
    def roles(self, roles):
        """Sets the roles of this UpdateUserRequest.


        :param roles: The roles of this UpdateUserRequest.  # noqa: E501
        :type: list[RoleId]
        """

        self._roles = roles

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
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

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, UpdateUserRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
