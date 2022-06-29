import enum

class NodeType(str, enum.Enum):
    PredictorNode = "PREDICTOR"
    OutputCollectorNode = "STORAGE"
    DataSenderNode = "DATA_SENDER"