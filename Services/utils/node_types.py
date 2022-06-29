import enum

class NodeType(str, enum.Enum):
    PredictorNode = "PREDICTOR"
    OutputCollectorNode = "STORAGE"
    ImageSenderNode = "IMAGE_SENDER"
    IntSenderNode = "INT_SENDER"
    MathComputeNode = "MATH_COMPUTE"


def parse_next_request(request):
    request = request.split(",")
    node_type = request[0]
    ip = request[1]
    request = request[2:]
    if node_type == NodeType.ImageSenderNode.value:
        img_width, img_height, client_id, name = None, None, "", ""
        for argument in request:
            argument = argument.split(":")
            key, value = argument[0], argument[1]
            if key == "img_width":
                img_width = int(value)
            elif key == "img_height":
                img_height = int(value)
            elif key == "client_id":
                client_id = value
            elif key == "name":
                name = value
        return [NodeType.ImageSenderNode, ip, name, img_width, img_height, client_id]
    elif node_type == NodeType.IntSenderNode.value:
        # client id for the correct location
        # name - name of the file with number
        client_id, name = "", ""
        for argument in request:
            argument = argument.split(":")
            key, value = argument[0], argument[1]
            if key == "client_id":
                client_id = value
            elif key == "name":
                name = value
        return [NodeType.IntSenderNode, ip, name, client_id]
    elif node_type == NodeType.PredictorNode.value:
        img_width, img_height, client_id = None, None, ""
        for argument in request:
            argument = argument.split(":")
            key, value = argument[0], argument[1]
            if key == "img_width":
                img_width = int(value)
            elif key == "img_height":
                img_height = int(value)
            elif key == "client_id":
                client_id = value
        return [NodeType.PredictorNode, ip, img_width, img_height, client_id]
    elif node_type == NodeType.OutputCollectorNode.value:
        name, storage_id = "", ""
        for argument in request:
            argument = argument.split(":")
            key, value = argument[0], argument[1]
            if key == "storage_id":
                storage_id = value
            elif key == "name":
                name = value
        return [NodeType.OutputCollectorNode, ip, name, storage_id]
    elif node_type == NodeType.MathComputeNode.value:
        # n is not used is request with storage, but if provided in app, can be used directly here
        n = None
        for argument in request:
            key, value = argument.split(":")
            if key == "n":
                n = value
        return [NodeType.MathComputeNode.value, ip, n]
    return None