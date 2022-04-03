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
Concourse is the conductor. It looks for trigger events, like say, 
artifacts from a Docker service that checks 
XNAT for new exams to download, and then can launch any number of 
processes from there. The artifacts can be passed as the input(s) 
for other services. For instance, a change to the session manifest 
for a project triggers another Docker service that 
downloads and organizes the data, the successful completion of which
could trigger yet another event, such as fmriprep, with artifacts  
being passed to any further stages. Notifications via Slack, Email, etc. 
can be seamlessly added for any event.



References
    https://medium.com/concourse-ci/concourse-pipeline-ui-explained-87dfeea83553

Load Balancing
    Load balancing is the active monitoring of 

DNS Autoscaling

AirFlow
--------
Graphical workflow manager geared toward cloud services.

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

SLURM seams to be best for large institutes to provide and manage resources 
for potentially over a thousand users. If you want granular control over when and how 
you submit jobs, or you don't have the resources to create fully hands-off pipelines for 
every user of the cluster), SLURM is good. If both your data and analysis processes are 
uniform, and you have the resources to create complete hands-off pipelines for each 
user, SLURM is less ideal. 

The latter is an ambitious concept, but the direction data processing seems to be headed.

It may be possible to integrate calls to an external SLURM cluster (i.e. one provided 
by the institute, possibly at a discount) into the primary pipeline system.


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
   
    Advantages
        -   Out of the box
        -   Hybrid
        -   Less configuration and management
            -   Fewer points of failure
            -   Frees up resources 
        -   Explore multiple configurations of products without having 
        to learn all of them

    Disadvantages 
        Reliant on paid service. Analysis should be performed to 
        assess annual cost of service and 

CloudLab 
-----------
https://cloudlab.us/index.php

A product of NSFCloud Program https://www.nsf.gov/pubs/2013/nsf13602/nsf13602.htm

"Build Your Own Cloud
    CloudLab provides researchers with control and visibility all the way 
    down to the bare metal. Provisioning an entire cloud inside of CloudLab 
    takes only minutes. Most CloudLab resources provide hard isolation from 
    other users, so it can support hundreds of simultaneous "slices", with 
    each getting an artifact-free environment suitable for scientific 
    experimentation with new cloud architectures. Run standard cloud software 
    stacks such as OpenStack, Hadoop, and Kubernetes. Or, build your own from 
    the ground up. The bare metal's the limit!

    CloudLab is built from the software technologies that make up Emulab and 
    parts of GENI, so it provides a familiar, consistent interface for 
    researchers.

On Our Hardware
    The CloudLab clusters have almost 1,000 machines distributed across three 
    sites around the United States: Utah, Wisconsin, and South Carolina. In 
    addition, it provides access to a number of federated facilities around and 
    outside of the US. CloudLab is interconnected with nationwide and 
    international infrastructure from Internet2, so it is possible to extend 
    private, software-defined networks right to every server.

    CloudLab interoperates with existing testbeds including GENI and Emulab, 
    so you can take advantage of hardware at dozens of sites around the world."

Workload Priority
------------------
It should be possible to divide computational allocation of cluster 
resources by project, so that when resources are being competed for, 
a precedence can be determined.

One means of employing this could be to use *PriorityClass* in 
Kubernetes. A priority class is set when the Pod is created, and its 
value can be anywhere from 0 to 1,000,000,000. The default value is 
0 if not set.

https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/

