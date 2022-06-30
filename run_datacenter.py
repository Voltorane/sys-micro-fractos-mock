import os
import shutil
from configparser import ConfigParser

dir_path = os.path.dirname(__file__)
config_path = os.path.join(dir_path, "data_center_setup.cnf")
original_zookeeper_dir = os.path.join(dir_path, "apache-zookeeper-3.7.1-bin")
zookeeper_target_dir = os.path.join(dir_path, "zookeeper_test1")

config_parser = ConfigParser()   
config_parser.read(config_path)

def setup_zookeeper(ports):
    if not os.path.exists(zookeeper_target_dir):
        os.makedirs(zookeeper_target_dir)
    print(ports)
    servers = ''
    ip = "localhost"
    server_port1, server_port2 = 2888, 3888
    nb_servers = len(ports) + 1 if len(ports) % 2 == 0 else len(ports)
    bin_paths = {}
    
    for i in range(nb_servers):
        s = f"server.{i}={ip}:{server_port1}:{server_port2}\n"
        server_port1 += 1
        server_port2 += 1
        servers += s
    
    for id, port in enumerate(ports):
        id += 1
        path = os.path.join(zookeeper_target_dir, f"zookeeper{id}")
        shutil.copytree(original_zookeeper_dir, path)
        z_config_path = os.path.join(path, os.path.join("conf", "zoo.cfg"))
        with open(z_config_path, "w") as config:
            conf = f'''
            # The number of milliseconds of each tick
            tickTime=2000
            # The number of ticks that the initial 
            # synchronization phase can take
            initLimit=10
            # The number of ticks that can pass between 
            # sending a request and getting an acknowledgement
            syncLimit=5
            # the directory where the snapshot is stored.
            # do not use /tmp for storage, /tmp here is just 
            # example sakes.
            # dataDir=/tmp/zookeeper
            # the port at which the clients will connect
            # clientPort=2181

            dataDir=../data{id}
            clientPort={port}
            
            {servers}


            # the maximum number of client connections.
            # increase this if you need to handle more clients
            #maxClientCnxns=60
            #
            # Be sure to read the maintenance section of the 
            # administrator guide before turning on autopurge.
            #
            # http://zookeeper.apache.org/doc/current/zookeeperAdmin.html#sc_maintenance
            #
            # The number of snapshots to retain in dataDir
            #autopurge.snapRetainCount=3
            # Purge task interval in hours
            # Set to "0" to disable auto purge feature
            #autopurge.purgeInterval=1

            ## Metrics Providers
            #
            # https://prometheus.io Metrics Exporter
            #metricsProvider.className=org.apache.zookeeper.metrics.prometheus.PrometheusMetricsProvider
            #metricsProvider.httpPort=7000
            #metricsProvider.exportJvmInfo=true
            '''
            
            config.write(conf)
        
        bin_paths[os.path.join(path, "bin")] = z_config_path
        
        data_dir = os.path.join(path, f"data{id}")
        
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
        
        with open(os.path.join(data_dir, "myid"), "w") as myid:
            myid.write(str(id))
    
    request = ""
    for path in bin_paths.keys():
        executable = os.path.join(path, "zkServer.sh start")
        request += f"{executable} {bin_paths[path]} ; "
    
    print(request)
    
    os.system(f"gnome-terminal -e 'bash -c \"{request}; exec bash \"'")

def fill_internal_config(controller_port_dict, zookeeper_controller_port_dict={}, storage_path=""):
    service_config_paths = config_parser.get('DataCenter', 'service_config_paths')
    service_config_paths = service_config_paths.replace(" ", "").split(",")
    try:
        application_zookeeper_port = config_parser.get('Applications', 'application_zookeeper_port')
        zookeeper_controller_port_dict["application"] = application_zookeeper_port
    except Exception as e:
        print("application_zookeeper_port, could not be added")
    
    for path in service_config_paths:
        path_to_dir = os.path.join(dir_path, path)
        if not os.path.exists(path_to_dir):
            os.makedirs(path_to_dir)
        with open(os.path.join(path_to_dir, "grpc_ip.cfg"), "w") as grpc_ip_config:
            try:
                ip = config_parser.get('DataCenter', 'grpc_ip')
            except:
                print("Could not find 'grpc_ip' in [DataCenter] config")
            grpc_ip_config.write(ip)
        
        with open(os.path.join(path_to_dir, "controller_ports.cfg"), "w") as controller_ports_config:
            s = []
            for controller, port in controller_port_dict.items():
                s.append(f'{controller}:{port}\n')
            controller_ports_config.writelines(s)
        
        with open(os.path.join(path_to_dir, "zookeeper_controller_ports.cfg"), "w") as controller_ports_config:
            s = []
            for controller, port in zookeeper_controller_port_dict.items():
                s.append(f'{controller}:{port}\n')
            controller_ports_config.writelines(s)

        
def run_controllers():    
    controllers = config_parser.get('Controllers', 'controller_names')
    controllers = controllers.replace(" ", "").split(",")
    zookeeper_ports = set()
    controller_port_dict, zookeeper_controller_port_dict = {}, {}
    controller_path_dict = {}
    storage_path = ""
    for controller in controllers:
        paths_to_controller, servers, controller_port, verbose, zookeeper, zookeeper_port = "", "", "", "", "", ""
        try:
            paths_to_controller = config_parser.get(controller, "paths_to_controller")
            paths_to_controller = paths_to_controller.replace(" ", "").split(",")
            controller_path_dict[controller] = paths_to_controller
        except:
            # can't run controller without path
            print(f"Controller path for {controller} is not found in [{controller}] controller_port")
            continue
        # port on which the controller will run
        try:
            controller_port = config_parser.get(controller, "controller_port")
            controller_port_dict[controller] = controller_port
        except:
            # can't run controller without port
            print(f"Controller port for {controller} is not found or incorrect in [{controller}] controller_port")
            continue
        # print output in the terminal
        try:
            verbose = bool(config_parser.get(controller, "verbose"))
        except:
            pass
        # print output in the terminal
        try:
            storage_path = config_parser.get(controller, "storage_path")
        except:
            pass
        # run with zookeeper
        try:
            zookeeper = bool(config_parser.get(controller, "zookeeper"))
        except:
            pass
        # select zookeeper port for this controller
        try:
            zookeeper_port = config_parser.get(controller, "zookeeper_port")
            zookeeper_ports.add(zookeeper_port)
            zookeeper_controller_port_dict[controller] = zookeeper_port
        except:
            pass
        
    fill_internal_config(controller_port_dict, zookeeper_controller_port_dict, storage_path)

    for controller in controllers:
        for id, path in enumerate(controller_path_dict[controller]):
            runner_request = f"python3 {path} "
            runner_request += f"-n {id} "
            if zookeeper:
                runner_request += f"-z "
            if verbose:
                runner_request += f"-v "

            # code snippet taken from https://stackoverflow.com/questions/7574841/open-a-terminal-from-python
            os.system(f"gnome-terminal -e 'bash -c \"{runner_request}; exec bash \"'")
            print(f"Controller {path} is now running!")

if __name__ == "__main__":
    run_controllers()