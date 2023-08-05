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


class V1alpha1GeneDatasetRequest(object):
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
        'accessions': 'list[str]',
        'fasta_filter': 'list[str]',
        'gene_ids': 'list[int]',
        'include_annotation_type': 'list[V1alpha1Fasta]',
        'limit': 'str',
        'returned_content': 'V1alpha1GeneDatasetRequestContentType',
        'sort_schema': 'GeneDatasetRequestSort',
        'symbols_for_taxon': 'GeneDatasetRequestSymbolsForTaxon',
        'taxon': 'str'
    }

    attribute_map = {
        'accessions': 'accessions',
        'fasta_filter': 'fasta_filter',
        'gene_ids': 'gene_ids',
        'include_annotation_type': 'include_annotation_type',
        'limit': 'limit',
        'returned_content': 'returned_content',
        'sort_schema': 'sort_schema',
        'symbols_for_taxon': 'symbols_for_taxon',
        'taxon': 'taxon'
    }

    def __init__(self, accessions=None, fasta_filter=None, gene_ids=None, include_annotation_type=None, limit=None, returned_content=None, sort_schema=None, symbols_for_taxon=None, taxon=None, local_vars_configuration=None):  # noqa: E501
        """V1alpha1GeneDatasetRequest - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._accessions = None
        self._fasta_filter = None
        self._gene_ids = None
        self._include_annotation_type = None
        self._limit = None
        self._returned_content = None
        self._sort_schema = None
        self._symbols_for_taxon = None
        self._taxon = None
        self.discriminator = None

        if accessions is not None:
            self.accessions = accessions
        if fasta_filter is not None:
            self.fasta_filter = fasta_filter
        if gene_ids is not None:
            self.gene_ids = gene_ids
        if include_annotation_type is not None:
            self.include_annotation_type = include_annotation_type
        if limit is not None:
            self.limit = limit
        if returned_content is not None:
            self.returned_content = returned_content
        if sort_schema is not None:
            self.sort_schema = sort_schema
        if symbols_for_taxon is not None:
            self.symbols_for_taxon = symbols_for_taxon
        if taxon is not None:
            self.taxon = taxon

    @property
    def accessions(self):
        """Gets the accessions of this V1alpha1GeneDatasetRequest.  # noqa: E501

        RNA or Protein accessions.  # noqa: E501

        :return: The accessions of this V1alpha1GeneDatasetRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._accessions

    @accessions.setter
    def accessions(self, accessions):
        """Sets the accessions of this V1alpha1GeneDatasetRequest.

        RNA or Protein accessions.  # noqa: E501

        :param accessions: The accessions of this V1alpha1GeneDatasetRequest.  # noqa: E501
        :type: list[str]
        """

        self._accessions = accessions

    @property
    def fasta_filter(self):
        """Gets the fasta_filter of this V1alpha1GeneDatasetRequest.  # noqa: E501


        :return: The fasta_filter of this V1alpha1GeneDatasetRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._fasta_filter

    @fasta_filter.setter
    def fasta_filter(self, fasta_filter):
        """Sets the fasta_filter of this V1alpha1GeneDatasetRequest.


        :param fasta_filter: The fasta_filter of this V1alpha1GeneDatasetRequest.  # noqa: E501
        :type: list[str]
        """

        self._fasta_filter = fasta_filter

    @property
    def gene_ids(self):
        """Gets the gene_ids of this V1alpha1GeneDatasetRequest.  # noqa: E501


        :return: The gene_ids of this V1alpha1GeneDatasetRequest.  # noqa: E501
        :rtype: list[int]
        """
        return self._gene_ids

    @gene_ids.setter
    def gene_ids(self, gene_ids):
        """Sets the gene_ids of this V1alpha1GeneDatasetRequest.


        :param gene_ids: The gene_ids of this V1alpha1GeneDatasetRequest.  # noqa: E501
        :type: list[int]
        """

        self._gene_ids = gene_ids

    @property
    def include_annotation_type(self):
        """Gets the include_annotation_type of this V1alpha1GeneDatasetRequest.  # noqa: E501

        Select additional types of annotation to include in the data package.  If unset, no annotation is provided.  # noqa: E501

        :return: The include_annotation_type of this V1alpha1GeneDatasetRequest.  # noqa: E501
        :rtype: list[V1alpha1Fasta]
        """
        return self._include_annotation_type

    @include_annotation_type.setter
    def include_annotation_type(self, include_annotation_type):
        """Sets the include_annotation_type of this V1alpha1GeneDatasetRequest.

        Select additional types of annotation to include in the data package.  If unset, no annotation is provided.  # noqa: E501

        :param include_annotation_type: The include_annotation_type of this V1alpha1GeneDatasetRequest.  # noqa: E501
        :type: list[V1alpha1Fasta]
        """

        self._include_annotation_type = include_annotation_type

    @property
    def limit(self):
        """Gets the limit of this V1alpha1GeneDatasetRequest.  # noqa: E501


        :return: The limit of this V1alpha1GeneDatasetRequest.  # noqa: E501
        :rtype: str
        """
        return self._limit

    @limit.setter
    def limit(self, limit):
        """Sets the limit of this V1alpha1GeneDatasetRequest.


        :param limit: The limit of this V1alpha1GeneDatasetRequest.  # noqa: E501
        :type: str
        """

        self._limit = limit

    @property
    def returned_content(self):
        """Gets the returned_content of this V1alpha1GeneDatasetRequest.  # noqa: E501


        :return: The returned_content of this V1alpha1GeneDatasetRequest.  # noqa: E501
        :rtype: V1alpha1GeneDatasetRequestContentType
        """
        return self._returned_content

    @returned_content.setter
    def returned_content(self, returned_content):
        """Sets the returned_content of this V1alpha1GeneDatasetRequest.


        :param returned_content: The returned_content of this V1alpha1GeneDatasetRequest.  # noqa: E501
        :type: V1alpha1GeneDatasetRequestContentType
        """

        self._returned_content = returned_content

    @property
    def sort_schema(self):
        """Gets the sort_schema of this V1alpha1GeneDatasetRequest.  # noqa: E501


        :return: The sort_schema of this V1alpha1GeneDatasetRequest.  # noqa: E501
        :rtype: GeneDatasetRequestSort
        """
        return self._sort_schema

    @sort_schema.setter
    def sort_schema(self, sort_schema):
        """Sets the sort_schema of this V1alpha1GeneDatasetRequest.


        :param sort_schema: The sort_schema of this V1alpha1GeneDatasetRequest.  # noqa: E501
        :type: GeneDatasetRequestSort
        """

        self._sort_schema = sort_schema

    @property
    def symbols_for_taxon(self):
        """Gets the symbols_for_taxon of this V1alpha1GeneDatasetRequest.  # noqa: E501


        :return: The symbols_for_taxon of this V1alpha1GeneDatasetRequest.  # noqa: E501
        :rtype: GeneDatasetRequestSymbolsForTaxon
        """
        return self._symbols_for_taxon

    @symbols_for_taxon.setter
    def symbols_for_taxon(self, symbols_for_taxon):
        """Sets the symbols_for_taxon of this V1alpha1GeneDatasetRequest.


        :param symbols_for_taxon: The symbols_for_taxon of this V1alpha1GeneDatasetRequest.  # noqa: E501
        :type: GeneDatasetRequestSymbolsForTaxon
        """

        self._symbols_for_taxon = symbols_for_taxon

    @property
    def taxon(self):
        """Gets the taxon of this V1alpha1GeneDatasetRequest.  # noqa: E501


        :return: The taxon of this V1alpha1GeneDatasetRequest.  # noqa: E501
        :rtype: str
        """
        return self._taxon

    @taxon.setter
    def taxon(self, taxon):
        """Sets the taxon of this V1alpha1GeneDatasetRequest.


        :param taxon: The taxon of this V1alpha1GeneDatasetRequest.  # noqa: E501
        :type: str
        """

        self._taxon = taxon

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
        if not isinstance(other, V1alpha1GeneDatasetRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1alpha1GeneDatasetRequest):
            return True

        return self.to_dict() != other.to_dict()
