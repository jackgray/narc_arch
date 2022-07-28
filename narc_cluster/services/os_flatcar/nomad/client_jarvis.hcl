bind_addr = "0.0.0.0"

data_dir  = "/var/nomad/data"

client {
    enabled = true

//   servers = ["192.168.10.10:4647"]
    servers = ["127.0.0.1"]

    host_volume "mysql" {
        path = "/opt/mysql/data"
    //   read_only = false
    }
  
    host_volume "ca-certificates" {
        path = "/home/jackgray/Code/narc_arch/narc_cluster/services/certs"
    //   read_only = true
    }
}

