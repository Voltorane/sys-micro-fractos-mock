# sys-micro-fractos-mock

IMPORTANT! This is not final release! Demonstration video and further setup instructions will come by 5.06.2022!
We beg for your patience!

## Overview
A FractOS mock imitates a distributed system for decentralized appliactions following the proposed by FractOS design. 
Our mock system nodes are an abstraction of hardware, e.g., a storage node represents an SSD, and computational nodes act as CPU/GPU.
We use ZooKeeper to maintain large set of hosts and coordinate among them.
Each node represents the following structure:
![node model][node_model] \
Our system consists of application, storage, math and convolutional neural network nodes. Hence, using the above representation we can model our system this way: \
![system model][sys_model] \
Our implementation already contains a configuration file, that you may modify depending on your needs.

##### The implementation consists of around 2.5k LoC

## Table of content
- [Setup](#-setup)
- [Demo](#-demo)
- [Research paper](#-research-paper)
## Setup
* ### Install python3 to your system
[Installation & setup guide](https://realpython.com/installing-python/)
* ### Clone repository
  ```
  $ git clone https://github.com/Voltorane/sys-micro-fractos-mock.git
  ```
* ### Install dependencies
  ```
  $ python3 -m pip install -r requirements.txt
  ```
* ### Install ZooKeeper
  ```
  $ wget https://dlcdn.apache.org/zookeeper/zookeeper-3.7.1/apache-zookeeper-3.7.1-bin.tar.gz
  $ tar -xf apache-zookeeper-3.7.1-bin.tar.gz
  ```
* ### (opt.) Install Training dataset for Convolutional Neural Network node
  If you want to have a CNN node in your dataset (required by default setup) you need to provide training data into the Services/ComputationalNodes/CNN/Node/TrainingData.
  In the example application we use Dogs and Cats classification, but you can use any binary classification data.
  ```
  $ wget https://download.microsoft.com/download/3/E/1/3E1C3F21-ECDB-4869-8368-6DEBA77B919F/kagglecatsanddogs_5340.zip -P Services/ComputationalNodes/CNN/Node/TrainingData
  $ unzip Services/ComputationalNodes/CNN/Node/TrainingData/kagglecatsanddogs_5340.zip -d Services/ComputationalNodes/CNN/Node/TrainingData
  $ mv Services/ComputationalNodes/CNN/Node/TrainingData/PetImages/Cat Services/ComputationalNodes/CNN/Node/TrainingData/Cat ;
    mv Services/ComputationalNodes/CNN/Node/TrainingData/PetImages/Dog Services/ComputationalNodes/CNN/Node/TrainingData/Dog ;
    rm -R Services/ComputationalNodes/CNN/Node/TrainingData/PetImages
  ```

* ### Setup config
  The config is ready for the demonstration and you need to change it only if you want to add some new nodes. \
  The data_center_setup.cfg config has the following layout:
    ```
    # this section is required for setting up the connection for gRPC and setup all configs
    # change it only if you change the config paths
    [DataCenter]
    # ip for internal communication between all controllers
    grpc_ip = 127.0.0.1
    # internal config folders (usually Services/config but can be also in different places)
    service_config_paths = Services/config
    # in this section you should give all names of the controllers, that you will use in the datacenter
    [Controllers]
    controller_names = cnn_controller, math_controller, application_controller, storage_controller
    # ----------------------------------------------------------------------
    # create config with controller name for every controller you want to configure
    [cnn_controller]
    # you can give multiple comma-separated paths to the same controller, to make the best use of the zookeeper
    paths_to_controller = Services/ComputationalNodes/CNN/CNN_Controller/cnn_controller.py
    # print output in the terminal
    verbose = True
    # run with zookeeper
    zookeeper = True
    # ----------------------------------------------------------------------
    ...
    ```
  All ports are dynamically selected, so you shall not worry about them anymore :)
* ### Setup data center
  If you don't want to connect ZooKeeper to your data center, you can skip this step and directly run data center! \
  This step is needed to initialize all ZooKeeper directories and configs.
  ```
  $ python3 run_datacenter.py (-s|--setup)
  ```
* ### Run ZooKeeper for each node
  After last step, the "zookeeper" folder should have appeared. In order to start each ZooKeeper, you should go to each ZooKeeper's bin folder (i.e. zookeeper/zookeeper0/bin, zookeeper/zookeeper1/bin, ...) and start it manually (We didn't find a way to automatize it :(... )
  ```
  $ cd zookeeper/zookeeper0/bin
  $ ./zkServer.sh start
  # go back to the sys-micro-fractos-mock
  $ cd zookeeper/zookeeper1/bin
  $ ./zkServer.sh start
  ...
  ```
  If you got the following message for each of your ZooKeepers - you are ready for running the data center!
  ```
  /usr/bin/java
  ZooKeeper JMX enabled by default
  Using config: path/to/sys-micro-fractos-mock/zookeeper/zookeeper(0/1/...)bin/../conf/zoo.cfg
  Starting zookeeper ... STARTED
  ```
* ### Run data center
  #### **Via run_datacenter.py (Linux with gnome-terminal)**
  ```
  $ python3 run_datacenter.py
  ```
  This will create separate terminal for each of the nodes
  #### **Manually (Mac & Linux)**
  For each node you want in the data center, you need to start its controller:
  ```
  $ python3 path/to/controller/controller_name.py [-n <name>|--name=<name>] [-v|--verbose] [-z|--zookeeper]
  ```
  Example for Storage Node with ZooKeeper and with output in terminal:
  ```
  $ python3 Services/StorageNode/Storage_Controller/storage_controller.py -v -z
  ``` 
* ### Run Applications
  After you have started the data center, you are ready to run your applications.\
  You can either run applications, that we have already prepared, or write your own, using the template in Applications/application_template.py. \
  Example:
  ```
  $ python3 Applications/image_prediction_application.py
  ```   

## Demo
Here we will walk you through the workflow of this program, mainly how to run a convolutional neural network application in the proposed system.
## Research paper
Our [research paper] describes the design of our mock system as well as the design of initial reference system - FractOS.

[node_model]: resources/node_model.png
[sys_model]: resources/sys_model.png
[research paper]: resources/report.pdf
