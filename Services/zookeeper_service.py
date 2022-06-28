from kazoo.client import KazooClient
from datetime import datetime
# https://sleeplessbeastie.eu/2021/10/20/how-to-use-zookeeper-to-elect-the-leader-with-a-python-script/

class ZKeeper():
    # :attr:`~kazoo.interfaces.IHandler.timeout_exception`
    #              if the connection wasn't established within `timeout`
    #              seconds.
    def __init__(self, ip, server_name):
        try:
            print(f"Initializing zookeeper for {server_name}...")
            self.zookeeper = KazooClient(ip)
            self.server_name = server_name
            self.path_nodes = "/node_storage"
            self.path_data = "/data"
            print(f"Connecting to {ip}...")
            self.connect()
            print(f"Connection successfull!")
            self.register()
            self.watch_application_nodes()
            self.watch_application_data()
        except Exception as e:
            print(f"Error {str(e)} occured, while loading zookeeper for: {server_name} on {ip}")
    
    def connect(self):
        self.zookeeper.start()

    def register(self):
        self.zookeeper.create("{0}/{1}_".format(self.path_nodes, self.server_name),
                              ephemeral=True, sequence=True, makepath=True)

    def watch_application_data(self):
        self.zookeeper.ensure_path(self.path_data)
        self.zookeeper.DataWatch(path=self.path_data, func=self.check_application_data)

    def watch_application_nodes(self):
        self.zookeeper.ensure_path(self.path_nodes)
        self.zookeeper.ChildrenWatch(path=self.path_nodes, func=self.check_application_nodes)

    def check_application_nodes(self, children):
        application_nodes = [{"node": i[0], "sequence": i[1]} for i in (i.split("_") for i in children)]
        current_leader = min(application_nodes, key=lambda x: x["sequence"])
        # print("ababa",application_nodes)
        print(f"Current leader: {current_leader['node']}_{current_leader['sequence']}")

        self.display_server_information(application_nodes, current_leader)
        if current_leader == self.server_name:
            self.update_shared_data()

    def check_application_data(self, data, stat):
        print(
            "Data change detected on {0}:\nData: {1}\nStat: {2}".format((datetime.now()).strftime("%B %d, %Y %H:%M:%S"),
                                                                        data, stat))
        print()

    def update_shared_data(self):
        if not self.zookeeper.exists(self.path_data):
            self.zookeeper.create(self.path_data,
                                  bytes("name: {0}\ndata: {1}".format(self.server_name, self.server_data), "utf8"),
                                  ephemeral=True, sequence=False, makepath=True)

    def display_server_information(self, application_nodes, current_leader):
        print("Datetime: {0}".format((datetime.now()).strftime("%B %d, %Y %H:%M:%S")))
        print("Server name: {0}".format(self.server_name))
        print("Nodes:")
        for i in application_nodes:
            print("  - {0} with sequence {1}".format(i["node"], i["sequence"]))
        print("Role: {0}".format("leader" if current_leader == self.server_name else "follower"))
        print()

    def __del__(self):
        self.zookeeper.close()    