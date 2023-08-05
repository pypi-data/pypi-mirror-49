# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: routing.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from .scalapb import scalapb_pb2 as scalapb_dot_scalapb__pb2
from . import CasperMessage_pb2 as CasperMessage__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='routing.proto',
  package='coop.rchain.comm.protocol.routing',
  syntax='proto3',
  serialized_options=_b('\342?%\n!coop.rchain.comm.protocol.routing\020\001'),
  serialized_pb=_b('\n\rrouting.proto\x12!coop.rchain.comm.protocol.routing\x1a\x15scalapb/scalapb.proto\x1a\x13\x43\x61sperMessage.proto\"D\n\x04Node\x12\n\n\x02id\x18\x01 \x01(\x0c\x12\x0c\n\x04host\x18\x02 \x01(\x0c\x12\x10\n\x08tcp_port\x18\x03 \x01(\r\x12\x10\n\x08udp_port\x18\x04 \x01(\r\"T\n\x06Header\x12\x37\n\x06sender\x18\x01 \x01(\x0b\x32\'.coop.rchain.comm.protocol.routing.Node\x12\x11\n\tnetworkId\x18\x02 \x01(\t\"\x0b\n\tHeartbeat\"\x13\n\x11HeartbeatResponse\"\"\n\x11ProtocolHandshake\x12\r\n\x05nonce\x18\x01 \x01(\x0c\"*\n\x19ProtocolHandshakeResponse\x12\r\n\x05nonce\x18\x01 \x01(\x0c\")\n\x06Packet\x12\x0e\n\x06typeId\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\x0c\"\x0c\n\nDisconnect\"\xce\x03\n\x08Protocol\x12\x39\n\x06header\x18\x01 \x01(\x0b\x32).coop.rchain.comm.protocol.routing.Header\x12\x41\n\theartbeat\x18\x02 \x01(\x0b\x32,.coop.rchain.comm.protocol.routing.HeartbeatH\x00\x12R\n\x12protocol_handshake\x18\x03 \x01(\x0b\x32\x34.coop.rchain.comm.protocol.routing.ProtocolHandshakeH\x00\x12\x63\n\x1bprotocol_handshake_response\x18\x04 \x01(\x0b\x32<.coop.rchain.comm.protocol.routing.ProtocolHandshakeResponseH\x00\x12;\n\x06packet\x18\x05 \x01(\x0b\x32).coop.rchain.comm.protocol.routing.PacketH\x00\x12\x43\n\ndisconnect\x18\x06 \x01(\x0b\x32-.coop.rchain.comm.protocol.routing.DisconnectH\x00\x42\t\n\x07message\"J\n\tTLRequest\x12=\n\x08protocol\x18\x01 \x01(\x0b\x32+.coop.rchain.comm.protocol.routing.Protocol\"$\n\x13InternalServerError\x12\r\n\x05\x65rror\x18\x01 \x01(\x0c\"G\n\nNoResponse\x12\x39\n\x06header\x18\x01 \x01(\x0b\x32).coop.rchain.comm.protocol.routing.Header\"\xb3\x01\n\nTLResponse\x12\x43\n\nnoResponse\x18\x01 \x01(\x0b\x32-.coop.rchain.comm.protocol.routing.NoResponseH\x00\x12U\n\x13internalServerError\x18\x02 \x01(\x0b\x32\x36.coop.rchain.comm.protocol.routing.InternalServerErrorH\x00\x42\t\n\x07payload\"\x94\x01\n\x0b\x43hunkHeader\x12\x37\n\x06sender\x18\x01 \x01(\x0b\x32\'.coop.rchain.comm.protocol.routing.Node\x12\x0e\n\x06typeId\x18\x02 \x01(\t\x12\x12\n\ncompressed\x18\x03 \x01(\x08\x12\x15\n\rcontentLength\x18\x04 \x01(\x05\x12\x11\n\tnetworkId\x18\x05 \x01(\t\" \n\tChunkData\x12\x13\n\x0b\x63ontentData\x18\x01 \x01(\x0c\"\x92\x01\n\x05\x43hunk\x12@\n\x06header\x18\x01 \x01(\x0b\x32..coop.rchain.comm.protocol.routing.ChunkHeaderH\x00\x12<\n\x04\x64\x61ta\x18\x02 \x01(\x0b\x32,.coop.rchain.comm.protocol.routing.ChunkDataH\x00\x42\t\n\x07\x63ontent\"\x0f\n\rChunkResponse2\xe1\x01\n\x0eTransportLayer\x12\x65\n\x04Send\x12,.coop.rchain.comm.protocol.routing.TLRequest\x1a-.coop.rchain.comm.protocol.routing.TLResponse\"\x00\x12h\n\x06Stream\x12(.coop.rchain.comm.protocol.routing.Chunk\x1a\x30.coop.rchain.comm.protocol.routing.ChunkResponse\"\x00(\x01\x42(\xe2?%\n!coop.rchain.comm.protocol.routing\x10\x01\x62\x06proto3')
  ,
  dependencies=[scalapb_dot_scalapb__pb2.DESCRIPTOR,CasperMessage__pb2.DESCRIPTOR,])




_NODE = _descriptor.Descriptor(
  name='Node',
  full_name='coop.rchain.comm.protocol.routing.Node',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='coop.rchain.comm.protocol.routing.Node.id', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='host', full_name='coop.rchain.comm.protocol.routing.Node.host', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='tcp_port', full_name='coop.rchain.comm.protocol.routing.Node.tcp_port', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='udp_port', full_name='coop.rchain.comm.protocol.routing.Node.udp_port', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=96,
  serialized_end=164,
)


_HEADER = _descriptor.Descriptor(
  name='Header',
  full_name='coop.rchain.comm.protocol.routing.Header',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sender', full_name='coop.rchain.comm.protocol.routing.Header.sender', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='networkId', full_name='coop.rchain.comm.protocol.routing.Header.networkId', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=166,
  serialized_end=250,
)


_HEARTBEAT = _descriptor.Descriptor(
  name='Heartbeat',
  full_name='coop.rchain.comm.protocol.routing.Heartbeat',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
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
  serialized_start=252,
  serialized_end=263,
)


_HEARTBEATRESPONSE = _descriptor.Descriptor(
  name='HeartbeatResponse',
  full_name='coop.rchain.comm.protocol.routing.HeartbeatResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
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
  serialized_start=265,
  serialized_end=284,
)


_PROTOCOLHANDSHAKE = _descriptor.Descriptor(
  name='ProtocolHandshake',
  full_name='coop.rchain.comm.protocol.routing.ProtocolHandshake',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='nonce', full_name='coop.rchain.comm.protocol.routing.ProtocolHandshake.nonce', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=286,
  serialized_end=320,
)


_PROTOCOLHANDSHAKERESPONSE = _descriptor.Descriptor(
  name='ProtocolHandshakeResponse',
  full_name='coop.rchain.comm.protocol.routing.ProtocolHandshakeResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='nonce', full_name='coop.rchain.comm.protocol.routing.ProtocolHandshakeResponse.nonce', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=322,
  serialized_end=364,
)


_PACKET = _descriptor.Descriptor(
  name='Packet',
  full_name='coop.rchain.comm.protocol.routing.Packet',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='typeId', full_name='coop.rchain.comm.protocol.routing.Packet.typeId', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='content', full_name='coop.rchain.comm.protocol.routing.Packet.content', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=366,
  serialized_end=407,
)


_DISCONNECT = _descriptor.Descriptor(
  name='Disconnect',
  full_name='coop.rchain.comm.protocol.routing.Disconnect',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
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
  serialized_start=409,
  serialized_end=421,
)


_PROTOCOL = _descriptor.Descriptor(
  name='Protocol',
  full_name='coop.rchain.comm.protocol.routing.Protocol',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='header', full_name='coop.rchain.comm.protocol.routing.Protocol.header', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='heartbeat', full_name='coop.rchain.comm.protocol.routing.Protocol.heartbeat', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='protocol_handshake', full_name='coop.rchain.comm.protocol.routing.Protocol.protocol_handshake', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='protocol_handshake_response', full_name='coop.rchain.comm.protocol.routing.Protocol.protocol_handshake_response', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='packet', full_name='coop.rchain.comm.protocol.routing.Protocol.packet', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='disconnect', full_name='coop.rchain.comm.protocol.routing.Protocol.disconnect', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
    _descriptor.OneofDescriptor(
      name='message', full_name='coop.rchain.comm.protocol.routing.Protocol.message',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=424,
  serialized_end=886,
)


_TLREQUEST = _descriptor.Descriptor(
  name='TLRequest',
  full_name='coop.rchain.comm.protocol.routing.TLRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='protocol', full_name='coop.rchain.comm.protocol.routing.TLRequest.protocol', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=888,
  serialized_end=962,
)


_INTERNALSERVERERROR = _descriptor.Descriptor(
  name='InternalServerError',
  full_name='coop.rchain.comm.protocol.routing.InternalServerError',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='error', full_name='coop.rchain.comm.protocol.routing.InternalServerError.error', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=964,
  serialized_end=1000,
)


_NORESPONSE = _descriptor.Descriptor(
  name='NoResponse',
  full_name='coop.rchain.comm.protocol.routing.NoResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='header', full_name='coop.rchain.comm.protocol.routing.NoResponse.header', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=1002,
  serialized_end=1073,
)


_TLRESPONSE = _descriptor.Descriptor(
  name='TLResponse',
  full_name='coop.rchain.comm.protocol.routing.TLResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='noResponse', full_name='coop.rchain.comm.protocol.routing.TLResponse.noResponse', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='internalServerError', full_name='coop.rchain.comm.protocol.routing.TLResponse.internalServerError', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
    _descriptor.OneofDescriptor(
      name='payload', full_name='coop.rchain.comm.protocol.routing.TLResponse.payload',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=1076,
  serialized_end=1255,
)


_CHUNKHEADER = _descriptor.Descriptor(
  name='ChunkHeader',
  full_name='coop.rchain.comm.protocol.routing.ChunkHeader',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sender', full_name='coop.rchain.comm.protocol.routing.ChunkHeader.sender', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='typeId', full_name='coop.rchain.comm.protocol.routing.ChunkHeader.typeId', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='compressed', full_name='coop.rchain.comm.protocol.routing.ChunkHeader.compressed', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='contentLength', full_name='coop.rchain.comm.protocol.routing.ChunkHeader.contentLength', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='networkId', full_name='coop.rchain.comm.protocol.routing.ChunkHeader.networkId', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=1258,
  serialized_end=1406,
)


_CHUNKDATA = _descriptor.Descriptor(
  name='ChunkData',
  full_name='coop.rchain.comm.protocol.routing.ChunkData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='contentData', full_name='coop.rchain.comm.protocol.routing.ChunkData.contentData', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=1408,
  serialized_end=1440,
)


_CHUNK = _descriptor.Descriptor(
  name='Chunk',
  full_name='coop.rchain.comm.protocol.routing.Chunk',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='header', full_name='coop.rchain.comm.protocol.routing.Chunk.header', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='data', full_name='coop.rchain.comm.protocol.routing.Chunk.data', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
    _descriptor.OneofDescriptor(
      name='content', full_name='coop.rchain.comm.protocol.routing.Chunk.content',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=1443,
  serialized_end=1589,
)


_CHUNKRESPONSE = _descriptor.Descriptor(
  name='ChunkResponse',
  full_name='coop.rchain.comm.protocol.routing.ChunkResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
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
  serialized_start=1591,
  serialized_end=1606,
)

_HEADER.fields_by_name['sender'].message_type = _NODE
_PROTOCOL.fields_by_name['header'].message_type = _HEADER
_PROTOCOL.fields_by_name['heartbeat'].message_type = _HEARTBEAT
_PROTOCOL.fields_by_name['protocol_handshake'].message_type = _PROTOCOLHANDSHAKE
_PROTOCOL.fields_by_name['protocol_handshake_response'].message_type = _PROTOCOLHANDSHAKERESPONSE
_PROTOCOL.fields_by_name['packet'].message_type = _PACKET
_PROTOCOL.fields_by_name['disconnect'].message_type = _DISCONNECT
_PROTOCOL.oneofs_by_name['message'].fields.append(
  _PROTOCOL.fields_by_name['heartbeat'])
_PROTOCOL.fields_by_name['heartbeat'].containing_oneof = _PROTOCOL.oneofs_by_name['message']
_PROTOCOL.oneofs_by_name['message'].fields.append(
  _PROTOCOL.fields_by_name['protocol_handshake'])
_PROTOCOL.fields_by_name['protocol_handshake'].containing_oneof = _PROTOCOL.oneofs_by_name['message']
_PROTOCOL.oneofs_by_name['message'].fields.append(
  _PROTOCOL.fields_by_name['protocol_handshake_response'])
_PROTOCOL.fields_by_name['protocol_handshake_response'].containing_oneof = _PROTOCOL.oneofs_by_name['message']
_PROTOCOL.oneofs_by_name['message'].fields.append(
  _PROTOCOL.fields_by_name['packet'])
_PROTOCOL.fields_by_name['packet'].containing_oneof = _PROTOCOL.oneofs_by_name['message']
_PROTOCOL.oneofs_by_name['message'].fields.append(
  _PROTOCOL.fields_by_name['disconnect'])
_PROTOCOL.fields_by_name['disconnect'].containing_oneof = _PROTOCOL.oneofs_by_name['message']
_TLREQUEST.fields_by_name['protocol'].message_type = _PROTOCOL
_NORESPONSE.fields_by_name['header'].message_type = _HEADER
_TLRESPONSE.fields_by_name['noResponse'].message_type = _NORESPONSE
_TLRESPONSE.fields_by_name['internalServerError'].message_type = _INTERNALSERVERERROR
_TLRESPONSE.oneofs_by_name['payload'].fields.append(
  _TLRESPONSE.fields_by_name['noResponse'])
_TLRESPONSE.fields_by_name['noResponse'].containing_oneof = _TLRESPONSE.oneofs_by_name['payload']
_TLRESPONSE.oneofs_by_name['payload'].fields.append(
  _TLRESPONSE.fields_by_name['internalServerError'])
_TLRESPONSE.fields_by_name['internalServerError'].containing_oneof = _TLRESPONSE.oneofs_by_name['payload']
_CHUNKHEADER.fields_by_name['sender'].message_type = _NODE
_CHUNK.fields_by_name['header'].message_type = _CHUNKHEADER
_CHUNK.fields_by_name['data'].message_type = _CHUNKDATA
_CHUNK.oneofs_by_name['content'].fields.append(
  _CHUNK.fields_by_name['header'])
_CHUNK.fields_by_name['header'].containing_oneof = _CHUNK.oneofs_by_name['content']
_CHUNK.oneofs_by_name['content'].fields.append(
  _CHUNK.fields_by_name['data'])
_CHUNK.fields_by_name['data'].containing_oneof = _CHUNK.oneofs_by_name['content']
DESCRIPTOR.message_types_by_name['Node'] = _NODE
DESCRIPTOR.message_types_by_name['Header'] = _HEADER
DESCRIPTOR.message_types_by_name['Heartbeat'] = _HEARTBEAT
DESCRIPTOR.message_types_by_name['HeartbeatResponse'] = _HEARTBEATRESPONSE
DESCRIPTOR.message_types_by_name['ProtocolHandshake'] = _PROTOCOLHANDSHAKE
DESCRIPTOR.message_types_by_name['ProtocolHandshakeResponse'] = _PROTOCOLHANDSHAKERESPONSE
DESCRIPTOR.message_types_by_name['Packet'] = _PACKET
DESCRIPTOR.message_types_by_name['Disconnect'] = _DISCONNECT
DESCRIPTOR.message_types_by_name['Protocol'] = _PROTOCOL
DESCRIPTOR.message_types_by_name['TLRequest'] = _TLREQUEST
DESCRIPTOR.message_types_by_name['InternalServerError'] = _INTERNALSERVERERROR
DESCRIPTOR.message_types_by_name['NoResponse'] = _NORESPONSE
DESCRIPTOR.message_types_by_name['TLResponse'] = _TLRESPONSE
DESCRIPTOR.message_types_by_name['ChunkHeader'] = _CHUNKHEADER
DESCRIPTOR.message_types_by_name['ChunkData'] = _CHUNKDATA
DESCRIPTOR.message_types_by_name['Chunk'] = _CHUNK
DESCRIPTOR.message_types_by_name['ChunkResponse'] = _CHUNKRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Node = _reflection.GeneratedProtocolMessageType('Node', (_message.Message,), dict(
  DESCRIPTOR = _NODE,
  __module__ = 'routing_pb2'
  # @@protoc_insertion_point(class_scope:coop.rchain.comm.protocol.routing.Node)
  ))
_sym_db.RegisterMessage(Node)

Header = _reflection.GeneratedProtocolMessageType('Header', (_message.Message,), dict(
  DESCRIPTOR = _HEADER,
  __module__ = 'routing_pb2'
  # @@protoc_insertion_point(class_scope:coop.rchain.comm.protocol.routing.Header)
  ))
_sym_db.RegisterMessage(Header)

Heartbeat = _reflection.GeneratedProtocolMessageType('Heartbeat', (_message.Message,), dict(
  DESCRIPTOR = _HEARTBEAT,
  __module__ = 'routing_pb2'
  # @@protoc_insertion_point(class_scope:coop.rchain.comm.protocol.routing.Heartbeat)
  ))
_sym_db.RegisterMessage(Heartbeat)

HeartbeatResponse = _reflection.GeneratedProtocolMessageType('HeartbeatResponse', (_message.Message,), dict(
  DESCRIPTOR = _HEARTBEATRESPONSE,
  __module__ = 'routing_pb2'
  # @@protoc_insertion_point(class_scope:coop.rchain.comm.protocol.routing.HeartbeatResponse)
  ))
_sym_db.RegisterMessage(HeartbeatResponse)

ProtocolHandshake = _reflection.GeneratedProtocolMessageType('ProtocolHandshake', (_message.Message,), dict(
  DESCRIPTOR = _PROTOCOLHANDSHAKE,
  __module__ = 'routing_pb2'
  # @@protoc_insertion_point(class_scope:coop.rchain.comm.protocol.routing.ProtocolHandshake)
  ))
_sym_db.RegisterMessage(ProtocolHandshake)

ProtocolHandshakeResponse = _reflection.GeneratedProtocolMessageType('ProtocolHandshakeResponse', (_message.Message,), dict(
  DESCRIPTOR = _PROTOCOLHANDSHAKERESPONSE,
  __module__ = 'routing_pb2'
  # @@protoc_insertion_point(class_scope:coop.rchain.comm.protocol.routing.ProtocolHandshakeResponse)
  ))
_sym_db.RegisterMessage(ProtocolHandshakeResponse)

Packet = _reflection.GeneratedProtocolMessageType('Packet', (_message.Message,), dict(
  DESCRIPTOR = _PACKET,
  __module__ = 'routing_pb2'
  # @@protoc_insertion_point(class_scope:coop.rchain.comm.protocol.routing.Packet)
  ))
_sym_db.RegisterMessage(Packet)

Disconnect = _reflection.GeneratedProtocolMessageType('Disconnect', (_message.Message,), dict(
  DESCRIPTOR = _DISCONNECT,
  __module__ = 'routing_pb2'
  # @@protoc_insertion_point(class_scope:coop.rchain.comm.protocol.routing.Disconnect)
  ))
_sym_db.RegisterMessage(Disconnect)

Protocol = _reflection.GeneratedProtocolMessageType('Protocol', (_message.Message,), dict(
  DESCRIPTOR = _PROTOCOL,
  __module__ = 'routing_pb2'
  # @@protoc_insertion_point(class_scope:coop.rchain.comm.protocol.routing.Protocol)
  ))
_sym_db.RegisterMessage(Protocol)

TLRequest = _reflection.GeneratedProtocolMessageType('TLRequest', (_message.Message,), dict(
  DESCRIPTOR = _TLREQUEST,
  __module__ = 'routing_pb2'
  # @@protoc_insertion_point(class_scope:coop.rchain.comm.protocol.routing.TLRequest)
  ))
_sym_db.RegisterMessage(TLRequest)

InternalServerError = _reflection.GeneratedProtocolMessageType('InternalServerError', (_message.Message,), dict(
  DESCRIPTOR = _INTERNALSERVERERROR,
  __module__ = 'routing_pb2'
  # @@protoc_insertion_point(class_scope:coop.rchain.comm.protocol.routing.InternalServerError)
  ))
_sym_db.RegisterMessage(InternalServerError)

NoResponse = _reflection.GeneratedProtocolMessageType('NoResponse', (_message.Message,), dict(
  DESCRIPTOR = _NORESPONSE,
  __module__ = 'routing_pb2'
  # @@protoc_insertion_point(class_scope:coop.rchain.comm.protocol.routing.NoResponse)
  ))
_sym_db.RegisterMessage(NoResponse)

TLResponse = _reflection.GeneratedProtocolMessageType('TLResponse', (_message.Message,), dict(
  DESCRIPTOR = _TLRESPONSE,
  __module__ = 'routing_pb2'
  # @@protoc_insertion_point(class_scope:coop.rchain.comm.protocol.routing.TLResponse)
  ))
_sym_db.RegisterMessage(TLResponse)

ChunkHeader = _reflection.GeneratedProtocolMessageType('ChunkHeader', (_message.Message,), dict(
  DESCRIPTOR = _CHUNKHEADER,
  __module__ = 'routing_pb2'
  # @@protoc_insertion_point(class_scope:coop.rchain.comm.protocol.routing.ChunkHeader)
  ))
_sym_db.RegisterMessage(ChunkHeader)

ChunkData = _reflection.GeneratedProtocolMessageType('ChunkData', (_message.Message,), dict(
  DESCRIPTOR = _CHUNKDATA,
  __module__ = 'routing_pb2'
  # @@protoc_insertion_point(class_scope:coop.rchain.comm.protocol.routing.ChunkData)
  ))
_sym_db.RegisterMessage(ChunkData)

Chunk = _reflection.GeneratedProtocolMessageType('Chunk', (_message.Message,), dict(
  DESCRIPTOR = _CHUNK,
  __module__ = 'routing_pb2'
  # @@protoc_insertion_point(class_scope:coop.rchain.comm.protocol.routing.Chunk)
  ))
_sym_db.RegisterMessage(Chunk)

ChunkResponse = _reflection.GeneratedProtocolMessageType('ChunkResponse', (_message.Message,), dict(
  DESCRIPTOR = _CHUNKRESPONSE,
  __module__ = 'routing_pb2'
  # @@protoc_insertion_point(class_scope:coop.rchain.comm.protocol.routing.ChunkResponse)
  ))
_sym_db.RegisterMessage(ChunkResponse)


DESCRIPTOR._options = None

_TRANSPORTLAYER = _descriptor.ServiceDescriptor(
  name='TransportLayer',
  full_name='coop.rchain.comm.protocol.routing.TransportLayer',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=1609,
  serialized_end=1834,
  methods=[
  _descriptor.MethodDescriptor(
    name='Send',
    full_name='coop.rchain.comm.protocol.routing.TransportLayer.Send',
    index=0,
    containing_service=None,
    input_type=_TLREQUEST,
    output_type=_TLRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Stream',
    full_name='coop.rchain.comm.protocol.routing.TransportLayer.Stream',
    index=1,
    containing_service=None,
    input_type=_CHUNK,
    output_type=_CHUNKRESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_TRANSPORTLAYER)

DESCRIPTOR.services_by_name['TransportLayer'] = _TRANSPORTLAYER

# @@protoc_insertion_point(module_scope)
