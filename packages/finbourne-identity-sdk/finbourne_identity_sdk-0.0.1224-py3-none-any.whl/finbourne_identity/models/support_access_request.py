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

class SupportAccessRequest(object):
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
        'duration': 'str',
        'description': 'str'
    }

    attribute_map = {
        'duration': 'duration',
        'description': 'description'
    }

    required_map = {
        'duration': 'required',
        'description': 'optional'
    }

    def __init__(self, duration=None, description=None):  # noqa: E501
        """
        SupportAccessRequest - a model defined in OpenAPI

        :param duration:  The duration for which access is requested (in any ISO-8601 format) (required)
        :type duration: str
        :param description:  The description of why the support access has been granted (i.e. support ticket numbers)
        :type description: str

        """  # noqa: E501

        self._duration = None
        self._description = None
        self.discriminator = None

        self.duration = duration
        self.description = description

    @property
    def duration(self):
        """Gets the duration of this SupportAccessRequest.  # noqa: E501

        The duration for which access is requested (in any ISO-8601 format)  # noqa: E501

        :return: The duration of this SupportAccessRequest.  # noqa: E501
        :rtype: str
        """
        return self._duration

    @duration.setter
    def duration(self, duration):
        """Sets the duration of this SupportAccessRequest.

        The duration for which access is requested (in any ISO-8601 format)  # noqa: E501

        :param duration: The duration of this SupportAccessRequest.  # noqa: E501
        :type: str
        """
        if duration is None:
            raise ValueError("Invalid value for `duration`, must not be `None`")  # noqa: E501
        if duration is not None and len(duration) > 30:
            raise ValueError("Invalid value for `duration`, length must be less than or equal to `30`")  # noqa: E501
        if duration is not None and len(duration) < 2:
            raise ValueError("Invalid value for `duration`, length must be greater than or equal to `2`")  # noqa: E501
        if (duration is not None and not re.search(r'^P(?!$)((\d+Y)|(\d+\.\d+Y$))?((\d+M)|(\d+\.\d+M$))?((\d+W)|(\d+\.\d+W$))?((\d+D)|(\d+\.\d+D$))?(T(?=\d)((\d+H)|(\d+\.\d+H$))?((\d+M)|(\d+\.\d+M$))?(\d+(\.\d+)?S)?)??$', duration)):  # noqa: E501
            raise ValueError(r"Invalid value for `duration`, must be a follow pattern or equal to `/^P(?!$)((\d+Y)|(\d+\.\d+Y$))?((\d+M)|(\d+\.\d+M$))?((\d+W)|(\d+\.\d+W$))?((\d+D)|(\d+\.\d+D$))?(T(?=\d)((\d+H)|(\d+\.\d+H$))?((\d+M)|(\d+\.\d+M$))?(\d+(\.\d+)?S)?)??$/`")  # noqa: E501

        self._duration = duration

    @property
    def description(self):
        """Gets the description of this SupportAccessRequest.  # noqa: E501

        The description of why the support access has been granted (i.e. support ticket numbers)  # noqa: E501

        :return: The description of this SupportAccessRequest.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this SupportAccessRequest.

        The description of why the support access has been granted (i.e. support ticket numbers)  # noqa: E501

        :param description: The description of this SupportAccessRequest.  # noqa: E501
        :type: str
        """
        if description is not None and len(description) > 1024:
            raise ValueError("Invalid value for `description`, length must be less than or equal to `1024`")  # noqa: E501
        if description is not None and len(description) < 0:
            raise ValueError("Invalid value for `description`, length must be greater than or equal to `0`")  # noqa: E501
        if (description is not None and not re.search(r'^[\s\S]*$', description)):  # noqa: E501
            raise ValueError(r"Invalid value for `description`, must be a follow pattern or equal to `/^[\s\S]*$/`")  # noqa: E501

        self._description = description

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
        if not isinstance(other, SupportAccessRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
