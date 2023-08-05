# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ncbi/datasets/v1alpha1/request_options.proto

from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import descriptor_pb2 as google_dot_protobuf_dot_descriptor__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='ncbi/datasets/v1alpha1/request_options.proto',
  package='ncbi.datasets.v1alpha1',
  syntax='proto3',
  serialized_options=b'Z\026ncbi/datasets/v1alpha1\370\001\001',
  serialized_pb=b'\n,ncbi/datasets/v1alpha1/request_options.proto\x12\x16ncbi.datasets.v1alpha1\x1a google/protobuf/descriptor.proto\"Z\n\x13RequestFieldOptions\x12\x43\n\x0b\x66ilter_type\x18\x01 \x01(\x0e\x32\".ncbi.datasets.v1alpha1.FilterTypeR\nfilterType*f\n\nFilterType\x12\x1b\n\x17\x46ILTER_TYPE_UNSPECIFIED\x10\x00\x12\x1e\n\x1a\x46ILTER_TYPE_CONTENT_FILTER\x10\x01\x12\x1b\n\x17\x46ILTER_TYPE_FILE_FILTER\x10\x02:y\n\x11request_qualifier\x12\x1d.google.protobuf.FieldOptions\x18\x8b\x9e\x03 \x01(\x0b\x32+.ncbi.datasets.v1alpha1.RequestFieldOptionsR\x10requestQualifierB\x1bZ\x16ncbi/datasets/v1alpha1\xf8\x01\x01\x62\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_descriptor__pb2.DESCRIPTOR,])

_FILTERTYPE = _descriptor.EnumDescriptor(
  name='FilterType',
  full_name='ncbi.datasets.v1alpha1.FilterType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='FILTER_TYPE_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FILTER_TYPE_CONTENT_FILTER', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FILTER_TYPE_FILE_FILTER', index=2, number=2,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=198,
  serialized_end=300,
)
_sym_db.RegisterEnumDescriptor(_FILTERTYPE)

FilterType = enum_type_wrapper.EnumTypeWrapper(_FILTERTYPE)
FILTER_TYPE_UNSPECIFIED = 0
FILTER_TYPE_CONTENT_FILTER = 1
FILTER_TYPE_FILE_FILTER = 2

REQUEST_QUALIFIER_FIELD_NUMBER = 53003
request_qualifier = _descriptor.FieldDescriptor(
  name='request_qualifier', full_name='ncbi.datasets.v1alpha1.request_qualifier', index=0,
  number=53003, type=11, cpp_type=10, label=1,
  has_default_value=False, default_value=None,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  serialized_options=None, json_name='requestQualifier', file=DESCRIPTOR)


_REQUESTFIELDOPTIONS = _descriptor.Descriptor(
  name='RequestFieldOptions',
  full_name='ncbi.datasets.v1alpha1.RequestFieldOptions',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='filter_type', full_name='ncbi.datasets.v1alpha1.RequestFieldOptions.filter_type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='filterType', file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=106,
  serialized_end=196,
)

_REQUESTFIELDOPTIONS.fields_by_name['filter_type'].enum_type = _FILTERTYPE
DESCRIPTOR.message_types_by_name['RequestFieldOptions'] = _REQUESTFIELDOPTIONS
DESCRIPTOR.enum_types_by_name['FilterType'] = _FILTERTYPE
DESCRIPTOR.extensions_by_name['request_qualifier'] = request_qualifier
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

RequestFieldOptions = _reflection.GeneratedProtocolMessageType('RequestFieldOptions', (_message.Message,), {
  'DESCRIPTOR' : _REQUESTFIELDOPTIONS,
  '__module__' : 'ncbi.datasets.v1alpha1.request_options_pb2'
  # @@protoc_insertion_point(class_scope:ncbi.datasets.v1alpha1.RequestFieldOptions)
  })
_sym_db.RegisterMessage(RequestFieldOptions)

request_qualifier.message_type = _REQUESTFIELDOPTIONS
google_dot_protobuf_dot_descriptor__pb2.FieldOptions.RegisterExtension(request_qualifier)

DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
