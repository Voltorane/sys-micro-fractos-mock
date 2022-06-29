from kazoo.client import KazooClient
from datetime import datetime
# https://sleeplessbeastie.eu/2021/10/20/how-to-use-zookeeper-to-elect-the-leader-with-a-python-script/

class ZKeeper():
    # :attr:`~kazoo.interfaces.IHandler.timeout_exception`
    #              if the connection wasn't established within `timeout`
    #              seconds.
    def __init__(self, ip, server_name, logger):
        try:
            self.logger = logger
            self.logger.info(f"Initializing zookeeper for {server_name}...")
            self.zookeeper = KazooClient(ip)
            self.server_name = server_name + datetime.now().strftime("%H:%M:%S")
            try:
                self.server_dict = {"node" : self.server_name.split("_")[0], "sequence" : self.server_name.split("_")[1]}
            except:
                self.server_dict = {"node" : self.server_name, "sequence" : ""}
            self.logger.info("Server name: ", server_name)
            self.path_nodes = "/node_storage"
            self.path_data = "/data"
            self.logger.info(f"Connecting to {ip}...")
            self.connect()
            self.logger.info(f"Connection successfull!")
            self.register()
            self.watch_application_nodes()
            self.watch_application_data()
        except Exception as e:
            self.logger.error(f"ERROR {str(e)} occured, while loading zookeeper for: {server_name} on {ip}")

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
        self.logger.info(f"Current leader: {current_leader['node']}_{current_leader['sequence']}")

        self.display_server_information(application_nodes, current_leader)
        if current_leader['node'] == self.server_dict['node'] and current_leader['sequence'] == self.server_dict['sequence']:
            self.update_shared_data()

    def check_application_data(self, data, stat):
        self.logger.info(
            "Data change detected on {0}:\nData: {1}\nStat: {2}".format((datetime.now()).strftime("%B %d, %Y %H:%M:%S"),
                                                                        data, stat), "\n")

    def update_shared_data(self):
        if not self.zookeeper.exists(self.path_data):
            self.zookeeper.create(self.path_data,
                                  bytes("name: {0}\ndata: {1}".format(self.server_name, self.server_data), "utf8"),
                                  ephemeral=True, sequence=False, makepath=True)

    def display_server_information(self, application_nodes, current_leader):
        self.logger.info("Datetime: {0}".format((datetime.now()).strftime("%B %d, %Y %H:%M:%S")))
        self.logger.info("Nodes:")
        self.logger.info("Server name: {0}".format(self.server_name))
        for i in application_nodes:
            self.logger.info("  - {0} with sequence {1}".format(i["node"], i["sequence"]))
        self.logger.info("Role: {0}".format("leader" if current_leader['node'] == self.server_dict['node'] and current_leader['sequence'] == self.server_dict['sequence'] else "follower"), "\n")

    def __del__(self):
        self.logger.warning("Closing connection...")
        self.zookeeper.close()    
        self.logger.warning("Disconnected from server.")
