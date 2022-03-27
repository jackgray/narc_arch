==================
Data Organization
==================



The best solution for storing, organizing, and 
interacting with data must require the following:
    - Vertical and horizontal scalability
    - Distributed accross the cluster 
    - An intuitive, no-code front-end for manipulating data and form creation
    - if possible, a sync to graph database such as neo4j

The proposed solution:
- MongoDB with a sharded configuration, and backup to MinIO storage 
- Budibase for form generation and user interaction 

Choosing the right Data Model
------------------------------
Assessing needs

Multimodal data 
    - EEG 
    - fMRI 
    - phenotypic 
    - genotypic?

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