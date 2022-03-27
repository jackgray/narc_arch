============
Setup Steps
============

Create Cluster 
    Install Kubernetes 

Database Conversion
    Convert MS Access to MongoDB

    Install MongoDB Shard

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

        Connect BudiBase to MongoDB

        Set up user accounts

Storage 
    Install MinIO 
        Connect MongoDB backups

        Install O-Drive
            Setup User Accounts
            Install MinIO Buckets as folders on user computers 
