===========
Storage
===========

An ideal storage solution is expandable, dependible, secure,  
easy to access, and easy to manage. These will require some kind 
of distributed storage solution, allocation management, a 
comprehensive backup strategy, a key management system (KMS), 
and a means of accessing the files remotely.

S3 Buckets with Min.io
---------------------------------------
Built on the same concept as Amazon's S3 bucket storage, MinIO 
makes infinitely scalable clustered data storage available on-premise. 
It integrates seamlessly with other cloud providers for instant 
expansion when necessary, allowing time to increase hardware 
storage if desired, without loss of service.

It runs on Kubernetes, can utilize its central key management 
system (KMS) for authentication, providing zero-knowledge 
encryption during transfer, and at rest, and can be interacted 
with using both POSIX-flavored and aws's s3-select commands alike.

Feature Summary:
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
            -   drive parity set to maximum of 8 would allow for half of the 
            drives to fail at once, without any loss of data 
            -   on any drive failure, the missing data chunks are rebuilt automatically, 
            giving the admin time to replace the failed drives.
            -   when failed drives are replaced, the recovered data is automatically 
            backed up to return to previous state
   

Installation
    https://docs.min.io/docs/deploy-minio-on-kubernetes


Personal PC Integration with O-Drive
----------------------------------------------
O-Drive makes file access to multiple storage sources, including MinIO 
seamless to a personal computer, appearing as a regular folder. Think 
DropBox or OneDrive, but custom-fitted and on-premise. You can even 
add any of your existing cloud storage services into the mix, syncing and organizing them 
centrally through O-Drive. 

O-Drive offers zero-knowledge server connection to the file store. 
Once set up on a personal computer, folders on the server 
will look like any other local folder on your computer. 

Reverse-sync local folders to server.

This marriage between server and personal computer enables the system to 
maintain a single source of truth for all lab files, without 
requiring users to ssh to the file server and download data that 
they may want to interact with locally.

Here's some more info from odrive:

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
    -   Directly connected to central cluster file storage
    -   Tracks changes to files and retains previous versions   
    -   See files on database without downloading them locally 
    -   Integrate external cloud drives, such as OneDrive, Dropbox, 
    Google Drive, etc. 

(https://odrive.com/)

Fault Tolerability & Disaster Recovery
---------------------------------------
To support a truly fault tolerant system, every component must be 
fault-tolerant. The cluster storage solution should be able to 
handle multiple concurrent drive failures without loss of data 
or interuption of service. Additionally, data should be replicated 
off-site to protect against location related failures, such as 
power outage, flood, fire, A/C failure electric surge, etc.

Fortunately, MinIO makes mitigating such failures fairly easy with its 
Erasure Code, Bucket Replication, and Tiering features.

Erasure Coding 
    "MinIO Erasure Coding is a data redundancy and availability feature 
    that allows MinIO deployments to automatically reconstruct objects 
    on-the-fly despite the loss of multiple drives or nodes in the cluster. 
    Erasure Coding provides object-level healing with less overhead than 
    adjacent technologies such as RAID or replication.

    MinIO splits each new object into data and parity blocks, where 
    parity blocks support reconstruction of missing or corrupted data 
    blocks. MinIO writes these blocks to a single erasure set in the 
    deployment. Since erasure set drives are striped across the deployment, 
    a given node typically contains only a portion of data or parity blocks 
    for each object. MinIO can therefore tolerate the loss of multiple 
    drives or nodes in the deployment depending on the configured parity 
    and deployment topology."
    -   https://docs.min.io/minio/baremetal/concepts/erasure-coding.html#minio-erasure-coding

Bucket Replication
    For some projects, it might be desirable to share data between 
    teams accross labs or sites. Bucket replication can allow a 
    two-way syncronization between buckets on disparate systems. 
    This means data that is collected or artifacts that are processed
    by one team are immediately available to the other teams. Each 
    site can have their own erasure code configurations, increasing 
    the integrity of the data for each replication.

    "Configure per-bucket rules for automatically synchronizing 
    objects between buckets within the same MinIO cluster or 
    between two independent MinIO Clusters. MinIO applies rules 
    as part of object write operations and automatically 
    synchronizes any changes to filesystem.

    Synchronize objects between buckets 
    within the same S3-compatible cluster or between two independent 
    S3-compatible clusters. Client-side replication using mc mirror 
    supports MinIO-to-S3 and similar replication configurations.

    MinIO server-side bucket replication is functionally similar 
    to Amazon S3 replication while adding the following MinIO-only 
    features:
    -   Source and destination bucket names can match, supporting 
    site-to-site use cases such as Splunk or Veeam BC/DR.
    -   Simplified implementation than S3 bucket replication 
    configuration, removing the need to configure settings like 
    -   AccessControlTranslation, Metrics, and SourceSelectionCriteria.
    -   Active-Active (Two-Way) replication of objects between source 
    and destination buckets. Multi-Site replication of objects 
    between three or more MinIO deployments."

    -   https://docs.min.io/minio/baremetal/replication/replication-overview.html

Object Transition (Tiering)
    "MinIO supports creating object transition lifecycle management 
    rules, where MinIO can automatically move an object to a remote 
    storage “tier”. MinIO supports any S3-compatible service as a 
    remote tier in addition to the following public cloud storage 
    services:
    -   Amazon S3
    -   Google Cloud Storage
    -   Microsoft Azure Blob Storage
    -   MinIO object transition supports use cases like moving aged 
    data from MinIO clusters in private or public cloud infrastructure 
    to low-cost private or public cloud storage solutions. MinIO 
    manages retrieving tiered objects on-the-fly without any additional 
    application-side logic.

    Use the mc admin tier command to create a remote target for 
    tiering data to a supported Cloud Service Provider object storage. 
    You can then use the mc ilm add --transition-days command to 
    transition objects to the remote tier after a specified number 
    of calendar days.

    -   https://docs.min.io/minio/baremetal/lifecycle-management/lifecycle-management-overview.html#minio-lifecycle-management-tiering