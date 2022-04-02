===================================
Planning & Design Considerations
===================================

Assessing and Prioritizing Needs
---------------------------------

Design Approach: Important questions to ask:
    What are the bottlenecks in data flow?

    What are the most pressing needs/immediate goals?

    What are the long term goals of the lab?

    What is the current data process like? What are the 
    familiar/comfortable methods of the team.

Maintenance
------------
As a general rule, the more granular control one seeks in a system, the more 
resources and specialized knowledge is required to maintain or build on top 
of it. This also generally applies to product cost: if a service is free, you 
will either have to host and maintain it yourself, or you will not have access 
to all features, or the service will either grow and incur a blind cost model that 
you will essentially be hostage to, lest potantially the entire infrastructure 
will need redesigning.

Paid Service vs. On-Prem Savings and Trade-offs 
------------------------------------------------
Because of the fairly direct trade-off between cost of paid, pre-packaged 
or externally maintained systems and cost of on-premise expertise 
to maintain a custom-built and cost effective solution, a few key 
factors should be considered when making this decision:
    -   annual costs of an all-in-one cluster management solution
    -   the salary of Cloud Engineers in the private market (worst case scenario/budget ceiling)
    -   the salary and ambition of a less experienced developer 
        potentially capable of filling the needs
    -   the risk trade-off of the aforementioned factor 
    -   the chances that a post-doctoral or Phd candidate will be familiar 
        with complex DevOps tools in this document not directly relating to the analyis 
        of data.
    -   the learning curve of the various tools and required time 
        investment feasability


Tentative Setup Outline
--------------------------------
This section serves as a tentative action plan for implementing the cluster 
being proposed. It will change and evolve as more design choices are cemented. 

Create Cluster 
    Install Kubernetes 

Database Conversion
    Convert MS Access to document or SQL database

    Install and configure new database for cluster 

    Install BudiBase
        - https://docs.budibase.com/docs/kubernetes-k8s
        - Use Budibase helm chart 
        - create namespace "Budibase"

        .. code-block:: sh 

            helm repo add budibase https://budibase.github.io/budibase/
            helm repo update
            helm install --create-namespace --namespace budibase budibase budibase/budibase
        
        Get IP of ingress controller

        .. code-block:: sh

            kubectl get pods -n budibase 
            kubectl get ingress -n budibase

        Visit ingress URL in a web browser to access budibase interface 

        Custom Domain Configuration
            - Add domain settings to **values.yaml** 
            - Setup an A record in DNS provider to point the URL of the ingress controller 

            .. code-block:: sh

                ingress:
                    enabled: true
                    nginx: true
                    className: ""
                    annotations: 
                        kubernetes.io/ingress.class: nginx
                    hosts:
                        - host: yourdomain.com
                        paths:
                        - path: /
                            pathType: Prefix
                            backend:
                            service:
                                name: proxy-service
                                port:
                                number: 10000 

        
        Import MS Access database 

        Connect BudiBase to newly created database 

        Set up user accounts

Storage 
    Install MinIO 
        Move lab files from existing RAID storage into buckets on MinIO  
        
        Connect and configure automated MongoDB snapshot backups

        Install O-Drive
            Set up User Accounts
            
            Install MinIO Buckets as folders on user computers 
