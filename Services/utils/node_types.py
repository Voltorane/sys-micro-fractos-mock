import enum

class NodeType(str, enum.Enum):
    PredictorNode = "PREDICTOR"
    OutputCollectorNode = "STORAGE"
    ImageSenderNode = "IMAGE_SENDER"