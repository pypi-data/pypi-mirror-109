# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/billing/plugin/billing.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='spaceone/api/billing/plugin/billing.proto',
  package='spaceone.api.billing.plugin',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n)spaceone/api/billing/plugin/billing.proto\x12\x1bspaceone.api.billing.plugin\x1a\x1cgoogle/protobuf/struct.proto\"\xeb\x01\n\x12\x42illingDataRequest\x12(\n\x07options\x18\x01 \x01(\x0b\x32\x17.google.protobuf.Struct\x12,\n\x0bsecret_data\x18\x02 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\'\n\x06\x66ilter\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x13\n\x0b\x61ggregation\x18\x04 \x03(\t\x12\r\n\x05start\x18\x05 \x01(\t\x12\x0b\n\x03\x65nd\x18\x06 \x01(\t\x12\x13\n\x0bgranularity\x18\x07 \x01(\t\x12\x0e\n\x06schema\x18\t \x01(\t\";\n\x0b\x42illingData\x12\x0c\n\x04\x64\x61te\x18\x01 \x01(\t\x12\x0c\n\x04\x63ost\x18\x02 \x01(\x01\x12\x10\n\x08\x63urrency\x18\x03 \x01(\t\"r\n\x0b\x42illingInfo\x12\x15\n\rresource_type\x18\x01 \x01(\t\x12>\n\x0c\x62illing_data\x18\x02 \x03(\x0b\x32(.spaceone.api.billing.plugin.BillingData\x12\x0c\n\x04name\x18\x03 \x01(\t\"k\n\x19PluginBillingDataResponse\x12\x39\n\x07results\x18\x01 \x03(\x0b\x32(.spaceone.api.billing.plugin.BillingInfo\x12\x13\n\x0btotal_count\x18\x02 \x01(\x05\x32\x80\x01\n\x07\x42illing\x12u\n\x08get_data\x12/.spaceone.api.billing.plugin.BillingDataRequest\x1a\x36.spaceone.api.billing.plugin.PluginBillingDataResponse\"\x00\x62\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_struct__pb2.DESCRIPTOR,])




_BILLINGDATAREQUEST = _descriptor.Descriptor(
  name='BillingDataRequest',
  full_name='spaceone.api.billing.plugin.BillingDataRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='options', full_name='spaceone.api.billing.plugin.BillingDataRequest.options', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='secret_data', full_name='spaceone.api.billing.plugin.BillingDataRequest.secret_data', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='filter', full_name='spaceone.api.billing.plugin.BillingDataRequest.filter', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='aggregation', full_name='spaceone.api.billing.plugin.BillingDataRequest.aggregation', index=3,
      number=4, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='start', full_name='spaceone.api.billing.plugin.BillingDataRequest.start', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='end', full_name='spaceone.api.billing.plugin.BillingDataRequest.end', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='granularity', full_name='spaceone.api.billing.plugin.BillingDataRequest.granularity', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='schema', full_name='spaceone.api.billing.plugin.BillingDataRequest.schema', index=7,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=105,
  serialized_end=340,
)


_BILLINGDATA = _descriptor.Descriptor(
  name='BillingData',
  full_name='spaceone.api.billing.plugin.BillingData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='date', full_name='spaceone.api.billing.plugin.BillingData.date', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cost', full_name='spaceone.api.billing.plugin.BillingData.cost', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='currency', full_name='spaceone.api.billing.plugin.BillingData.currency', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=342,
  serialized_end=401,
)


_BILLINGINFO = _descriptor.Descriptor(
  name='BillingInfo',
  full_name='spaceone.api.billing.plugin.BillingInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_type', full_name='spaceone.api.billing.plugin.BillingInfo.resource_type', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='billing_data', full_name='spaceone.api.billing.plugin.BillingInfo.billing_data', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='spaceone.api.billing.plugin.BillingInfo.name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=403,
  serialized_end=517,
)


_PLUGINBILLINGDATARESPONSE = _descriptor.Descriptor(
  name='PluginBillingDataResponse',
  full_name='spaceone.api.billing.plugin.PluginBillingDataResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='results', full_name='spaceone.api.billing.plugin.PluginBillingDataResponse.results', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='total_count', full_name='spaceone.api.billing.plugin.PluginBillingDataResponse.total_count', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=519,
  serialized_end=626,
)

_BILLINGDATAREQUEST.fields_by_name['options'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_BILLINGDATAREQUEST.fields_by_name['secret_data'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_BILLINGDATAREQUEST.fields_by_name['filter'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_BILLINGINFO.fields_by_name['billing_data'].message_type = _BILLINGDATA
_PLUGINBILLINGDATARESPONSE.fields_by_name['results'].message_type = _BILLINGINFO
DESCRIPTOR.message_types_by_name['BillingDataRequest'] = _BILLINGDATAREQUEST
DESCRIPTOR.message_types_by_name['BillingData'] = _BILLINGDATA
DESCRIPTOR.message_types_by_name['BillingInfo'] = _BILLINGINFO
DESCRIPTOR.message_types_by_name['PluginBillingDataResponse'] = _PLUGINBILLINGDATARESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

BillingDataRequest = _reflection.GeneratedProtocolMessageType('BillingDataRequest', (_message.Message,), {
  'DESCRIPTOR' : _BILLINGDATAREQUEST,
  '__module__' : 'spaceone.api.billing.plugin.billing_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.billing.plugin.BillingDataRequest)
  })
_sym_db.RegisterMessage(BillingDataRequest)

BillingData = _reflection.GeneratedProtocolMessageType('BillingData', (_message.Message,), {
  'DESCRIPTOR' : _BILLINGDATA,
  '__module__' : 'spaceone.api.billing.plugin.billing_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.billing.plugin.BillingData)
  })
_sym_db.RegisterMessage(BillingData)

BillingInfo = _reflection.GeneratedProtocolMessageType('BillingInfo', (_message.Message,), {
  'DESCRIPTOR' : _BILLINGINFO,
  '__module__' : 'spaceone.api.billing.plugin.billing_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.billing.plugin.BillingInfo)
  })
_sym_db.RegisterMessage(BillingInfo)

PluginBillingDataResponse = _reflection.GeneratedProtocolMessageType('PluginBillingDataResponse', (_message.Message,), {
  'DESCRIPTOR' : _PLUGINBILLINGDATARESPONSE,
  '__module__' : 'spaceone.api.billing.plugin.billing_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.billing.plugin.PluginBillingDataResponse)
  })
_sym_db.RegisterMessage(PluginBillingDataResponse)



_BILLING = _descriptor.ServiceDescriptor(
  name='Billing',
  full_name='spaceone.api.billing.plugin.Billing',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=629,
  serialized_end=757,
  methods=[
  _descriptor.MethodDescriptor(
    name='get_data',
    full_name='spaceone.api.billing.plugin.Billing.get_data',
    index=0,
    containing_service=None,
    input_type=_BILLINGDATAREQUEST,
    output_type=_PLUGINBILLINGDATARESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_BILLING)

DESCRIPTOR.services_by_name['Billing'] = _BILLING

# @@protoc_insertion_point(module_scope)
