from diagrams import Cluster, Diagram, Edge

from diagrams.programming.language import R
from diagrams.generic.virtualization import Virtualbox, Vmware, XEN
from diagrams.generic.device import Tablet


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

with Diagram(name="NARC Services", show=True, graph_attr=graph_attr):
    xnat = Nginx("XNAT")
    # terraform = Terraform("Terraform")
    # consul = Consul("Service Discovery")
    user1 = User("User")
    user2 = User("User")
    user3 = User("User")
    redcapdb = Redis("Redcap DB")
    tab1 = Tablet("O-Drive 1")
    tab2 = Tablet("O-drive 2")
    tab3 = Tablet("O-drive 3")

    with Cluster("Docker Service Ecosystem"):
        
        odrive = Docker("O-Drive Server")
        
        with Cluster("Pipelines"):
            xnat2bids = Docker("xnat2bids")
            dwipreproc = Docker("dwipreproc")
            heudi = Docker("heuidiconv")
            fmriprep =  Docker("fmriprep")
            pytrack = Docker("PyTrack-NARC")
            postanalysis = R("post-analysis")
        
        with Cluster("narclab.com \nService Frontends"):
            # web = Docker("narclrab.com")
            vmAccess = Docker("remote.narclab.com \nCluster Driven VMs (Client)")
            dbAccess = Docker("data.narclab.com \nArangoDB")
            jobs = Docker("jobs.narclab.com \nJobs Dashboard")
            healthweb = Docker("health.narclab.com \nHealth Stats")
            redcapper = Docker("redcapper.narclab.com \nRedcap API Client.")
        vms = Docker("Remote VMs \n(Server)")
        
        with Cluster("RedCap API"):
            redcapDoctor = Docker("Redcap Doctor")
            redcap = Docker("Redcap Sync")
            
        # with Cluster("Orchestration"):
            # concourse = ConcourseCI("Concourse")
        
        # with Cluster("Monitoring"):
        #     grafana = Grafana("Grafana")
        #     prometheus = Prometheus("Prometheus")
        
        
            
        
   
        
      

       
        # xnat2bids >> dwi
        # xnat2bids >> fmriprep
    with Cluster("On-Premise Cluster"):   
        with Cluster("RUDI (Manager)"):
            
            # node1server = Server("Node 1 \n(Manager)")
            nomad1 = Nomad("Nomad Server")
            # consul1 = Consul("Consul Server")
            vault1 = Vault("Key Management Server")
            # minio1 = Storage("Min.IO Storage 1")
            concourse = ConcourseCI("Conductor")  
                
        with Cluster("Node 2 - Golgi (Worker/Database)"):
            # node2server = Server("Node 2 - Golgi \n(Worker)"),
            nomad2 = Nomad("Nomad Client")
            # consul2 = Consul("Consul Client")
            db = Neo4J("ArangoDB")

            minio2 = Storage("Min.IO Storage")
          
        with Cluster("Node 3 - Gazanaga (Worker/Storage)"):
            # node3server = Server("Node 3 - Cajal \n(Database)"),
            nomad3 = Nomad("Nomad Client")
            # consul3 = Consul("Consul Client")
            minio3 = Storage("Min.IO Storage")
            minio_manager = Storage("Min.IO Manager")
            jdrive = Storage("J-Drive Mount")

        with Cluster("Node 4 - Cajal (Worker/Analysis)"):
            # node4server = Server("Node 4 - Gazzaniga \n(Worker)"),  
            minio4 = Storage("Min.io Storage")
            gazanaga = Nomad("Nomad Client")
    # with Cluster("Reverse Proxy"):
    #     traefik = Traefik("Traefik Ingress")
    #     lb = LoadBalancer("Load Balancer")
        
        

    
    dgEdge = Edge(color="darkgreen")
    # with Cluster("Multi-Cloud"):
    #     with Cluster("AWS VPC"):
    #         with Cluster("Public Subnet"):
    #             bastion = PublicSubnet("Bastion Host")
    #             nomad4 = Nomad("Nomad Server")
    #             consul4 = Consul("Consul Server")
    #             # consul1 >> bastion
    #             # terraform >> dgEdge >> bastion 
    #         with Cluster("Private Subnet"):
    #             primary = EC2("Compute Helper")
    #             primary \
    #                 - Edge(color="brown", style="dashed") \
    #                 - Redis("replica") \
    #                 << Edge(label="collect")
    #             # localsvc >> Edge(color="brown") >> primary
    #     with Cluster("Azure VPC"):
    #         with Cluster("Public Subnet"):
    #             bastion = PublicSubnet("Bastion Host")
    #             nomad5 = Nomad("Nomad Client")
    #             consul5 = Consul("Consul Client")
    #             # terraform >> dgEdge >> bastion 
    #         with Cluster("Private Subnet"):
    #             primary = AppServices("Compute Helper")
    #             bastion >> primary
    #             primary \
    #                 - Edge(color="brown", style="dashed") \
    #                 - Redis("replica") \
    #                 << Edge(label="collect") 
    #             # localsvc >> Edge(color="brown") >> primary
        
    #     with Cluster("GCP VPC"):
    #         with Cluster("Public Subnet"):
    #             bastion = PublicSubnet("Bastion Host")
    #             nomad6 = Nomad("Nomad Client")
    #             consul6 = Consul("Consul Client")
    #             # terraform >> dgEdge >> bastion << consul1
    #         with Cluster("Private Subnet"):
    #             primary = GCE("Compute Helper")
    #             bastion >> primary
    #             primary \
    #                 - Edge(color="brown", style="dashed") \
    #                 - Redis("replica") \
    #                 << Edge(label="collect") 
            # localsvc >> Edge(color="brown") >> primary


    # EDGES
    backupEdge1 = Edge(color='purple', style='dashed')
    backupEdge2 = Edge(color='magenta', style='dotted')
    twoway = Edge(color='orange')
    drEdge = Edge(color='darkred')
    bEdge = Edge(color='darkblue')
    gEdge = Edge(color='green')
    oEdge = Edge(color='orange')
    pEdge = Edge(color="pink")
    boldEdge = Edge(color='darkorange')
    
    # consul1 >> consul5
    # consul1 >> consul6
    # consul4 - backupEdge1 - consul2
    # consul4 -backupEdge2 - consul3
    # consul4 >> consul5
    # consul4 >> consul6
    # nomad4 >> nomad2
    # nomad4 >> nomad3

    # concourse - drEdge >> redcap
    # concourse - drEdge - web
    # concourse - drEdge - xnat2bids
    # concourse - gEdge << jobs
    # concourse >> dwipreproc
    # traefik << vms
    # traefik << web
    # traefik << dbAccess
    # traefik << vault1
    # traefik << bEdge - concourse
    # traefik - bEdge << db
    # traefik - bEdge << healthweb
    # traefik - bEdge << redcapper
    # nomad1 - gEdge << lb
    
    # lb >> xnat2bids
    # lb >> redcapDoctor
    # consul1 - twoway - nomad1
    nomad1 >> nomad2
    # nomad2 - bEdge >> traefik
    nomad1 >> nomad3
    nomad1 >> gazanaga
    
    # nomad3 >> traefik
    # consul1 << consul2 - twoway - nomad2
    # consul1 << consul3 - twoway - nomad3
    # consul1 >> vault1
    
    # nomad2 >> minio2
    # nomad3 >> minio3
    minio2 - Edge(color='red', style='dashed') - minio3 - Edge(color="red", style="dashed") - minio4
    # minio2 >> node2server
    # minio3 >> node3server
    
    nomad1 - xnat2bids
    xnat2bids >> heudi >> fmriprep >> postanalysis
    xnat2bids >> dwipreproc >> postanalysis
    pytrack >> postanalysis
    # terraform >> consul1
    # nomad3 >> db << redcap
    # nomad2 >> concourse

    # concourse
    
    # user - drEdge >> web
    # web >> dbAccess 
    vmAccess << vms
    # web - drEdge >> jobs
    # redcapper >>  redcapDoctor
 
    
    xnat >> oEdge << xnat2bids
    
    # user1>> jobs
    # user1 >> dbAccess
    
    # user1 >> redcapper 
    redcapper << redcapDoctor >>  db
    dbAccess << db
    redcap >> db
    redcapdb - redcap
    
    odrive - Edge(color="purple", style="bold") - minio_manager
    minio_manager - minio3
    minio_manager - jdrive
    
    
    
    user1 >> tab1 
    tab1 << Edge(color="darkred") << odrive
    user2 >> tab2 
    tab2 << Edge(color="darkred") << odrive
    user3 >> tab3 
    tab3 << Edge(color="darkred") << odrive
    tab3 >> Edge(color="darkgreen") >> jobs
    
    tab1 - boldEdge - vault1
    tab2 - boldEdge - vault1
    tab3 - boldEdge - vault1
    tab2 >> dgEdge >> dbAccess
    # tab3 - vault1
    tab1 >> dgEdge >> vmAccess
    # tab3 >> dgEdge >>jobs
    jobs - concourse