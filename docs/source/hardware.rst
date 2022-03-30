=====================
Hardware Requirements
=====================

Networking
-----------
Router
    The router must support enough bandwidth to keep up with the 
    processing power of the cluster. 


Wireless
    Check with institute on broadcasting VPNs. 

    Port forwarding to make endpoints publically available could be handled in-house, 
    or by the institute.



Hot Storage
------------
Fast access- for actively or commonly used files 
More expensive

-   NVMe 
-   SSD 
-   Cloud


Cold Storage
------------
Slower retrieval- for backups, hot overflow, or less used files.
Cheaper

-   Hard Disk Drives
-   Whatever is lying around 
-   Cloud (less expensive)

Cloud Overfill
-----------------

The backup policy should be such that data past a certain age is automatically converted 
to cold storage, and in emergency situations where space runs out, automatically uploaded 
to external cloud service. 

Full snapshots of the entire system should always be backed up to at least one off-site 
provider.

Compute
---------
Metrics on compute loads to go here 
