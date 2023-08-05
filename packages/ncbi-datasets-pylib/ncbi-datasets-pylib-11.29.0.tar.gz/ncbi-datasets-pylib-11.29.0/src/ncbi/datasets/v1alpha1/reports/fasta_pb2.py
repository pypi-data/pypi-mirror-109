# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ncbi/datasets/v1alpha1/reports/fasta.proto

from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='ncbi/datasets/v1alpha1/reports/fasta.proto',
  package='ncbi.datasets.v1alpha1.reports',
  syntax='proto3',
  serialized_options=b'Z\036ncbi/datasets/v1alpha1/reports\370\001\001',
  serialized_pb=b'\n*ncbi/datasets/v1alpha1/reports/fasta.proto\x12\x1encbi.datasets.v1alpha1.reports*\xb1\x01\n\x0f\x46\x61staFieldNames\x12\x0c\n\x08ORGANISM\x10\x00\x12\x11\n\rELEMENT_RANGE\x10\x01\x12\x10\n\x0c\x45LEMENT_NAME\x10\x02\x12\x12\n\x0e\x45LEMENT_SYMBOL\x10\x03\x12\n\n\x06\x43ONTIG\x10\x04\x12\x08\n\x04GENE\x10\x05\x12\x15\n\x11PROTEIN_ACCESSION\x10\x06\x12\x0e\n\nCHROMOSOME\x10\x07\x12\x08\n\x04NAME\x10\x08\x12\x10\n\x0c\x43OMPLETENESS\x10\tB#Z\x1encbi/datasets/v1alpha1/reports\xf8\x01\x01\x62\x06proto3'
)

_FASTAFIELDNAMES = _descriptor.EnumDescriptor(
  name='FastaFieldNames',
  full_name='ncbi.datasets.v1alpha1.reports.FastaFieldNames',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='ORGANISM', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ELEMENT_RANGE', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ELEMENT_NAME', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ELEMENT_SYMBOL', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CONTIG', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GENE', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PROTEIN_ACCESSION', index=6, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHROMOSOME', index=7, number=7,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NAME', index=8, number=8,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='COMPLETENESS', index=9, number=9,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=79,
  serialized_end=256,
)
_sym_db.RegisterEnumDescriptor(_FASTAFIELDNAMES)

FastaFieldNames = enum_type_wrapper.EnumTypeWrapper(_FASTAFIELDNAMES)
ORGANISM = 0
ELEMENT_RANGE = 1
ELEMENT_NAME = 2
ELEMENT_SYMBOL = 3
CONTIG = 4
GENE = 5
PROTEIN_ACCESSION = 6
CHROMOSOME = 7
NAME = 8
COMPLETENESS = 9


DESCRIPTOR.enum_types_by_name['FastaFieldNames'] = _FASTAFIELDNAMES
_sym_db.RegisterFileDescriptor(DESCRIPTOR)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
