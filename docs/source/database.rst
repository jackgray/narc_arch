==================
Data Organization
==================

The best solution for storing, organizing, and 
interacting with data should meet the following requirements: 
    -   Vertical and horizontal scalability
    -   Distributability accross the cluster 
    -   An intuitive, no-code front-end for manipulating data and form creation
    -   If possible, ability to accommodate graph models

This document will review some possible options to suit these needs.

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

Exploring the Graph Database Model 
-----------------------------------
Reference 
    https://ercim-news.ercim.eu/en125/r-i/graph-based-management-of-neuroscience-data-representation-integration-and-analysis

    https://www.researchgate.net/publication/350654192_Graph-based_Management_of_Neuroscience_Data_Representation_Integration_and_Analysis/link/606c25fd299bf13f5d5e30fc/download


MinIO S3 Select API
--------------------
Used primarily for the storage of files as opposed to tabular data, 
(i.e. MRI, EEG).

If desired, however, CSV or JSON data files can be directly queried 
using MinIO's s3 select API.

Tabular data within CSVs can be selected with SQL-like queries. For 
example, data could be aggregated accross multiple CSV files, satisfying a 
single set of conditions. 

CSV files can be easily imported to Budibase and merged with central data store. 

MariaDB, PostgreSQL, mySQL
---------------------------
If an SQL-based model is needed, Maria may be the best option for horizontal scaling; it 
features built in cluster options, growing community support, and promises 
continued long-term growth. MariaDB, PostgreSQL, and mySQL are all widely accepted 
and supported, and aren't at risk of dying out any time in the foreseeable future.

MariaDB has potential for integrating with S3 storage, but more investigating is needed to 
determine the extent of its utility.

Using the S3 Engine 
    https://www.percona.com/blog/2020/07/17/mariadb-s3-engine-implementation-and-benchmarking/

With S3 integration, audit trailing and backups may be simplified, due to MinIO's 
built-in file versioning system that allow files to be returned to previous states.

MongoDB 
---------
MongoDB is one of the leading standards for document-based database solutions. It 
is among the most mature and feature-rich, and is a great generalized solution likely 
to fit a wide range of needs. 

Mongo's shard engine allows for distributed storage of documents, making database storage more flexible.
If database storage requirements are small, however, sharding may effectively decrease access efficiency, 
so be sure to assess the long term storage needs of your data.

MongoDB access endpoint with sharding implemented: 
    https://stackoverflow.com/questions/49671158/mongodb-sharding-key

Connecting AccessDB to MongoDB
    https://www.mongodb.com/blog/post/odbc-driver-for-the-mongodb-connector-for-business-intelligence


ArrangoDB
----------

From arrangodb.com:

Advantages of Native Multi-Model
    Unlike many NoSQL databases, ArangoDB is a native multi-model database.  You can store your data as key/value pairs, graphs or documents and access any or all of your data using a single declarative query language.  You can combine different models in one query.  And, due to its native multi-model approach, you can build high performance applications and scale horizontally with all three data models.

Native vs. Layered
    Many vendors call themselves “multi-model,” but there is an important difference between adding a graph layer to say a key/value or document store and ArangoDB’s native multi-mode approach.

    With ArangoDB, using the same core and the same query language for all data models, users can combine different models and features in a single query. ArangoDB doesn’t “switch” between models behind the scenes and it doesn’t shovel data from A to B in order to execute queries.  This gives ArangoDB stronger performance advantages when compared to the “layered” approaches.

    For more information on performance, see High Performance with ArangoDB.

When to use ArangoDB
    Native multi-model databases shine particularly in three situations:

    Staying flexible in developing new ideas
        In situations when developing a new product or service, you might not know all your requirements for at the outset. Changes in your product or the need for new features can lead to changes in your data model.With a multi-model database, you are able to easily react to those changes. You can apply your knowledge of one technology to several use cases and requirements.No need to learn a new technology or build a new tech-stack.

    Developing software as a team
        ArangoDB enables teams to cooperate across use cases. For instance, one team starts work on an application that requires a Document database. In the course of development, members of this team learns tips and tricks about the usage of ArangoDB. Another team begins work on a Graph database.Both teams can exchange their experience with ArangoDB and optimize their usage. This shortens the learning curve, deepens teamwork and reduces the time to get your solutions live.

    Combining different data models in one query
        No need to build two or three tech-stacks to support your application. These create risky connections between different single-model databases. Instead, ArangoDB is designed it easier to develop modular applications.

Advantages of ArangoDB
    Consolidation
        As a native multi-model database, ArangoDB minimizes the components that you need to maintain, reducing the complexity of the technology stack for your application or usage. This means a lower total cost of ownership, increasing flexibility and consolidating your overall technical needs.

    Simplified Performance Scaling
        Applications grow and mature over time. With ArangoDB, you can easily react to growing performance and storage needs by independently scaling with different data models. ArangoDB scales both vertically and horizontally, and if your performance needs decrease, you can just as easily scale down your back-end system to save on hardware and operational requirements.

    Reduced Operational Complexity
        In the concept of Polyglot Persistence, the goal is to use the best tools for whatever jobs you may have. When working with single-model databases, this can lead to various operational challenges. Certain tasks require a document database, while others require a graph database. Integrating them is a complex task in itself, but creating a large cohesive system with data consistency and fault tolerance between separate, unrelated database systems may prove impossible.

        Polyglot Persistence is about choosing the right data model for the right job. A native multi-model database allows you to have polyglot data without the complexity, but with data consistency on a fault tolerant system. With ArangoDB, you can use the right data model for the right job.

    Strong Data Consistency
        When using multiple single-model databases, data consistency becomes an issue. These databases aren’t meant to talk to each other, which means you need to implement some form of transaction functionality to keep your data consistent between different models.

        With ArangoDB, a single back-end manages your different data models with support for ACID transactions. ArangoDB provides strong consistency on a single instance and atomic operations when operating in cluster mode.

    Fault Tolerance
        Building fault tolerant systems with many unrelated components is a challenging task in itself. When working with clusters, this grows even more difficult. Deploying and maintaining such systems requires deep expertise of several different technologies and technology stacks. Moreover, bringing together multiple subsystems that were designed to run independently imposes significant engineering and operational costs.

        The solution to these challenges is a multi-model database and a consolidated technology stack. By design, ArangoDB enables modern, modular architectures with different data models running and works for cluster usage as well.

    Lower Total Cost of Ownership
        Each database technology you use needs ongoing maintenance, patches, bug fixes and other modifications delivered by the vendor. Each new update has to be tested by a specialized team member and tested for their overall fit into the current system.  Using a multi-model database significantly reduces these maintenance costs as it allows you to reduce the number of database technologies you need for your application.

    Transactions
        It is a real challenge to provide transactional guarantees across multiple machines and few NoSQL database provide these guarantees. As a native multi-model database, ArangoDB requires transactions to ensure data consistency.  ArangoDB provides strong consistency on single instances and atomic single document operations when running in cluster mode.

Consuming data in Python:
    https://github.com/ArangoDB-Community/python-arango


Backing Up
-----------
For a data storage solution to be robust and reliable, it must be backed up accross 
multiple sources and allow for multiple concurrent points of failure.

Data should have a single source of truth, but exist in 
multiple places.

By using MinIO as a single storage entity, data backups can be 
orchestrated from a single source. Different data targets can have 
their own backup policy, so relatively light document databases can 
be replicated across multiple cloud services for very little cost. 


Audit Trailing
---------------
It's nice to have a history of how your data changes, so you can 
better trust in its accuracy. 

For document-based databases, this feature is not directly built-in 
for free, but there are some design patterns that can be used to create 
this effect, like schema versioning, and document versioning patterns.

https://www.mongodb.com/blog/post/building-with-patterns-the-schema-versioning-pattern

https://www.mongodb.com/blog/post/building-with-patterns-the-document-versioning-pattern


There are also paid enterprise editions of many database 
cloud providers that offer this feature.

https://www.mongodb.com/docs/manual/core/auditing/

https://www.arangodb.com/docs/stable/security-auditing-audit-events.html