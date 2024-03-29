# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: face-status.proto

import sys

_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()

DESCRIPTOR = _descriptor.FileDescriptor(
    name='face-status.proto',
    package='ndn_message',
    syntax='proto2',
    serialized_pb=_b(
        '\n\x11\x66\x61\x63\x65-status.proto\x12\x0bndn_message\"\x88\x04\n\x11\x46\x61\x63\x65StatusMessage\x12?\n\x0b\x66\x61\x63\x65_status\x18\x80\x01 \x03(\x0b\x32).ndn_message.FaceStatusMessage.FaceStatus\x1a\xb1\x03\n\nFaceStatus\x12\x0f\n\x07\x66\x61\x63\x65_id\x18i \x01(\x04\x12\x0b\n\x03uri\x18r \x01(\t\x12\x12\n\tlocal_uri\x18\x81\x01 \x01(\t\x12\x19\n\x11\x65xpiration_period\x18m \x01(\x04\x12\x13\n\nface_scope\x18\x84\x01 \x01(\x04\x12\x19\n\x10\x66\x61\x63\x65_persistency\x18\x85\x01 \x01(\x04\x12\x12\n\tlink_type\x18\x86\x01 \x01(\x04\x12)\n base_congestion_marking_interval\x18\x87\x01 \x01(\x04\x12%\n\x1c\x64\x65\x66\x61ult_congestion_threshold\x18\x88\x01 \x01(\x04\x12\x0c\n\x03mtu\x18\x89\x01 \x01(\x04\x12\x17\n\x0en_in_interests\x18\x90\x01 \x01(\x04\x12\x13\n\nn_in_datas\x18\x91\x01 \x01(\x04\x12\x13\n\nn_in_nacks\x18\x97\x01 \x01(\x04\x12\x18\n\x0fn_out_interests\x18\x92\x01 \x01(\x04\x12\x14\n\x0bn_out_datas\x18\x93\x01 \x01(\x04\x12\x14\n\x0bn_out_nacks\x18\x98\x01 \x01(\x04\x12\x13\n\nn_in_bytes\x18\x94\x01 \x01(\x04\x12\x14\n\x0bn_out_bytes\x18\x95\x01 \x01(\x04')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

_FACESTATUSMESSAGE_FACESTATUS = _descriptor.Descriptor(
    name='FaceStatus',
    full_name='ndn_message.FaceStatusMessage.FaceStatus',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='face_id', full_name='ndn_message.FaceStatusMessage.FaceStatus.face_id', index=0,
            number=105, type=4, cpp_type=4, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None),
        _descriptor.FieldDescriptor(
            name='uri', full_name='ndn_message.FaceStatusMessage.FaceStatus.uri', index=1,
            number=114, type=9, cpp_type=9, label=1,
            has_default_value=False, default_value=_b("").decode('utf-8'),
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None),
        _descriptor.FieldDescriptor(
            name='local_uri', full_name='ndn_message.FaceStatusMessage.FaceStatus.local_uri', index=2,
            number=129, type=9, cpp_type=9, label=1,
            has_default_value=False, default_value=_b("").decode('utf-8'),
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None),
        _descriptor.FieldDescriptor(
            name='expiration_period', full_name='ndn_message.FaceStatusMessage.FaceStatus.expiration_period', index=3,
            number=109, type=4, cpp_type=4, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None),
        _descriptor.FieldDescriptor(
            name='face_scope', full_name='ndn_message.FaceStatusMessage.FaceStatus.face_scope', index=4,
            number=132, type=4, cpp_type=4, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None),
        _descriptor.FieldDescriptor(
            name='face_persistency', full_name='ndn_message.FaceStatusMessage.FaceStatus.face_persistency', index=5,
            number=133, type=4, cpp_type=4, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None),
        _descriptor.FieldDescriptor(
            name='link_type', full_name='ndn_message.FaceStatusMessage.FaceStatus.link_type', index=6,
            number=134, type=4, cpp_type=4, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None),
        _descriptor.FieldDescriptor(
            name='base_congestion_marking_interval',
            full_name='ndn_message.FaceStatusMessage.FaceStatus.base_congestion_marking_interval', index=7,
            number=135, type=4, cpp_type=4, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None),
        _descriptor.FieldDescriptor(
            name='default_congestion_threshold',
            full_name='ndn_message.FaceStatusMessage.FaceStatus.default_congestion_threshold', index=8,
            number=136, type=4, cpp_type=4, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None),
        _descriptor.FieldDescriptor(
            name='mtu', full_name='ndn_message.FaceStatusMessage.FaceStatus.mtu', index=9,
            number=137, type=4, cpp_type=4, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None),
        _descriptor.FieldDescriptor(
            name='n_in_interests', full_name='ndn_message.FaceStatusMessage.FaceStatus.n_in_interests', index=10,
            number=144, type=4, cpp_type=4, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None),
        _descriptor.FieldDescriptor(
            name='n_in_datas', full_name='ndn_message.FaceStatusMessage.FaceStatus.n_in_datas', index=11,
            number=145, type=4, cpp_type=4, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None),
        _descriptor.FieldDescriptor(
            name='n_in_nacks', full_name='ndn_message.FaceStatusMessage.FaceStatus.n_in_nacks', index=12,
            number=151, type=4, cpp_type=4, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None),
        _descriptor.FieldDescriptor(
            name='n_out_interests', full_name='ndn_message.FaceStatusMessage.FaceStatus.n_out_interests', index=13,
            number=146, type=4, cpp_type=4, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None),
        _descriptor.FieldDescriptor(
            name='n_out_datas', full_name='ndn_message.FaceStatusMessage.FaceStatus.n_out_datas', index=14,
            number=147, type=4, cpp_type=4, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None),
        _descriptor.FieldDescriptor(
            name='n_out_nacks', full_name='ndn_message.FaceStatusMessage.FaceStatus.n_out_nacks', index=15,
            number=152, type=4, cpp_type=4, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None),
        _descriptor.FieldDescriptor(
            name='n_in_bytes', full_name='ndn_message.FaceStatusMessage.FaceStatus.n_in_bytes', index=16,
            number=148, type=4, cpp_type=4, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None),
        _descriptor.FieldDescriptor(
            name='n_out_bytes', full_name='ndn_message.FaceStatusMessage.FaceStatus.n_out_bytes', index=17,
            number=149, type=4, cpp_type=4, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None),
    ],
    extensions=[
    ],
    nested_types=[],
    enum_types=[
    ],
    options=None,
    is_extendable=False,
    syntax='proto2',
    extension_ranges=[],
    oneofs=[
    ],
    serialized_start=122,
    serialized_end=555,
)

_FACESTATUSMESSAGE = _descriptor.Descriptor(
    name='FaceStatusMessage',
    full_name='ndn_message.FaceStatusMessage',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='face_status', full_name='ndn_message.FaceStatusMessage.face_status', index=0,
            number=128, type=11, cpp_type=10, label=3,
            has_default_value=False, default_value=[],
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None),
    ],
    extensions=[
    ],
    nested_types=[_FACESTATUSMESSAGE_FACESTATUS, ],
    enum_types=[
    ],
    options=None,
    is_extendable=False,
    syntax='proto2',
    extension_ranges=[],
    oneofs=[
    ],
    serialized_start=35,
    serialized_end=555,
)

_FACESTATUSMESSAGE_FACESTATUS.containing_type = _FACESTATUSMESSAGE
_FACESTATUSMESSAGE.fields_by_name['face_status'].message_type = _FACESTATUSMESSAGE_FACESTATUS
DESCRIPTOR.message_types_by_name['FaceStatusMessage'] = _FACESTATUSMESSAGE

FaceStatusMessage = _reflection.GeneratedProtocolMessageType('FaceStatusMessage', (_message.Message,), dict(

    FaceStatus=_reflection.GeneratedProtocolMessageType('FaceStatus', (_message.Message,), dict(
        DESCRIPTOR=_FACESTATUSMESSAGE_FACESTATUS,
        __module__='face_status_pb2'
        # @@protoc_insertion_point(class_scope:ndn_message.FaceStatusMessage.FaceStatus)
    ))
    ,
    DESCRIPTOR=_FACESTATUSMESSAGE,
    __module__='face_status_pb2'
    # @@protoc_insertion_point(class_scope:ndn_message.FaceStatusMessage)
))
_sym_db.RegisterMessage(FaceStatusMessage)
_sym_db.RegisterMessage(FaceStatusMessage.FaceStatus)

# @@protoc_insertion_point(module_scope)
