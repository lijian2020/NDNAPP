#!/usr/bin/python3
#
# Copyright (C) 2019 Trinity College of Dublin, the University of Dublin.
# Copyright (c) 2019 Li Jian
# Author: Li Jian <lij12@tcd.ie>

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# Project Description:
# This project is created by Li Jian for his master degree dissertation project, 
# which is an OpenFlow Implementation over Named-Data Networking. In this project, 
# a new designed OpenFlow SDN is designed to run over NDN and to offer control-plane
# for NDN nodes. 

# In this application, there are several main components, and all of these components
# can run on NDN nodes, specifically on the nodes of Minindn simulator. All of these 
# components are written in Python3.6. 
# Controller.py  is the main component used as a OF-SDN controller, which needs only  
# one node to run it.
# Node.py is the other main component which should be running on all other NDN nodes. 
# It is used to monitor the status of NDN nodes and to communicate with the controller.
# It also has the ability to configure the nodes.

# There are other two components used for test, testproducer.py and testconsumer.py. 
# They are just used to send 'Interest' and response it with 'Data'.  

# This application is also based on adjusted Minindn simulator, which means that if 
# if you want to the full function of this application, the Minindn simulator environment
# needs to adjust.  The modification has been described in Li Jian's dissertation paper 
# in detail. 

# Because of the limitation of time, this application may include some imperfections or errors,
# The author will be very grateful to you for pointing out of these mistakes. The author's 
# email address has been listed in the front of this page.
