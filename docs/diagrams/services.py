from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.analytics import Spark
from diagrams.onprem.compute import Server, Nomad
from diagrams.onprem.database import PostgreSQL, Neo4J
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.aggregator import Fluentd
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.queue import Kafka
from diagrams.onprem.container import Docker
from diagrams.onprem.client import Client, User, Users
from diagrams.onprem.ci import ConcourseCI
from diagrams.onprem.network import Traefik, Nginx, Envoy, Consul
from diagrams.onprem.security import Vault
from diagrams.onprem.vcs import Git
from diagrams.onprem.iac import Terraform

from diagrams.outscale.network import LoadBalancer
from diagrams.outscale.storage import Storage


from diagrams.aws.compute import EC2, ECS
from diagrams.aws.network import ELB, PrivateSubnet, PublicSubnet
# from diagrams.aws.database import RDS
# from diagrams.aws.storage import S3

from diagrams.azure.compute import AppServices, VMLinux, VMScaleSet

from diagrams.gcp.compute import GCE, Run

graph_attr = {
    # "splines":"spline",
    # "layout":"neato",
}

with Diagram(name="NARC HPC", show=True, graph_attr=graph_attr):
    xnat = Nginx("XNAT")
    # terraform = Terraform("Terraform")
    # consul = Consul("Service Discovery")
    user = User("User")

    
    with Cluster("Docker Service Ecosystem"):
        
        with Cluster("Pipelines"):
            xnat2bids = Docker("xnat2bids")
            dwipreproc = Docker("dwipreproc")
            heudi = Docker("heuidiconv")
            fmriprep =  Docker("fmriprep")
            pytrack = Docker("PyTrack-NARC")
        
        with Cluster("narclab.com \nService Frontends"):
            # web = Docker("narclrab.com")
            vmAccess = Docker("remote.narclab.com \nCluster Driven VMs (Client)")
            dbAccess = Docker("data.narclab.com \nArangoDB")
            jobs = Docker("jobs.narclab.com \nJobs Dashboard")
            healthweb = Docker("health.narclab.com \nHealth Stats")
            redcapper = Docker("redcapper.narclab.com \nGUI for services like RedCap Fixer.")
        vms = Docker("Remote VMs \n(Server)")
        
        with Cluster("RedCap API"):
            redcapFixer = Docker("Redcap Fixer")
            redcap = Docker("Redcap Sync")
            
        with Cluster("Orchestration"):
            concourse = ConcourseCI("Concourse")
        
        with Cluster("Monitoring"):
            grafana = Grafana("Grafana")
            prometheus = Prometheus("Prometheus")
        
        
            
        
   
        
      

       
        # xnat2bids >> dwi
        # xnat2bids >> fmriprep

    with Cluster("On-Premise Cluster"):
         
            
        with Cluster("RUDI (MANAGER)"):
            
            node1server = Server("Node 1 \n(Manager)"),
            nomad1 = Nomad("Nomad Server")
            consul1 = Consul("Consul Server")
            vault1 = Vault("Key Management Server")
            # minio1 = Storage("Min.IO Storage 1")
                
        with Cluster("Golgi (ANALYSIS)"):
            node2server = Server("Node 2 - Golgi \n(Worker)"),
            nomad2 = Nomad("Nomad Client")
            consul2 = Consul("Consul Client")
            minio2 = Storage("Min.IO Storage")
          
        with Cluster("Cajal (DATABASE)"):
            node3server = Server("Node 3 - Cajal \n(Database)"),
            nomad3 = Nomad("Nomad Client")
            consul3 = Consul("Consul Client")
            db = PostgreSQL("Database")
            minio3 = Storage("Min.IO Storage")
        
    with Cluster("Reverse Proxy"):
        traefik = Traefik("Traefik Ingress")
        lb = LoadBalancer("Load Balancer")
        
        

    
    dgEdge = Edge(color="darkgreen")
    with Cluster("Multi-Cloud"):
        with Cluster("AWS VPC"):
            with Cluster("Public Subnet"):
                bastion = PublicSubnet("Bastion Host")
                nomad4 = Nomad("Nomad Server")
                consul4 = Consul("Consul Server")
                consul1 >> bastion
                # terraform >> dgEdge >> bastion 
            with Cluster("Private Subnet"):
                primary = EC2("Compute Helper")
                primary \
                    - Edge(color="brown", style="dashed") \
                    - Redis("replica") \
                    << Edge(label="collect")
                # localsvc >> Edge(color="brown") >> primary
        with Cluster("Azure VPC"):
            with Cluster("Public Subnet"):
                bastion = PublicSubnet("Bastion Host")
                nomad5 = Nomad("Nomad Client")
                consul5 = Consul("Consul Client")
                # terraform >> dgEdge >> bastion 
            with Cluster("Private Subnet"):
                primary = AppServices("Compute Helper")
                bastion >> primary
                primary \
                    - Edge(color="brown", style="dashed") \
                    - Redis("replica") \
                    << Edge(label="collect") 
                # localsvc >> Edge(color="brown") >> primary
        
        with Cluster("GCP VPC"):
            with Cluster("Public Subnet"):
                bastion = PublicSubnet("Bastion Host")
                nomad6 = Nomad("Nomad Client")
                consul6 = Consul("Consul Client")
                # terraform >> dgEdge >> bastion << consul1
            with Cluster("Private Subnet"):
                primary = GCE("Compute Helper")
                bastion >> primary
                primary \
                    - Edge(color="brown", style="dashed") \
                    - Redis("replica") \
                    << Edge(label="collect") 
            # localsvc >> Edge(color="brown") >> primary


    # EDGES
    backupEdge1 = Edge(color='purple', style='dashed')
    backupEdge2 = Edge(color='magenta', style='dotted')
    twoway = Edge(color='orange')
    drEdge = Edge(color='darkred')
    bEdge = Edge(color='darkblue')
    gEdge = Edge(color='green')
    oEdge = Edge(color='orange')
    
    # consul1 >> consul5
    # consul1 >> consul6
    # consul4 - backupEdge1 - consul2
    # consul4 -backupEdge2 - consul3
    # consul4 >> consul5
    # consul4 >> consul6
    # nomad4 >> nomad2
    # nomad4 >> nomad3

    concourse - drEdge >> redcap
    # concourse - drEdge - web
    concourse - drEdge - xnat2bids
    concourse - gEdge << jobs
    # concourse >> dwipreproc
    traefik << vms
    # traefik << web
    traefik << dbAccess
    traefik << vault1
    # traefik << bEdge - concourse
    traefik - bEdge << db
    traefik - bEdge << healthweb
    traefik - bEdge << redcapper
    nomad1 - gEdge << lb
    
    # lb >> xnat2bids
    # lb >> redcapFixer
    consul1 - twoway - nomad1
    nomad1 >> nomad2
    # nomad2 - bEdge >> traefik
    nomad1 >> nomad3
    nomad3 >> traefik
    consul1 << consul2 - twoway - nomad2
    consul1 << consul3 - twoway - nomad3
    consul1 >> vault1
    
    nomad2 >> minio2
    nomad3 >> minio3
    minio2 - Edge(color='red', style='dashed') - minio3
    # minio2 >> node2server
    # minio3 >> node3server
    
    xnat2bids >> heudi >> fmriprep
    xnat2bids >> dwipreproc
    # terraform >> consul1
    nomad3 >> db << redcap
    # nomad2 >> concourse

    
    # user - drEdge >> web
    # web >> dbAccess 
    vmAccess >> vms
    # web - drEdge >> jobs
    redcapper >> drEdge - redcapFixer
    healthweb >> gEdge >> grafana
    healthweb >> gEdge >> prometheus
    
    xnat >> oEdge << xnat2bids
    
    user >> jobs
    
    user >> drEdge >> redcapper 
    redcapper >> drEdge >> redcapFixer >> Edge(color='blue') >> db
    