==================
Data Organization
==================

The best solution for storing, organizing, and 
interacting with data should include the following:
    -   Vertical and horizontal scalability
    -   Distributability accross the cluster 
    -   An intuitive, no-code front-end for manipulating data and form creation
    -   If possible, ability to sync relational database to graph database such as neo4j

The proposed solution:
-   MongoDB with a sharded configuration, and automatic snapshot backup to MinIO storage 
-   Budibase for form generation and user interaction 

Choosing the right Data Model
------------------------------
Assessing needs

Multimodal data 
    -   EEG 
        -   interacts with: (?)
        -   Average file size: (?)
    -   fMRI 
        -   Interacts with: (?)
        -   Average file size: (?)
    -   Phenotypic 
    -   Genotypic?

How many datapoints per subject?

How many relations? 

Is the goal to discover relationships, or to simply quantify the 
extent of previously known relationships?
    Graph database models can aid in the discovery of relationships 
in a dataset.

Exploring the Graph DB Model 
-----------------------------
Reading Links
    https://ercim-news.ercim.eu/en125/r-i/graph-based-management-of-neuroscience-data-representation-integration-and-analysis

    https://www.researchgate.net/publication/350654192_Graph-based_Management_of_Neuroscience_Data_Representation_Integration_and_Analysis/link/606c25fd299bf13f5d5e30fc/download


MinIO S3 Object-based Storage
----------------------------
Used primarily for the storage of files as opposed to tabular data, 
(i.e. MRI, EEG), but MinIO's s3 select API allows data to be manipulated 
directly or consumed automatically by custom scripts or pipelines.

Tabular data within CSVs can even be selected with SQL-like queries. For 
example, data could be aggregated accross multiple CSV files, satisfying a 
single set of conditions. 

CSV files can be easily imported to Budibase and merged with central MongoDB 
(or whatever is desired) store. 


MariaDB
--------
-   Possible solution for distributed SQL

Using the S3 Engine 
    https://www.percona.com/blog/2020/07/17/mariadb-s3-engine-implementation-and-benchmarking/

Spark Storage
--------------

Postgres Server 
----------------

MongoDB Shard (Distributed DB)
-------------------------------
Some notes: https://stackoverflow.com/questions/49671158/mongodb-sharding-key

Connecting to BudiBase
    https://www.percona.com/blog/2020/07/17/mariadb-s3-engine-implementation-and-benchmarking/

