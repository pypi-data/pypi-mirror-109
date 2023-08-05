# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/notification/plugin/protocol.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='spaceone/api/notification/plugin/protocol.proto',
  package='spaceone.api.notification.plugin',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n/spaceone/api/notification/plugin/protocol.proto\x12 spaceone.api.notification.plugin\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1cgoogle/protobuf/struct.proto\"7\n\x0bInitRequest\x12(\n\x07options\x18\x01 \x01(\x0b\x32\x17.google.protobuf.Struct\"m\n\x13PluginVerifyRequest\x12(\n\x07options\x18\x01 \x01(\x0b\x32\x17.google.protobuf.Struct\x12,\n\x0bsecret_data\x18\x02 \x01(\x0b\x32\x17.google.protobuf.Struct\"7\n\nPluginInfo\x12)\n\x08metadata\x18\x01 \x01(\x0b\x32\x17.google.protobuf.Struct2\xcc\x01\n\x08Protocol\x12\x65\n\x04init\x12-.spaceone.api.notification.plugin.InitRequest\x1a,.spaceone.api.notification.plugin.PluginInfo\"\x00\x12Y\n\x06verify\x12\x35.spaceone.api.notification.plugin.PluginVerifyRequest\x1a\x16.google.protobuf.Empty\"\x00\x62\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_empty__pb2.DESCRIPTOR,google_dot_protobuf_dot_struct__pb2.DESCRIPTOR,])




_INITREQUEST = _descriptor.Descriptor(
  name='InitRequest',
  full_name='spaceone.api.notification.plugin.InitRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='options', full_name='spaceone.api.notification.plugin.InitRequest.options', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=144,
  serialized_end=199,
)


_PLUGINVERIFYREQUEST = _descriptor.Descriptor(
  name='PluginVerifyRequest',
  full_name='spaceone.api.notification.plugin.PluginVerifyRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='options', full_name='spaceone.api.notification.plugin.PluginVerifyRequest.options', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='secret_data', full_name='spaceone.api.notification.plugin.PluginVerifyRequest.secret_data', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=201,
  serialized_end=310,
)


_PLUGININFO = _descriptor.Descriptor(
  name='PluginInfo',
  full_name='spaceone.api.notification.plugin.PluginInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='metadata', full_name='spaceone.api.notification.plugin.PluginInfo.metadata', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=312,
  serialized_end=367,
)

_INITREQUEST.fields_by_name['options'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_PLUGINVERIFYREQUEST.fields_by_name['options'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_PLUGINVERIFYREQUEST.fields_by_name['secret_data'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_PLUGININFO.fields_by_name['metadata'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
DESCRIPTOR.message_types_by_name['InitRequest'] = _INITREQUEST
DESCRIPTOR.message_types_by_name['PluginVerifyRequest'] = _PLUGINVERIFYREQUEST
DESCRIPTOR.message_types_by_name['PluginInfo'] = _PLUGININFO
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

InitRequest = _reflection.GeneratedProtocolMessageType('InitRequest', (_message.Message,), {
  'DESCRIPTOR' : _INITREQUEST,
  '__module__' : 'spaceone.api.notification.plugin.protocol_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.notification.plugin.InitRequest)
  })
_sym_db.RegisterMessage(InitRequest)

PluginVerifyRequest = _reflection.GeneratedProtocolMessageType('PluginVerifyRequest', (_message.Message,), {
  'DESCRIPTOR' : _PLUGINVERIFYREQUEST,
  '__module__' : 'spaceone.api.notification.plugin.protocol_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.notification.plugin.PluginVerifyRequest)
  })
_sym_db.RegisterMessage(PluginVerifyRequest)

PluginInfo = _reflection.GeneratedProtocolMessageType('PluginInfo', (_message.Message,), {
  'DESCRIPTOR' : _PLUGININFO,
  '__module__' : 'spaceone.api.notification.plugin.protocol_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.notification.plugin.PluginInfo)
  })
_sym_db.RegisterMessage(PluginInfo)



_PROTOCOL = _descriptor.ServiceDescriptor(
  name='Protocol',
  full_name='spaceone.api.notification.plugin.Protocol',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=370,
  serialized_end=574,
  methods=[
  _descriptor.MethodDescriptor(
    name='init',
    full_name='spaceone.api.notification.plugin.Protocol.init',
    index=0,
    containing_service=None,
    input_type=_INITREQUEST,
    output_type=_PLUGININFO,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='verify',
    full_name='spaceone.api.notification.plugin.Protocol.verify',
    index=1,
    containing_service=None,
    input_type=_PLUGINVERIFYREQUEST,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_PROTOCOL)

DESCRIPTOR.services_by_name['Protocol'] = _PROTOCOL

# @@protoc_insertion_point(module_scope)
