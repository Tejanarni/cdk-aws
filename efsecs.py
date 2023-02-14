from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_efs as efs,
    aws_ecs as ecs
)

class MyStack(core.Stack):
    
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create the EFS file system
        file_system = efs.FileSystem(self, 'MyEfsFileSystem',
                                     vpc=ec2.Vpc(self, 'MyVpc'),
                                     encrypted=True)

        # Define the mount point for the EFS volume
        efs_volume_config = ecs.Volume(name='my-efs-volume',
                                       efs_volume_configuration=ecs.EfsVolumeConfiguration(
                                           file_system_id=file_system.file_system_id,
                                           transit_encryption='ENABLED',
                                           authorization_config=ecs.AuthorizationConfig(
                                               access_point_id='fsap-0123456789abcdef0'  # Replace with your EFS access point ID
                                           )))

        # Create the ECS Fargate task definition with the EFS volume mount
        task_definition = ecs.FargateTaskDefinition(self, 'MyTaskDefinition',
                                                    memory_limit_mib=512,
                                                    cpu=256)
        task_definition.add_volume(efs_volume_config)
        container_definition = task_definition.add_container('MyContainer',
                                                              image=ecs.ContainerImage.from_registry('nginx:latest'),
                                                              memory_limit_mib=512,
                                                              cpu=256)
        container_definition.add_mount_points(ecs.MountPoint(
            container_path='/mnt/efs',
            source_volume=efs_volume_config.name,
            read_only=False
        ))

        # Create the ECS Fargate service
        service = ecs.FargateService(self, 'MyFargateService',
                                     cluster=ecs.Cluster(self, 'MyCluster', vpc=ec2.Vpc(self, 'MyVpc')),
                                     task_definition=task_definition,
                                     desired_count=1,
                                     assign_public_ip=True)

        # Grant the ECS task IAM role access to the EFS file system
        file_system.connections.allow_default_port_from(service.task_definition.task_role)
