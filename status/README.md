this folder is used to monitor the status of nodes. 
This main idea is that:
1. Send interest to specific NFD prefix to fetch notifications. 
2. Check the changes in these notifications.
3. If changes happened, no notify the node to send new version HelloReq message.  So that the controller could know the changes had happened and fetch the node's new feature.

*Since the notification info is encoded using google protobuffer structure, the '.proto' files are require to decode this notification.
*It can monitor "channels", "faces", "FIB", "RIB".  
