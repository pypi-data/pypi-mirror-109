# coding: utf-8

"""
    NCBI Datasets API

    NCBI service to query and download biological sequence data across all domains of life from NCBI databases.  # noqa: E501

    The version of the OpenAPI document: v1alpha
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from ncbi.datasets.openapi.configuration import Configuration


class V1alpha1AssemblyDatasetDescriptorsFilter(object):
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
    """
    openapi_types = {
        'assembly_level': 'list[AssemblyDatasetDescriptorsFilterAssemblyLevel]',
        'assembly_source': 'AssemblyDatasetDescriptorsFilterAssemblySource',
        'first_release_date': 'datetime',
        'has_annotation': 'bool',
        'last_release_date': 'datetime',
        'reference_only': 'bool',
        'refseq_only': 'bool',
        'search_text': 'list[str]'
    }

    attribute_map = {
        'assembly_level': 'assembly_level',
        'assembly_source': 'assembly_source',
        'first_release_date': 'first_release_date',
        'has_annotation': 'has_annotation',
        'last_release_date': 'last_release_date',
        'reference_only': 'reference_only',
        'refseq_only': 'refseq_only',
        'search_text': 'search_text'
    }

    def __init__(self, assembly_level=None, assembly_source=None, first_release_date=None, has_annotation=None, last_release_date=None, reference_only=None, refseq_only=None, search_text=None, local_vars_configuration=None):  # noqa: E501
        """V1alpha1AssemblyDatasetDescriptorsFilter - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._assembly_level = None
        self._assembly_source = None
        self._first_release_date = None
        self._has_annotation = None
        self._last_release_date = None
        self._reference_only = None
        self._refseq_only = None
        self._search_text = None
        self.discriminator = None

        if assembly_level is not None:
            self.assembly_level = assembly_level
        if assembly_source is not None:
            self.assembly_source = assembly_source
        if first_release_date is not None:
            self.first_release_date = first_release_date
        if has_annotation is not None:
            self.has_annotation = has_annotation
        if last_release_date is not None:
            self.last_release_date = last_release_date
        if reference_only is not None:
            self.reference_only = reference_only
        if refseq_only is not None:
            self.refseq_only = refseq_only
        if search_text is not None:
            self.search_text = search_text

    @property
    def assembly_level(self):
        """Gets the assembly_level of this V1alpha1AssemblyDatasetDescriptorsFilter.  # noqa: E501


        :return: The assembly_level of this V1alpha1AssemblyDatasetDescriptorsFilter.  # noqa: E501
        :rtype: list[AssemblyDatasetDescriptorsFilterAssemblyLevel]
        """
        return self._assembly_level

    @assembly_level.setter
    def assembly_level(self, assembly_level):
        """Sets the assembly_level of this V1alpha1AssemblyDatasetDescriptorsFilter.


        :param assembly_level: The assembly_level of this V1alpha1AssemblyDatasetDescriptorsFilter.  # noqa: E501
        :type: list[AssemblyDatasetDescriptorsFilterAssemblyLevel]
        """

        self._assembly_level = assembly_level

    @property
    def assembly_source(self):
        """Gets the assembly_source of this V1alpha1AssemblyDatasetDescriptorsFilter.  # noqa: E501


        :return: The assembly_source of this V1alpha1AssemblyDatasetDescriptorsFilter.  # noqa: E501
        :rtype: AssemblyDatasetDescriptorsFilterAssemblySource
        """
        return self._assembly_source

    @assembly_source.setter
    def assembly_source(self, assembly_source):
        """Sets the assembly_source of this V1alpha1AssemblyDatasetDescriptorsFilter.


        :param assembly_source: The assembly_source of this V1alpha1AssemblyDatasetDescriptorsFilter.  # noqa: E501
        :type: AssemblyDatasetDescriptorsFilterAssemblySource
        """

        self._assembly_source = assembly_source

    @property
    def first_release_date(self):
        """Gets the first_release_date of this V1alpha1AssemblyDatasetDescriptorsFilter.  # noqa: E501


        :return: The first_release_date of this V1alpha1AssemblyDatasetDescriptorsFilter.  # noqa: E501
        :rtype: datetime
        """
        return self._first_release_date

    @first_release_date.setter
    def first_release_date(self, first_release_date):
        """Sets the first_release_date of this V1alpha1AssemblyDatasetDescriptorsFilter.


        :param first_release_date: The first_release_date of this V1alpha1AssemblyDatasetDescriptorsFilter.  # noqa: E501
        :type: datetime
        """

        self._first_release_date = first_release_date

    @property
    def has_annotation(self):
        """Gets the has_annotation of this V1alpha1AssemblyDatasetDescriptorsFilter.  # noqa: E501


        :return: The has_annotation of this V1alpha1AssemblyDatasetDescriptorsFilter.  # noqa: E501
        :rtype: bool
        """
        return self._has_annotation

    @has_annotation.setter
    def has_annotation(self, has_annotation):
        """Sets the has_annotation of this V1alpha1AssemblyDatasetDescriptorsFilter.


        :param has_annotation: The has_annotation of this V1alpha1AssemblyDatasetDescriptorsFilter.  # noqa: E501
        :type: bool
        """

        self._has_annotation = has_annotation

    @property
    def last_release_date(self):
        """Gets the last_release_date of this V1alpha1AssemblyDatasetDescriptorsFilter.  # noqa: E501


        :return: The last_release_date of this V1alpha1AssemblyDatasetDescriptorsFilter.  # noqa: E501
        :rtype: datetime
        """
        return self._last_release_date

    @last_release_date.setter
    def last_release_date(self, last_release_date):
        """Sets the last_release_date of this V1alpha1AssemblyDatasetDescriptorsFilter.


        :param last_release_date: The last_release_date of this V1alpha1AssemblyDatasetDescriptorsFilter.  # noqa: E501
        :type: datetime
        """

        self._last_release_date = last_release_date

    @property
    def reference_only(self):
        """Gets the reference_only of this V1alpha1AssemblyDatasetDescriptorsFilter.  # noqa: E501

        If true, only return reference and representative (GCF_ and GCA_) genome assemblies.  # noqa: E501

        :return: The reference_only of this V1alpha1AssemblyDatasetDescriptorsFilter.  # noqa: E501
        :rtype: bool
        """
        return self._reference_only

    @reference_only.setter
    def reference_only(self, reference_only):
        """Sets the reference_only of this V1alpha1AssemblyDatasetDescriptorsFilter.

        If true, only return reference and representative (GCF_ and GCA_) genome assemblies.  # noqa: E501

        :param reference_only: The reference_only of this V1alpha1AssemblyDatasetDescriptorsFilter.  # noqa: E501
        :type: bool
        """

        self._reference_only = reference_only

    @property
    def refseq_only(self):
        """Gets the refseq_only of this V1alpha1AssemblyDatasetDescriptorsFilter.  # noqa: E501

        If true, only return RefSeq (GCF_) genome assemblies. Deprecated - use assembly_type instead.  # noqa: E501

        :return: The refseq_only of this V1alpha1AssemblyDatasetDescriptorsFilter.  # noqa: E501
        :rtype: bool
        """
        return self._refseq_only

    @refseq_only.setter
    def refseq_only(self, refseq_only):
        """Sets the refseq_only of this V1alpha1AssemblyDatasetDescriptorsFilter.

        If true, only return RefSeq (GCF_) genome assemblies. Deprecated - use assembly_type instead.  # noqa: E501

        :param refseq_only: The refseq_only of this V1alpha1AssemblyDatasetDescriptorsFilter.  # noqa: E501
        :type: bool
        """

        self._refseq_only = refseq_only

    @property
    def search_text(self):
        """Gets the search_text of this V1alpha1AssemblyDatasetDescriptorsFilter.  # noqa: E501


        :return: The search_text of this V1alpha1AssemblyDatasetDescriptorsFilter.  # noqa: E501
        :rtype: list[str]
        """
        return self._search_text

    @search_text.setter
    def search_text(self, search_text):
        """Sets the search_text of this V1alpha1AssemblyDatasetDescriptorsFilter.


        :param search_text: The search_text of this V1alpha1AssemblyDatasetDescriptorsFilter.  # noqa: E501
        :type: list[str]
        """

        self._search_text = search_text

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
        if not isinstance(other, V1alpha1AssemblyDatasetDescriptorsFilter):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1alpha1AssemblyDatasetDescriptorsFilter):
            return True

        return self.to_dict() != other.to_dict()
