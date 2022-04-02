==========================
System Requirements
==========================

The system must provide certain features in some form or another. This 
page is not concerned with how any of those features are implemented, but 
rather aims to outline the desired features themselves, 
and serve as a reference throughout the design process. 

1.  Replication
----------------
*All* data should be replicated in at least one other separate location. 

2.  Scalability 
----------------
Each component throughout the entire system should be able 
to expand with the needs of the lab without any redesign 
of infrastructure. 

**2.1** Storage 
    :2.1.1: Storage should be infinitely expandable without demanding changes in configuration
    
**2.2** Computation 
    :2.2.1: The cluster should be able to accept new nodes without serious overhead or reconfiguration of other nodes. 

**2.3** Database
    :2.3.1: The database should have a  distributed model, where it is stored accross multiple nodes, to avoid potential interruptions or major intervention when the data fills up a drive.

3.  Accessibility
------------------
Commonly used resources from the computing system must be able to 
be accessed and utilized without specialized knowledge. 

3.1.    Data Accessibility
    :3.1.1: Tabular data from the underlying core database must have a graphical access client that does not require specialized knowledge to use.
    
    :3.1.2: Data that is acquired by digital forms must be automatically stored 
    into the core db without user initiation or intervention.

4.  Resource Efficiency
-------------------------
System resources must be considerately assigned to system processes in 
order to maximize their efficiency. This usually involves distributing 
tasks, files, and data accross multiple nodes.

**4.1.**    A load balancing solution must exist to efficiently distribute compute 
requests accross all available resources

**4.2**     File storage should be distributed