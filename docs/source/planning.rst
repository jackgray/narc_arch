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

    What aspects of dataflow are users attached to, and which 
    ones are particularly disfavored or cumbersome? 

Maintenance
------------
As a general rule, the more granular control offered by a system, the more 
resources and expertise are required to maintain or build on it. This  
generally applies to product cost as well: if a solution is free, you 
will probably have to host and maintain it yourself, not have access 
to all features, or the service will eventually mature to the point of 
incurring an unpredictable cost model that 
you will essentially be hostage to without redesigning  
at least some parts of the system. 

Paid Solutions vs. Self-Hosted/Maintained
------------------------------------------------
Because of the fairly direct trade-off between cost of paid, pre-packaged 
or externally maintained systems and the cost of staffing expertise 
needed to maintain a custom-built and cost effective solution, a few key 
factors should be considered when making this decision:
    -   Annual costs of an all-in-one cluster management solution
    -   How much you want to spend on full time data management staff 
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
