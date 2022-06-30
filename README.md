# sys-micro-fractos-mock
## Overview
A FractOS mock imitates a distributed system for decentralized appliactions following the proposed by FractOS design. 
Our mock system nodes are an abstraction of hardware, e.g., a storage node represents an SSD, and computational nodes act as CPU/GPU.
We use ZooKeeper to maintain large set of hosts and coordinate among them.
Each node represents the following structure:
![node model][node_model] \
Our system consists of application, storage, math and convolutional neural network nodes. Hence, using the above representation we can model our system this way: \
![system model][sys_model] \

## Table of content
- [Setup](#-setup)
- [Configuration](#-configuration)
- [Demo](#-demo)
- [Research paper](#-research-paper)
## Setup
Here is a checklist of dependencies to get this project up and running on your system:
* Install python3 to your system.
[Installation & setup guide](https://realpython.com/installing-python/)
* Install dependencies.
  ```
  python3 -m pip install grpcio grpcio-tools tensorflow kazoo
  ```
* Clone repository.
  ```
  git clone https://github.com/Voltorane/sys-micro-fractos-mock.git
  ```
* Do something

## Demo
Here we will walk you through the workflow of this program, mainly how to run a convolutional neural network application in the proposed system.
## Research paper
Our [TODO: research paper]() describes the design of our mock system as well as the design of initial reference system - FractOS.

[node_model]: resources/node_model.png
[sys_model]: resources/sys_model.png
