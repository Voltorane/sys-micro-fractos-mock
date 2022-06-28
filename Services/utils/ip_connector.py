# extracts ip list from user-defined config
def extract_ip_list(path):
    with open(path, "r+") as f:
        ips = f.readlines()
    return ips

def extract_port(name, path):
    with open(path, "r+") as f:
        ports = f.readlines()
        for port in ports:
            port = port.split(":")
            port_name, value = port[0], port[1]
            if name == port_name:
                # code snippet taken from https://stackoverflow.com/questions/17336943/removing-non-numeric-characters-from-a-string
                port = "".join(c for c in value if c.isdigit())
                return port
    return None

def get_grpc_ip(path):
    with open(path, "r+") as f:
        return f.read()