========================
Pipeline Orchestration
========================

Kubernetes
-------------
The brain of the cluster. All service installations should be done through Kubernetes 
and utilize its ingress controller for cohesive load balancing of services and efficient 
distribution of computational resources.
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
    -   Can automate more things than Budibase

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

Pre-packaged Solutions
----------------------

IBM Spectrum LSF
    A way to simplify management and maintenance of HPC Cluster 
    is to go with a pre-packaged and professionally maintained 
    all-in-one solution.

    Future admins would not need to be Kubernetes experts.

    "The IBM Spectrum LSF ("LSF", short for load sharing facility) software is 
    industry-leading enterprise-class software. LSF distributes work across 
    existing heterogeneous IT resources to create a shared, scalable, and 
    fault-tolerant infrastructure, that delivers faster, more reliable workload 
    performance and reduces cost. LSF balances load and allocates resources, 
    and provides access to those resources.

    LSF provides a resource management framework that takes your job requirements, 
    finds the best resources to run the job, and monitors its progress. Jobs always 
    run according to host load and site policies."

    https://www.ibm.com/docs/en/spectrum-lsf/10.1.0?topic=overview-lsf-introduction
    https://www.ibm.com/products/hpc-workload-management

    Pricing?

Cloudera CDP Private Cloud 

    Another all-in-one solution 

    Reading:
        https://www.forbes.com/sites/patrickmoorhead/2021/05/03/clouderas-data-platform-private-and-public-cloud-both-ga-and-its-time-to-migrate/?sh=46c1e6c72801

    -   Out of the box
    -   Hybrid
    -   Less configuration and management
        -   Fewer points of failure
        -   Frees up resources 
    -   Explore multiple configurations of products without having 
    to learn all of them

    Reliant on paid service. Analysis should be performed to 
    assess annual cost of service and 