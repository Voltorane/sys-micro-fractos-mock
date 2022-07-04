from asyncio import subprocess
import os
import shutil
from configparser import ConfigParser
from pathlib import Path
import getopt
import sys

dir_path = os.path.dirname(__file__)
abs_path = Path(__file__).parent.absolute()
config_path = os.path.join(dir_path, "data_center_setup.cnf")
original_zookeeper_dir = os.path.join(dir_path, "apache-zookeeper-3.7.1-bin")
zookeeper_target_dir = os.path.join(dir_path, "zookeeper")

config_parser = ConfigParser()   
config_parser.read(config_path)

def setup_zookeeper():
    print("Setting the zookeeper up!")
    controller_dict, _, application_zookeeper_port = get_config_data()
    ports = {controller_dict[controller]["zookeeper_port"] for controller in controller_dict.keys()}
    ports.add(application_zookeeper_port)
    if not os.path.exists(zookeeper_target_dir):
        os.makedirs(zookeeper_target_dir)
    else:
        shutil.rmtree(zookeeper_target_dir)
    servers = ''
    ip = "localhost"
    server_port1, server_port2 = 2870, 3870
    nb_servers = len(ports) + 1 if len(ports) % 2 == 0 else len(ports)
    bin_paths = {}
    
    for i in range(nb_servers):
        s = f"server.{i}={ip}:{server_port1}:{server_port2}\n"
        server_port1 += 1
        server_port2 += 1
        servers += s
    
    for id, port in enumerate(ports):
        path = os.path.join(zookeeper_target_dir, f"zookeeper{id}")
        shutil.copytree(original_zookeeper_dir, path)
        print(f"Zookeeper folder {path} created!")
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
        
        print(f"Zookeeper folder {path} filled!")
    
    print("Zookeeper setup was done!")
    # request = ""
    # for path in bin_paths.keys():
    #     executable = "./zkServer.sh start"
    #     # sys.path.insert(1, path)
    #     request = f"cd {path} ; {executable} ; cd .. ; cd .. ;"
    #     # request += f"{executable} {bin_paths[path]} ; "
    #     os.system(f"gnome-terminal -e 'bash -c \"{request}; exec bash \"'")
    
    

def fill_internal_config():
    controller_dict, _ = get_config_data()
    controller_port_dict = {controller : controller_dict[controller]["port"] for controller in controller_dict.keys()}
    zookeeper_controller_port_dict = {controller : controller_dict[controller]["zookeeper_port"] for controller in controller_dict.keys()}
    
    service_config_paths = config_parser.get('DataCenter', 'service_config_paths')
    service_config_paths = service_config_paths.replace(" ", "").split(",")
    try:
        application_zookeeper_port = config_parser.get('Applications', 'application_zookeeper_port')
        zookeeper_controller_port_dict["application"] = application_zookeeper_port
    except Exception as e:
        print("application_zookeeper_port, could not be added")
    
    print("Getting data from config!")
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
            
        with open(os.path.join(path_to_dir, "storage_path"), "w") as storage_path_config:
            storage_path_config.write(os.path.join(abs_path, storage_path))
    print("Internal config setup was done!")

def get_config_data():
    # {name: }
    controller_dict = {}
    controllers = config_parser.get('Controllers', 'controller_names').replace(" ", "").split(",")
    application_zookeeper_port = config_parser.get('Applications', 'application_zookeeper_port')
    zookeeper_ports = set()
    controller_port_dict, zookeeper_controller_port_dict = {}, {}
    controller_path_dict = {}
    storage_path = ""
    for controller in controllers:
        paths_to_controller, controller_port, verbose, zookeeper, zookeeper_port = "", "", "", "", ""
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
        controller_dict[controller] = {"paths" : paths_to_controller, "zookeeper" : zookeeper, "verbose" : verbose, "zookeeper_port" : zookeeper_port, "port" : controller_port}
    return controller_dict, storage_path, application_zookeeper_port

def run_controllers():    
    controller_dict, _ = get_config_data()
        
    fill_internal_config()
    
    for controller in controller_dict.keys():
        for id, path in enumerate(controller_dict[controller]["paths"]):
            args = []
            runner_request = f"python3 {path} "
            args.append(f"python3 {path} ")
            runner_request += f"-n {id} "
            args.append(f"-n {id} ")
            if controller_dict[controller]["zookeeper"]:
                runner_request += "-z "
                args.append("-z ")
            if controller_dict[controller]["verbose"]:
                runner_request += "-v "
                args.append("-z ")

            # code snippet taken from https://stackoverflow.com/questions/7574841/open-a-terminal-from-python
            
            set_title = """function set-title() {
                            if [[ -z "$ORIG" ]]; then
                                ORIG=$PS1
                            fi
                            TITLE=\"\[\e]2;$*\a\]\"
                            PS1=${ORIG}${TITLE}
                            }"""
            os.system(f"gnome-terminal -e 'bash -c \" {runner_request}; exec bash \"'")
            print(f"Controller {path} is now running!")

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], 's')
    except getopt.GetoptError:
        print(f"ERROR by parsing args: {sys.argv}!")
    setup = False
    for opt, arg in opts:
        if opt in ('-s', '--setup'):
            setup = True
    
    if setup:
        fill_internal_config()
        try:
            setup_zookeeper()
        except Exception as e:
            print(f"Couldn't setup zookeeper! {e}")
        print("Please proceed with further instructions!")
    else:
        run_controllers()