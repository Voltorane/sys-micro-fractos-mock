# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: service_rpc.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11service_rpc.proto\x12\x11service_connector\"r\n\x11PredictionRequest\x12\r\n\x05image\x18\x01 \x01(\t\x12\x11\n\timg_width\x18\x02 \x01(\x05\x12\x12\n\nimg_height\x18\x03 \x01(\x05\x12\x11\n\tclient_id\x18\x04 \x01(\t\x12\x14\n\x0cnext_request\x18\x06 \x03(\t\"p\n\x0bInitRequest\x12\x14\n\x0csample_limit\x18\x01 \x01(\x05\x12\x0e\n\x06\x65pochs\x18\x02 \x01(\x05\x12\x11\n\timg_width\x18\x03 \x01(\x05\x12\x12\n\nimg_height\x18\x04 \x01(\x05\x12\x14\n\x0cnext_request\x18\x06 \x03(\t\"\\\n\x14OutputStorageRequest\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x12\n\nstorage_id\x18\x03 \x01(\t\x12\x14\n\x0cnext_request\x18\x06 \x03(\t\"\x83\x01\n\x10ImageSendRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x11\n\timg_width\x18\x02 \x01(\x05\x12\x12\n\nimg_height\x18\x03 \x01(\x05\x12\x11\n\tclient_id\x18\x04 \x01(\t\x12\x11\n\tnext_node\x18\x05 \x01(\t\x12\x14\n\x0cnext_request\x18\x06 \x03(\t\")\n\x16\x41pplicationInitRequest\x12\x0f\n\x07request\x18\x01 \x03(\t\"6\n\x08Response\x12\x15\n\rresponse_code\x18\x01 \x01(\x05\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t2\xaf\x01\n\tPredictor\x12Q\n\nPrediction\x12$.service_connector.PredictionRequest\x1a\x1b.service_connector.Response\"\x00\x12O\n\x0eInitialization\x12\x1e.service_connector.InitRequest\x1a\x1b.service_connector.Response\"\x00\x32h\n\x0fOutputCollector\x12U\n\x0bStoreOutput\x12\'.service_connector.OutputStorageRequest\x1a\x1b.service_connector.Response\"\x00\x32^\n\x0bImageSender\x12O\n\tSendImage\x12#.service_connector.ImageSendRequest\x1a\x1b.service_connector.Response\"\x00\x32t\n\x12\x41pplicationStarter\x12^\n\x12SendInitialRequest\x12).service_connector.ApplicationInitRequest\x1a\x1b.service_connector.Response\"\x00\x42 B\x11Service_ConnectorP\x01\xa2\x02\x08SERVCONNb\x06proto3')



_PREDICTIONREQUEST = DESCRIPTOR.message_types_by_name['PredictionRequest']
_INITREQUEST = DESCRIPTOR.message_types_by_name['InitRequest']
_OUTPUTSTORAGEREQUEST = DESCRIPTOR.message_types_by_name['OutputStorageRequest']
_IMAGESENDREQUEST = DESCRIPTOR.message_types_by_name['ImageSendRequest']
_APPLICATIONINITREQUEST = DESCRIPTOR.message_types_by_name['ApplicationInitRequest']
_RESPONSE = DESCRIPTOR.message_types_by_name['Response']
PredictionRequest = _reflection.GeneratedProtocolMessageType('PredictionRequest', (_message.Message,), {
  'DESCRIPTOR' : _PREDICTIONREQUEST,
  '__module__' : 'service_rpc_pb2'
  # @@protoc_insertion_point(class_scope:service_connector.PredictionRequest)
  })
_sym_db.RegisterMessage(PredictionRequest)

InitRequest = _reflection.GeneratedProtocolMessageType('InitRequest', (_message.Message,), {
  'DESCRIPTOR' : _INITREQUEST,
  '__module__' : 'service_rpc_pb2'
  # @@protoc_insertion_point(class_scope:service_connector.InitRequest)
  })
_sym_db.RegisterMessage(InitRequest)

OutputStorageRequest = _reflection.GeneratedProtocolMessageType('OutputStorageRequest', (_message.Message,), {
  'DESCRIPTOR' : _OUTPUTSTORAGEREQUEST,
  '__module__' : 'service_rpc_pb2'
  # @@protoc_insertion_point(class_scope:service_connector.OutputStorageRequest)
  })
_sym_db.RegisterMessage(OutputStorageRequest)

ImageSendRequest = _reflection.GeneratedProtocolMessageType('ImageSendRequest', (_message.Message,), {
  'DESCRIPTOR' : _IMAGESENDREQUEST,
  '__module__' : 'service_rpc_pb2'
  # @@protoc_insertion_point(class_scope:service_connector.ImageSendRequest)
  })
_sym_db.RegisterMessage(ImageSendRequest)

ApplicationInitRequest = _reflection.GeneratedProtocolMessageType('ApplicationInitRequest', (_message.Message,), {
  'DESCRIPTOR' : _APPLICATIONINITREQUEST,
  '__module__' : 'service_rpc_pb2'
  # @@protoc_insertion_point(class_scope:service_connector.ApplicationInitRequest)
  })
_sym_db.RegisterMessage(ApplicationInitRequest)

Response = _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), {
  'DESCRIPTOR' : _RESPONSE,
  '__module__' : 'service_rpc_pb2'
  # @@protoc_insertion_point(class_scope:service_connector.Response)
  })
_sym_db.RegisterMessage(Response)

_PREDICTOR = DESCRIPTOR.services_by_name['Predictor']
_OUTPUTCOLLECTOR = DESCRIPTOR.services_by_name['OutputCollector']
_IMAGESENDER = DESCRIPTOR.services_by_name['ImageSender']
_APPLICATIONSTARTER = DESCRIPTOR.services_by_name['ApplicationStarter']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'B\021Service_ConnectorP\001\242\002\010SERVCONN'
  _PREDICTIONREQUEST._serialized_start=40
  _PREDICTIONREQUEST._serialized_end=154
  _INITREQUEST._serialized_start=156
  _INITREQUEST._serialized_end=268
  _OUTPUTSTORAGEREQUEST._serialized_start=270
  _OUTPUTSTORAGEREQUEST._serialized_end=362
  _IMAGESENDREQUEST._serialized_start=365
  _IMAGESENDREQUEST._serialized_end=496
  _APPLICATIONINITREQUEST._serialized_start=498
  _APPLICATIONINITREQUEST._serialized_end=539
  _RESPONSE._serialized_start=541
  _RESPONSE._serialized_end=595
  _PREDICTOR._serialized_start=598
  _PREDICTOR._serialized_end=773
  _OUTPUTCOLLECTOR._serialized_start=775
  _OUTPUTCOLLECTOR._serialized_end=879
  _IMAGESENDER._serialized_start=881
  _IMAGESENDER._serialized_end=975
  _APPLICATIONSTARTER._serialized_start=977
  _APPLICATIONSTARTER._serialized_end=1093
# @@protoc_insertion_point(module_scope)
