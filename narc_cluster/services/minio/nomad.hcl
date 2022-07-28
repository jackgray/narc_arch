job "minio" {
  datacenters = ["local1"]
  type        = "service"
  [[ range  $idx := loop 1 5 ]]
  group "minio[[ $idx ]]" {
    ephemeral_disk {
      size    = 10000
      sticky  = true
      migrate = false
    }
    task "minio[[ $idx ]]" {
      driver = "docker"
      env {
        MINIO_ACCESS_KEY = "minio"
        MINIO_SECRET_KEY = "minio123"
      }
      user = "root"
      config {
        image = "minio/minio:RELEASE.2020-04-04T05-39-31Z"
        command = "server"
        args = [
          "http://minio{1...4}.service.consul:9000/data{1...2}"
        ]
        dns_servers        = ["${attr.unique.network.ip-address}"]
        port_map {
          http = 9000
        }
        privileged = true
        mounts = [
        # sample volume mount
          {
            type = "volume"
            target = "/data1"
            source = "data[[$idx]]-1"
            readonly = false
          },     
          {
            type = "volume"
            target = "/data2"
            source = "data[[$idx]]-2"
            readonly = false
          },               
        ]   
      }
      service {
        name = "minio[[ $idx ]]"
        port = "http"
        check {
          name           = "alive"
          type           = "http"
          port           = "http"
          path           = "/minio/health/live"
          interval       = "30s"
          timeout        = "20s"
          initial_status = "passing"
          check_restart {
            limit           = 3
            grace           = "90s"
            ignore_warnings = false
          }
        }
      }
      resources {
        network {
          port "http" {
            static = 9000
          }
        }
        cpu    = 20
        memory = 100
      }
    }
  }
  [[ end ]]
}