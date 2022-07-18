# from diagrams import Cluster, Diagram



# from diagrams.onprem.compute import Nomad, Server
# from diagrams.onprem.container import Docker 
# from diagrams.onprem.database import Neo4J
from diagrams.onprem.iac import Terraform
from diagrams.onprem.network import Consul, Envoy,Traefik
# from diagrams.onprem.security import Vault
# from diagrams.onprem.vcs import Github

# with Diagram("General Structure"):
#     terraform = Terraform("IaC")
    
#     ec2 = EC2("Heavy Compute Load") 
#     lb = ELB("Load Balancer")
#     events = RDS("events")
    
#     with Cluster("Service Mesh Network"):
#         consul = Consul("Service Mesh Network")
    
#     with Cluster("NARC Cluster"):
#         with Cluster("Cloud"):
#             cloud_workers = [ECS("worker1"),
#                              ECS("worker2")]
#             ec2s = [EC2("sirattenborough"),
#                     EC2("jonstewart")]
            
#         with Cluster("On-Prem"):
#             local_servers = [Server("golgi"),
#                              Server("jonstewart")]
#             local_nomad = [Nomad("Nomad1")]
#             storage = S3("Hot file storage")
    
#     terraform >> consul
#     consul >> cloud_workers, local_nomad >> events
#     # consul >> local_servers >> events

from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.analytics import Spark
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.aggregator import Fluentd
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import Kafka

from diagrams.aws.compute import EC2, ECS
from diagrams.aws.network import ELB, PrivateSubnet, PublicSubnet
# from diagrams.aws.database import RDS
# from diagrams.aws.storage import S3

from diagrams.azure.compute import AppServices, VMLinux, VMScaleSet

from diagrams.gcp.compute import GCE, Run


with Diagram(name="Advanced Web Service with On-Premise (colored)", show=True):
    terraform = Terraform("Launch Cloud Services")

    metrics = Prometheus("metric")
    metrics << Edge(color="firebrick", style="dashed") << Grafana("monitoring")

    with Cluster("Local Service Cluster"):
        with Cluster("Cluster"):
            localsvc = [
                Server("golgi"),
                ]
            consul = Consul("Service Mesh Network")
    
    dgEdge = Edge(color="darkgreen")
    with Cluster("Multi-Cloud"):
        with Cluster("AWS VPC"):
            with Cluster("Public Subnet"):
                bastion = PublicSubnet("Bastion Host")
                terraform >> dgEdge >> bastion 
            with Cluster("Private Subnet"):
                primary = EC2("Compute Helper")
                bastion >> primary
                primary \
                    - Edge(color="brown", style="dashed") \
                    - Redis("replica") \
                    << Edge(label="collect") \
                    << metrics
                # localsvc >> Edge(color="brown") >> primary
        with Cluster("Azure VPC"):
            with Cluster("Public Subnet"):
                bastion = PublicSubnet("Bastion Host")
                terraform >> dgEdge >> bastion 
            with Cluster("Private Subnet"):
                primary = AppServices("Compute Helper")
                bastion >> primary
                primary \
                    - Edge(color="brown", style="dashed") \
                    - Redis("replica") \
                    << Edge(label="collect") \
                    << metrics
                # localsvc >> Edge(color="brown") >> primary
        
        with Cluster("GCP VPC"):
            with Cluster("Public Subnet"):
                bastion = PublicSubnet("Bastion Host")
                terraform >> dgEdge >> bastion
            with Cluster("Private Subnet"):
                primary = GCE("Compute Helper")
                bastion >> primary
                primary \
                    - Edge(color="brown", style="dashed") \
                    - Redis("replica") \
                    << Edge(label="collect") \
                    << metrics
            # localsvc >> Edge(color="brown") >> primary

    with Cluster("Sessions HA"):
        primary = Redis("session")
        primary \
            - Edge(color="brown", style="dashed") \
            - Redis("replica") \
            << Edge(label="collect") \
            << metrics
        terraform >> Edge(color="brown") >> primary

    with Cluster(""):
        primary = PostgreSQL("users")
        primary \
            - Edge(color="brown", style="dotted") \
            - PostgreSQL("replica") \
            << Edge(label="collect") \
            << metrics
        terraform >> Edge(color="black") >> primary

    aggregator = Fluentd("logging")
    aggregator \
        >> Edge(label="parse") \
        >> Kafka("stream") \
        >> Edge(color="black", style="bold") \
        >> Spark("analytics")

    terraform >> consul \
        >> Edge(color="darkgreen") \
        << localsvc \
        >> Edge(color="darkorange") \
        >> aggregator
         
    