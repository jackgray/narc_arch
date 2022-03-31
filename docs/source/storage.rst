===========
Storage
===========

The storage solution will consist of a primary (hot) distributed system
with 100% fault tolerance, a cold storage hybrid cloud for emergency overflow 
and secure offsite backup, a rolling backup policy to move files as the drive 
fills into the cold storage, and a graphical user interface (frontend client) 
to seamlessly access the data with little additional technical knowledge required.

Distributed Object Storage with Min.io
---------------------------------------
Main file store for any and everything. Automatically backed up 
and encrypted, seamless integration with Kubernetes and personal 
desktops (see section on O-drive).

S3 Object-based Storage: Open source, on-premise S3 buckets.
    -   Infinitely scalable 
    -   Universally consumable 
    -   Uses aws s3 api 
    -   Query tool (s3-select) based on SQL 
    -   Integrates seamlessly with multiple cloud 
        storage providers
    -   Zero-knowledge encryption in transport and at rest 
    -   More efficient storage process enables faster 
        data-retrieval
    -   Easily automate backups to cheaper cold storage based 
        on wide option of rules, such as age or last access date 
         -   Automatically transfer oldest files to backup storage if drives 
        overfill 
    -   Store references of cold-stored files on system alongside 
        on-premise files.
    -   Fault tolerant 
        -   easily add more drives 
        and re-adjust percent drive failure allowance on the fly. 
        -   Example: 
            -   a cluster with 8 nodes
            -   each node has 2 1TB drives
            -   total of 16 drives => 16TB of data
            -   drive parity set to maximum of 8 would allow for 8 drives 
            to fail at once, without any loss of data 
            -   on any drive failure, the missing data chunks are rebuilt automatically, 
            giving the admin time to replace the failed drives.
            -   when failed drives are replaced, the recovered data is automatically 
            backed up to return to previous state
   

Installation
    https://docs.min.io/docs/deploy-minio-on-kubernetes


Personal PC Integration with O-Drive
----------------------------------------------
Seamless integration between primary distributed storage 
(Min.io server) and local computers. 

Think DropBox or OneDrive, but custom-fitted, on-premise, 
single source compatible.
    -   Combine from multiple cloud service providers 

Zero-knowledge server connection
    -   Once set up on a personal computer, folders on the server 
    will look like any other local folder.

Reverse-sync local folders to server.

Reference 
    https://odrive.com/

From odrive:

Sync unlimited data
    odrive's Infinite Sync shows files available in your storage 
    initially as placeholder cloud files that don't take up any 
    disk space on your computer. Content isn't downloaded until 
    you try to access the file. This saves bandwidth and allows 
    you to sync storage with more data in it than you have hard 
    disk capacity.

Back up important files to any storage
    You can back up any folder on your computer to any storage 
    that you've linked to odrive. Backup automatically keep older 
    versions of files that have been updated or deleted since the 
    last backup run, protecting your data against loss. 

Connect your machines
    You can install the odrive sync app (or lightweight command 
    line sync agent) on unlimited machines. Make it easy to work 
    seamlessly across all of your computers. You can even easily 
    connect your virtual machines to all of your storage by installing 
    odrive and logging in with your odrive account, enabling a whole 
    new world of possibilities. 

Advantages
    -   Free 
    -   Seamless integration with MinIO and Kubernetes 
    -   Additional layer of data permanence and revertability 
    -   Removes risk of data merge conflicts
    -   On-premise solution is free 
    -   Expand storage to cloud 
    -   Directly connected to main cluster object store
    -   Tracks changes to files and retains previous versions   
    -   See files on database without downloading them locally 
    -   Integrate external cloud drives, such as OneDrive, Dropbox, 
        Google Drive, etc. 