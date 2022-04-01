===================
Computation
===================

This section aims to design a means for more granular control over cluster resources 
from within computational code. This study shows how parallelizing and distributing 
processes across all available resources can cut computation time by as much as 75%. 

Computation proccess managers should not be confused with application workflow 
managers, or CI/CD pipeline orchestrators. See the section on Orchestration for solutions 
on load balancing resources at the container level.


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
        You can leverage your Kubernetes cluster as a substrate for execution of distributed Ray programs. 
        The Ray Autoscaler spins up and deletes Kubernetes Pods according to the resource demands of the Ray workload. 
        Each Ray node runs in its own Kubernetes Pod.

Apache Spark
--------------
Using a data chunking strategy similar to MapReduce, granular control 
of computational processes, and their node distribution, can be achieved, 
and processing time can be reduced by up to 75%.

Setting up PySpark, JupyterHub, Kubeflow and Minio on Kubernetes
    https://medium.com/@szinck/setting-up-pyspark-jupyter-and-minio-on-kubeflow-kubernetes-aab98874794f

Dask
------
Comparable to Spark, but built on Python, and more similar in syntax to 
Numpy, pandas, etc., and therefore easier to integrate with existing code.


Dask vs. Spark 
---------------

Integrating Ray.io and Dask
------------------------------------
From Ray.io
    Dask is a Python parallel computing library geared towards scaling 
    analytics and scientific computing workloads. It provides big data 
    collections that mimic the APIs of the familiar NumPy and Pandas 
    libraries, allowing those abstractions to represent larger-than-memory 
    data and/or allowing operations on that data to be run on a multi-machine 
    cluster, while also providing automatic data parallelism, smart 
    scheduling, and optimized operations. Operations on these collections 
    create a task graph, which is executed by a scheduler.

    Ray provides a scheduler for Dask (dask_on_ray) which allows you to 
    build data analyses using Dask’s collections and execute the underlying 
    tasks on a Ray cluster.

    dask_on_ray uses Dask’s scheduler API, which allows you to specify any 
    callable as the scheduler that you would like Dask to use to execute 
    your workload. Using the Dask-on-Ray scheduler, the entire Dask ecosystem 
    can be executed on top of Ray.

More:
    https://docs.ray.io/en/latest/data/dask-on-ray.html

Integrating Ray.io and Apache Spark
------------------------------------
From Ray.io
    RayDP is a distributed data processing library that provides simple 
    APIs for running Spark on Ray and integrating Spark with distributed 
    deep learning and machine learning frameworks. RayDP makes it simple 
    to build distributed end-to-end data analytics and AI pipeline. 
    Instead of using lots of glue code or an orchestration framework to 
    stitch multiple distributed programs, RayDP allows you to write Spark, 
    PyTorch, Tensorflow, XGBoost code in a single python program with 
    increased productivity and performance. You can build an end-to-end 
    pipeline on a single Ray cluster by using Spark for data preprocessing, 
    RaySGD or Horovod for distributed deep learning, RayTune for 
    hyperparameter tuning and RayServe for model serving.

More
    https://docs.ray.io/en/latest/data/raydp.html

Modin
-----
From Ray.io 
    Modin, previously Pandas on Ray, is a dataframe manipulation 
    library that allows users to speed up their pandas workloads 
    by acting as a drop-in replacement. Modin also provides support 
    for other APIs (e.g. spreadsheet) and libraries, like xgboost.

    Modin has a layered architecture, and the core abstraction for 
    data manipulation is the Modin Dataframe, which implements a 
    novel algebra that enables Modin to handle all of pandas (see 
    Modin’s documentation for more on the architecture). Modin’s 
    internal dataframe object has a scheduling layer that is able 
    to partition and operate on data with Ray.

    Dataframe operations
        The Modin Dataframe uses Ray tasks to perform data manipulations. 
        Ray Tasks have a number of benefits over the actor model for 
        data manipulation:
            -   Multiple tasks may be manipulating the same objects 
            simultaneously
            -   Objects in Ray’s object store are immutable, making 
            provenance and lineage easier to track
            -   As new workers come online the shuffling of data will 
            happen as tasks are scheduled on the new node
            -   Identical partitions need not be replicated, especially 
            beneficial for operations that selectively mutate the data 
            (e.g. fillna).
            -   Finer grained parallelism with finer grained placement 
            control
            
    Machine Learning
        Modin uses Ray Actors for the machine learning support it 
        currently provides. Modin’s implementation of XGBoost is 
        able to spin up one actor for each node and aggregate all 
        of the partitions on that node to the XGBoost Actor. Modin 
        is able to specify precisely the node IP for each actor on 
        creation, giving fine-grained control over placement - a must 
        for distributed training performance.
    
Reference 
    https://docs.ray.io/en/latest/data/modin/index.html

====================
Machine Learning
====================

RLlib Reinforcement Learning
---------------------------------------------
From Ray.io
    RLlib is an open-source library for reinforcement learning (RL), 
    offering support for production-level, highly distributed RL 
    workloads while maintaining unified and simple APIs for a large 
    variety of industry applications. Whether you would like to train 
    your agents in a multi-agent setup, purely from offline (historic) 
    datasets, or using externally connected simulators, RLlib offers a 
    simple solution for each of your decision making needs.

    You don’t need to be an RL expert to use RLlib, nor do you need 
    to learn Ray or any other of its libraries! If you either have 
    your problem coded (in python) as an RL environment or own lots 
    of pre-recorded, historic behavioral data to learn from, you will 
    be up and running in only a few days.

    Features
        Highly distributed learning: 
            Our RLlib algorithms (such as our 
            “PPO” or “IMPALA”) allow you to set the num_workers config 
            parameter, such that your workloads can run on 100s of 
            CPUs/nodes thus parallelizing and speeding up learning.

        Vectorized (batched) and remote (parallel) environments: 
            RLlib auto-vectorizes your gym.Envs via the num_envs_per_worker 
            config. Environment workers can then batch and thus 
            significantly speedup the action computing forward pass. On 
            top of that, RLlib offers the remote_worker_envs config to 
            create single environments (within a vectorized one) as ray 
            Actors, thus parallelizing even the env stepping process.

        Multi-agent RL (MARL): 
            Convert your (custom) gym.Envs into a multi-agent one via 
            a few simple steps and start training your agents in any 
            of the following fashions:
                1) Cooperative with shared or separate policies and/or value functions.
                2) Adversarial scenarios using self-play and league-based training.
                3) Independent learning of neutral/co-existing agents.
                
        External simulators: 
            Don’t have your simulation running as a gym.Env in python? 
            No problem! RLlib supports an external environment API and 
            comes with a pluggable, off-the-shelve client/ server setup 
            that allows you to run 100s of independent simulators on 
            the “outside” (e.g. a Windows cloud) connecting to a central 
            RLlib Policy-Server that learns and serves actions. 
            Alternatively, actions can be computed on the client side to 
            save on network traffic.

        Offline RL and imitation learning/behavior cloning: 
            You don’t have a simulator for your particular problem, but 
            tons of historic data recorded by a legacy (maybe non-RL/ML) 
            system? This branch of reinforcement learning is for you! 
            RLlib’s comes with several offline RL algorithms 
            (CQL, MARWIL, and DQfD), allowing you to either purely 
            behavior-clone your existing system or learn how to further 
            improve over it.

More
    https://docs.ray.io/en/latest/rllib/core-concepts.html