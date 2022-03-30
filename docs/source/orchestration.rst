========================
Pipeline Orchestration
========================

Kubernetes
-------------
-   Manages Cluster
-   Provides DNS routing for all services
-   Load Balancing 
-   Environment for running containers (i.e. Docker)


Concourse-CI
-------------
Generalized pipeline orchestrator/scheduler
    -   Glues together containers and scripts to create complex workflows
    -   "General purpose thing-doer"

References
    https://medium.com/concourse-ci/concourse-pipeline-ui-explained-87dfeea83553

Load Balancing

DNS Autoscaling

AirFlow
--------
Graphical workflow manager for cloud data services.

Advantages over Budibase or Concourse
    -   Smaller learning curve than Concourse 

Disadvantages 
    -   Geared for cloud- may not be ideal for hybrid model 
    -   A good workflow manager should traverse the cloud and bare-metal seamlessly

SLURM
------
The standard for large scale HPC resource services. 

It is self-contained with its own job management, 
cluster management, and load balancing engines.

Pros
    -   More granular control of jobs
    -   Can convert and run most Docker containers 
    -   Convenient for central resource sharing between disparate 
        groups; (namespacing and auth isolation)

Cons 
    -   Additional point of failure with containerization conversion for using 
        Docker containers.
    -   Docker is the standard; offers more plug-and-play pipelines.
    -   No Kubernetes integration - could create complications with resource 
        management (having multiple independent clusters with isolated load balancing )
    -   Not as conducive for complicated, automatically triggered 
        pipelines where integration of modern technology is desired 

Possible Solutions:
   
    -   Investigate possibility of managing multiple clusters under a  
        secondary load balancing service. 
    -   Investigate what is required to route SLURM resources to a custom endpoint 

ArgoCD
------
Simple solution for continuous deployment of apps

Launch updates that self-revert on failure.