# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tensorflow_hub/module_def.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='tensorflow_hub/module_def.proto',
  package='tensorflow_hub',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x1ftensorflow_hub/module_def.proto\x12\x0etensorflow_hub\"\x89\x01\n\tModuleDef\x12\x30\n\x06\x66ormat\x18\x01 \x01(\x0e\x32 .tensorflow_hub.ModuleDef.Format\x12\x19\n\x11required_features\x18\x02 \x03(\t\"/\n\x06\x46ormat\x12\x16\n\x12\x46ORMAT_UNSPECIFIED\x10\x00\x12\r\n\tFORMAT_V3\x10\x03\x62\x06proto3')
)



_MODULEDEF_FORMAT = _descriptor.EnumDescriptor(
  name='Format',
  full_name='tensorflow_hub.ModuleDef.Format',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='FORMAT_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FORMAT_V3', index=1, number=3,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=142,
  serialized_end=189,
)
_sym_db.RegisterEnumDescriptor(_MODULEDEF_FORMAT)


_MODULEDEF = _descriptor.Descriptor(
  name='ModuleDef',
  full_name='tensorflow_hub.ModuleDef',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='format', full_name='tensorflow_hub.ModuleDef.format', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='required_features', full_name='tensorflow_hub.ModuleDef.required_features', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _MODULEDEF_FORMAT,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=52,
  serialized_end=189,
)

_MODULEDEF.fields_by_name['format'].enum_type = _MODULEDEF_FORMAT
_MODULEDEF_FORMAT.containing_type = _MODULEDEF
DESCRIPTOR.message_types_by_name['ModuleDef'] = _MODULEDEF
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ModuleDef = _reflection.GeneratedProtocolMessageType('ModuleDef', (_message.Message,), dict(
  DESCRIPTOR = _MODULEDEF,
  __module__ = 'tensorflow_hub.module_def_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow_hub.ModuleDef)
  ))
_sym_db.RegisterMessage(ModuleDef)


# @@protoc_insertion_point(module_scope)
