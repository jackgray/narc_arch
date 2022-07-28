job "minio" {
    region = "global"
    datacenters = ["wasil-local"]
    type = "service"
    priority = 80
    // constraint {
    // attribute = "$${attr.unique.hostname}"
    // value = "rpi3bp.wasil.local"
    // }
    // update {
    // stagger = "20s"
    // max_parallel = 1
    // auto_revert = true
    // auto_promote = true
    // canary = 1
    // }

    group "minio" {
        count = 1
        network {
        port "api" {}
        port "embedded_console" {}
        port "console" {
        to = 9090
    }
}
    volume "minio" {
        type = "host"
        read_only = false
        source = "minio"
}
    service {
    name = "minio"
    port = "embedded_console"
    tags = [
    "traefik.enable=true",
    "traefik.http.routers.minio.rule=HostRegexp(`{domain:(storage|minio)\\..+}`)",
    "traefik.http.routers.minio.entrypoints=http",
    # "traefik.http.routers.minio.middlewares=redirect@file",
    "traefik.http.routers.minio-secure.rule=HostRegexp(`{domain:(storage|minio)\\..+}`)",
    "traefik.http.routers.minio-secure.entrypoints=https",
    "traefik.http.routers.minio-secure.tls=true",
    ]
}
    service {
    name = "minio-api"
    port = "api"
    tags = [
    "traefik.enable=true",
    "traefik.http.routers.minio-api.rule=HostRegexp(`{domain:(storage-api|minio-api)\\..+}`)",
    "traefik.http.routers.minio-api.entrypoints=http",
    # "traefik.http.routers.minio-api.middlewares=redirect@file",
    "traefik.http.routers.minio-api-secure.rule=HostRegexp(`{domain:(storage-api|minio-api)\\..+}`)",
    "traefik.http.routers.minio-api-secure.entrypoints=https",
    "traefik.http.routers.minio-api-secure.tls=true",
    ]
    # check {
    # type = "http"
    # path = "/minio/health/live"
    # interval = "30s"
    # timeout = "20s"
    # }
    }
    # service {
    # name = "minio-console"
    # port = "console"
    # tags = [
    # "traefik.enable=true",
    # "traefik.http.routers.minio-console.rule=HostRegexp(`{domain:minio-console\\..+}`)",
    # "traefik.http.routers.minio-console.entrypoints=http",
    # "traefik.http.routers.minio-console.middlewares=redirect@file",
    # "traefik.http.routers.minio-console-secure.rule=HostRegexp(`{domain:minio-console\\..+}`)",
    # "traefik.http.routers.minio-console-secure.entrypoints=https",
    # "traefik.http.routers.minio-console-secure.tls=true",
    # # "traefik.http.routers.minio-console.rule=HostRegexp(`{domain:minio-console\\..+}`)",
    # # "traefik.http.routers.minio-console.entrypoints=http",
    # ]
    # # check {
    # # type = "http"
    # # path = "/minio/health/live"
    # # interval = "30s"
    # # timeout = "20s"
    # # }
    # }
    task "server" {
    driver = "docker"
    user = "root"
    # volume_mount {
    # volume  = "minio"
    # destination = "/data"
    # read_only = false
    # }
    config {
    image = "minio/minio:${version}"
    command = "server"
    args = [
    "/data",
    "--address",
    "0.0.0.0:$${NOMAD_HOST_PORT_api}",
    "--console-address",
    "0.0.0.0:$${NOMAD_HOST_PORT_embedded_console}"
    ]
    ports = ["api", "embedded_console"]
    volumes = [
    "/var/lib/nomad-data/minio:/data"
    ]
    }
    env {
    MINIO_PROMETHEUS_AUTH_TYPE = "public"
    MINIO_ROOT_USER = "admin"
    MINIO_ROOT_PASSWORD = "vd5b68UHGGn76f87tgo78"
    # CONSOLE_MINIO_SERVER = "http://$${NOMAD_HOST_ADDR_api}"
    CONSOLE_PBKDF_PASSPHRASE = "vd5u6bf86ingot7m786756"
    CONSOLE_PBKDF_SALT = "xsa2ax24asjgknh89h8lo"
    MINIO_PROMETHEUS_URL = "http://victoriametrics.service.consul"
    CONSOLE_MINIO_REGION = "dc-1"
    MINIO_PROMETHEUS_JOB_ID = "minio-job"
    }
    # template {
    # data = "---\n{{ key \"nomad/prometheus/prometheus.yml\" }}"
    # destination = "local/prometheus.yml"
    # change_mode = "signal"
    # change_signal = "SIGHUP"
    # }
    resources {
    cpu = 600
    memory = 1024
    }
    }
    # task "console" {
    # driver = "docker"
    # config {
    # image = "minio/console:v0.12.3"
    # command = "server"
    # ports = ["console"]
    # # dns_servers = ["192.168.1.5"]
    # # dns_options = ["use-vc"]
    # }
    # env {
    # # CONSOLE_LOG_QUERY_URL = "http://log_search:8080"
    # # CONSOLE_MINIO_SERVER = "https://storage.mindthebig.rocks"
    # CONSOLE_MINIO_SERVER = "http://$${NOMAD_HOST_ADDR_api}"
    # CONSOLE_PBKDF_PASSPHRASE = "vd5u6bf86ingot7m786756"
    # CONSOLE_PBKDF_SALT = "xsa2ax24asjgknh89h8lo"
    # CONSOLE_PROMETHEUS_URL = "http://victoriametrics.service.consul/"
    # CONSOLE_MINIO_REGION = "dc-1"
    # MINIO_PROMETHEUS_JOB_ID = "minio-job"
    # # LOGSEARCH_QUERY_AUTH_TOKEN = "ubyf756bri7ng7ordb65d7i6bg87nfi76"
    # }
    # # template {
    # # data = "---\n{{ key \"nomad/prometheus/prometheus.yml\" }}"
    # # destination = "local/prometheus.yml"
    # # change_mode = "signal"
    # # change_signal = "SIGHUP"
    # # }
    # resources {
    # cpu = 200
    # memory = 256
    # }
    # }
    }
    }