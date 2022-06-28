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
                return value
    return None