# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: knn.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'knn.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\tknn.proto\x12\x03knn\"+\n\nKNNRequest\x12\x12\n\ndata_point\x18\x01 \x03(\x02\x12\t\n\x01k\x18\x02 \x01(\x05\"+\n\x08Neighbor\x12\r\n\x05point\x18\x01 \x03(\x02\x12\x10\n\x08\x64istance\x18\x02 \x01(\x02\"/\n\x0bKNNResponse\x12 \n\tneighbors\x18\x01 \x03(\x0b\x32\r.knn.Neighbor2H\n\nKNNService\x12:\n\x15\x46indKNearestNeighbors\x12\x0f.knn.KNNRequest\x1a\x10.knn.KNNResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'knn_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_KNNREQUEST']._serialized_start=18
  _globals['_KNNREQUEST']._serialized_end=61
  _globals['_NEIGHBOR']._serialized_start=63
  _globals['_NEIGHBOR']._serialized_end=106
  _globals['_KNNRESPONSE']._serialized_start=108
  _globals['_KNNRESPONSE']._serialized_end=155
  _globals['_KNNSERVICE']._serialized_start=157
  _globals['_KNNSERVICE']._serialized_end=229
# @@protoc_insertion_point(module_scope)
