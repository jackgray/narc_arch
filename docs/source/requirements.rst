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
4.1.    A load balancing solution must exist to efficiently distribute 

