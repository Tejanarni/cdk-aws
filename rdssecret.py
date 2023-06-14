from aws_cdk import (
    aws_secretsmanager as secretsmanager,
    aws_rds as rds,
    aws_ec2 as ec2,
    aws_kms as kms,
    core
)

# ...

aurora_cluster_secret_name = "ccwb-database-instanceAuroraClusterCredentials"

# Check if the secret already exists
existing_secret = secretsmanager.Secret.from_secret_name_v2(
    self,
    "ExistingAuroraClusterCredentialsSecret",
    secret_name=aurora_cluster_secret_name
)

aurora_cluster_secret = None  # Define the variable outside the conditional block

if not existing_secret:
    # Create the secret if it doesn't exist
    aurora_cluster_secret = secretsmanager.Secret(
        self,
        "AuroraClusterCredentials",
        secret_name=aurora_cluster_secret_name,
        description=db_instance_name + " Aurora Cluster Credentials",
        generate_secret_string=secretsmanager.SecretStringGenerator(
            exclude_characters="\"@/\\ '",
            generate_string_key="password",
            password_length=30,
            secret_string_template='{"username":"' + aurora_cluster_username + '"}'
        )
    )

aurora_cluster_credentials = rds.Credentials.from_secret(
    aurora_cluster_secret or existing_secret,  # Use the existing secret if it exists, otherwise use the newly created secret
    aurora_cluster_username
)
self.aurora_cluster_credentials_secret_arn = (
    aurora_cluster_secret.secret_full_arn if aurora_cluster_secret else existing_secret.secret_full_arn
)

# ...

my_key_alias = kms.Alias.from_alias_name(self, "myKey", "alias/signet/rds")

# ...
