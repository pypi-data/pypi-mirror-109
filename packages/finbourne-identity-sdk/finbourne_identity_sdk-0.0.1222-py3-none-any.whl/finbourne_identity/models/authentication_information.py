# coding: utf-8

"""
    FINBOURNE Identity Service API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 0.0.1222
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

class AuthenticationInformation(object):
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
        'issuer_url': 'str',
        'saml_identity_provider_id': 'str',
        'support': 'SupportAccessExpiry',
        'links': 'list[Link]'
    }

    attribute_map = {
        'issuer_url': 'issuerUrl',
        'saml_identity_provider_id': 'samlIdentityProviderId',
        'support': 'support',
        'links': 'links'
    }

    required_map = {
        'issuer_url': 'required',
        'saml_identity_provider_id': 'optional',
        'support': 'optional',
        'links': 'optional'
    }

    def __init__(self, issuer_url=None, saml_identity_provider_id=None, support=None, links=None):  # noqa: E501
        """
        AuthenticationInformation - a model defined in OpenAPI

        :param issuer_url:  (required)
        :type issuer_url: str
        :param saml_identity_provider_id: 
        :type saml_identity_provider_id: str
        :param support: 
        :type support: finbourne_identity.SupportAccessExpiry
        :param links: 
        :type links: list[finbourne_identity.Link]

        """  # noqa: E501

        self._issuer_url = None
        self._saml_identity_provider_id = None
        self._support = None
        self._links = None
        self.discriminator = None

        self.issuer_url = issuer_url
        self.saml_identity_provider_id = saml_identity_provider_id
        if support is not None:
            self.support = support
        self.links = links

    @property
    def issuer_url(self):
        """Gets the issuer_url of this AuthenticationInformation.  # noqa: E501


        :return: The issuer_url of this AuthenticationInformation.  # noqa: E501
        :rtype: str
        """
        return self._issuer_url

    @issuer_url.setter
    def issuer_url(self, issuer_url):
        """Sets the issuer_url of this AuthenticationInformation.


        :param issuer_url: The issuer_url of this AuthenticationInformation.  # noqa: E501
        :type: str
        """
        if issuer_url is None:
            raise ValueError("Invalid value for `issuer_url`, must not be `None`")  # noqa: E501

        self._issuer_url = issuer_url

    @property
    def saml_identity_provider_id(self):
        """Gets the saml_identity_provider_id of this AuthenticationInformation.  # noqa: E501


        :return: The saml_identity_provider_id of this AuthenticationInformation.  # noqa: E501
        :rtype: str
        """
        return self._saml_identity_provider_id

    @saml_identity_provider_id.setter
    def saml_identity_provider_id(self, saml_identity_provider_id):
        """Sets the saml_identity_provider_id of this AuthenticationInformation.


        :param saml_identity_provider_id: The saml_identity_provider_id of this AuthenticationInformation.  # noqa: E501
        :type: str
        """

        self._saml_identity_provider_id = saml_identity_provider_id

    @property
    def support(self):
        """Gets the support of this AuthenticationInformation.  # noqa: E501


        :return: The support of this AuthenticationInformation.  # noqa: E501
        :rtype: SupportAccessExpiry
        """
        return self._support

    @support.setter
    def support(self, support):
        """Sets the support of this AuthenticationInformation.


        :param support: The support of this AuthenticationInformation.  # noqa: E501
        :type: SupportAccessExpiry
        """

        self._support = support

    @property
    def links(self):
        """Gets the links of this AuthenticationInformation.  # noqa: E501


        :return: The links of this AuthenticationInformation.  # noqa: E501
        :rtype: list[Link]
        """
        return self._links

    @links.setter
    def links(self, links):
        """Sets the links of this AuthenticationInformation.


        :param links: The links of this AuthenticationInformation.  # noqa: E501
        :type: list[Link]
        """

        self._links = links

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
        if not isinstance(other, AuthenticationInformation):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
