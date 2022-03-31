===================
Computation
===================

Distributed Processing with Ray.io Cluster
-------------------------------------------
From Ray.io
    Ray is an open-source project developed at UC Berkeley RISE Lab. As a general-purpose and universal distributed 
    compute framework, you can flexibly run any compute-intensive Python workload — from distributed training or 
    hyperparameter tuning to deep reinforcement learning and production model serving.

Ray Core provides a simple, universal API for building distributed applications.
Ray’s native libraries and tools enable you to run complex ML applications with Ray.
You can deploy these applications on any of the major cloud providers, including AWS, GCP, and Azure, or run them on your own servers.
Ray also has a growing ecosystem of community integrations, including Dask, MARS, Modin, Horovod, Hugging Face, Scikit-learn, and others. The following figure gives you an overview of the Ray ecosystem.
Deploying on Kubernetes
    Overview
    You can leverage your Kubernetes cluster as a substrate for execution of distributed Ray programs. 
    The Ray Autoscaler spins up and deletes Kubernetes Pods according to the resource demands of the Ray workload. 
    Each Ray node runs in its own Kubernetes Pod.

Apache Spark
--------------


Dask
------


Dask vs. Spark 
---------------


Integrating Ray.io and Apache Spark
------------------------------------

SLURM
-------

IBM Cloud LSF
--------------

