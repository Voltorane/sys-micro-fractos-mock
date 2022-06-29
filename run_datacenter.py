import os
from configparser import ConfigParser

config_path = "data_center_setup.cnf"

def run_controllers():
    config_parser = ConfigParser()   
    config_parser.read(config_path)
    
    controllers = config_parser.get('Controllers', 'controller_names')
    controllers = controllers.replace(" ", "").split(",")
    for controller in controllers:
        paths_to_controller, servers, controller_port, verbose, zookeeper, zookeeper_port = "", "", "", "", "", ""
        try:
            paths_to_controller = config_parser.get(controller, "paths_to_controller")
            paths_to_controller = paths_to_controller.replace(" ", "").split(",")
        except:
            # can't run controller without path
            continue
        # amount of servers
        try:
            servers = config_parser.get(controller, "servers")
        except:
            pass
        # port on which the controller will run
        try:
            controller_port = config_parser.get(controller, "controller_port")
        except:
            pass
        # print output in the terminal
        try:
            verbose = bool(config_parser.get(controller, "verbose"))
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
        except:
            pass
        
        for path in paths_to_controller:
            runner_request = f"python3 {path} "
            if servers != "":
                runner_request += f"-s {servers} "
            if zookeeper:
                runner_request += f"-z "
            if verbose:
                runner_request += f"-v "
        
            os.system(f"gnome-terminal -e 'bash -c \"{runner_request}; exec bash \"'")
            print(paths_to_controller, servers, controller_port, verbose, zookeeper, zookeeper_port)

if __name__ == "__main__":
    run_controllers()