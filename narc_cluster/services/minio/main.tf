
module "minio" {
  source = "https://github.com/Skatteetaten/terraform-nomad-minio"

  # nomad
  nomad_datacenters               = ["local-1"]
  nomad_namespace                 = "default"
  nomad_host_volume               = "persistence"

  # consul
  consul_tags = ["azure", "local"]

  # minio
  service_name                    = "minio"
  host                            = "127.0.0.1"
  port                            = vars.port
  container_image                 = "minio/minio:latest"
  vault_secret                    = {
                                      use_vault_provider        = true,
                                      vault_kv_policy_name      = var.vault_kv_policy_name,
                                      vault_kv_path             = "secret/data/minio",
                                      vault_kv_field_access_key = var.vault_kv_access_key,
                                      vault_kv_field_secret_key = var.vault_KV_secret_key
                                    }
  data_dir                        = "/minio/data"
  container_environment_variables = ["SOME_VAR_N1=some-value"]
  use_host_volume                 = true
  use_canary                      = true
  resource_proxy                  = {
                                      cpu    = 200
                                      memory = 128
                                    }

  # Vault transit encryption as KMS
  kms_variables                   = {
                                      use_vault_kms = true,
                                      vault_address = "http://10.0.2.15:8200",
                                      vault_kms_approle_kv = vault_generic_secret.kms_approle.path,
                                      vault_kms_key_name = "minio"
                                    }

  # minio client
  mc_service_name                 = "mc"
  mc_container_image              = "minio/mc:latest"
  buckets                         = ["one", "two"]
}

resource "vault_generic_secret" "kms_approle" {
  data_json = <<EOT
    {
      "approle_id": "${vault_approle_auth_backend_role.minio_kms.role_id}" ,
      "secret_id": "${vault_approle_auth_backend_role_secret_id.minio_kms.secret_id}"
    }
  EOT
  path = "secret/kms"
}

resource "vault_generic_secret" "kms_transit_key" {
  data_json = "{}"
  path = "transit/keys/minio"
}