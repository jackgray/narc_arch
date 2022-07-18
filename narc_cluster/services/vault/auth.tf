#--------------------------------
# Enable userpass auth method
#--------------------------------

resource "vault_auth_backend" "userpass" {
  type = "userpass"
}

# Create a user, 'student'
resource "vault_generic_endpoint" "jack" {
  depends_on           = [vault_auth_backend.userpass]
  path                 = "auth/userpass/users/jack"
  ignore_absent_fields = true

  data_json = <<EOT
{
  "policies": ["admins", "eaas-client"],
  "password": "changeme"
}
EOT
}
    