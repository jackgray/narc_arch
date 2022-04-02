==========================
System Requirements
==========================

The system must provide certain features in some form or another. This 
page is not concerned with how any of those features are implemented, but 
rather aims to outline the desired features themselves, 
and serve as a reference throughout the design process. 

1.  Replication
----------------
*All* files and data should be replicated in at least one other separate location. 
**1.1** Database Replication 
    :1.1.1: When space allows, the database should be fully replicated on each of the nodes, so that if one of the nodes go down or is corrupted, data can be accessed without interruption through any of the other nodes. 
    
    :1.1.2: Daily snapshots of the database should be backed up to the core file storage, which should contain a policy for back-up to an off-site cloud provider 

**1.2** Filesystem Replication
    :1.2.1: Copies of all files stored by the lab should exist in more than one physical location.

2.  Scalability 
----------------
Each component throughout the entire system should be able 
to expand with the needs of the lab without any redesign 
of infrastructure. 

**2.1** Storage Expansion 
    :2.1.1: Storage should be infinitely expandable without demanding changes in configuration
    
**2.2** Computational Expansion
    :2.2.1: The cluster should be able to accept new nodes without serious overhead or reconfiguration of other nodes. 

**2.3** Database Scalability
    :2.3.1: The database should have a  distributed model, where it is stored accross multiple nodes, to avoid potential interruptions or major intervention when the data fills up a drive.

3.  Accessibility
------------------
Commonly used resources from the computing system must be able to 
be accessed and utilized without specialized knowledge. 

**3.1.**    Data Accessibility
    :3.1.1: Tabular data from the underlying core database must have a graphical access client that does not require specialized knowledge to use.
    
    :3.1.2: Data that is acquired by digital forms must be automatically stored into the core database without user initiation or intervention.

**3.2** File Accessibility
    :3.2.1: End users must have a convenient means of accessing files stored on the main server. The solution should be seamless and feel like a normal folder to the user.

4.  Resource Efficiency
-------------------------
System resources must be considerately assigned to system processes in 
order to maximize their efficiency. This usually involves distributing 
tasks, files, and data accross multiple nodes.

**4.1.**    Load balancing 
    :4.1.1: Ingress routing must be implemented to efficiently distribute server requests across all available resources

**4.2**     Distributed File Storage 
    :4.2.1: Files should be stored in a distributed filesystem, such as Hadoop (HDFS) or S3 (Amazon, MinIO, Azure Blob)

5.  Form Generation 
---------------------
A means of creating forms and storing entries into the core database must exist. 

6.  Audit Trailing 
--------------------

7.  Monitoring 
---------------
There must be a means of monitoring the consumption of resources. 

**7.1** Graphical dashboard 

    :7.1.1: The cluster must provide a method for displaying breakdowns of 
    all consumed resources. 
    