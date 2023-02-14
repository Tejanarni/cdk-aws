import * as cdk from 'aws-cdk-lib';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as efs from 'aws-cdk-lib/aws-efs';
import * as ec2 from 'aws-cdk-lib/aws-ec2';

const app = new cdk.App();
const stack = new cdk.Stack(app, 'MyStack');

// Create the EFS file system
const fileSystem = new efs.FileSystem(stack, 'MyEfsFileSystem', {
  vpc: new ec2.Vpc(stack, 'MyVpc'),
  encrypted: true
});

// Define the mount point for the EFS volume
const efsVolumeConfig = {
  name: 'my-efs-volume',
  efsVolumeConfiguration: {
    fileSystemId: fileSystem.fileSystemId,
    transitEncryption: 'ENABLED',
    authorizationConfig: {
      accessPointId: 'fsap-0123456789abcdef0' // Replace with your EFS access point ID
    }
  }
};

// Create the ECS Fargate task definition with the EFS volume mount
const taskDefinition = new ecs.FargateTaskDefinition(stack, 'MyTaskDefinition', {
  memoryLimitMiB: 512,
  cpu: 256
});
taskDefinition.addVolume(efsVolumeConfig);
const containerDefinition = taskDefinition.addContainer('MyContainer', {
  image: ecs.ContainerImage.fromRegistry('nginx:latest'),
  memoryLimitMiB: 512,
  cpu: 256
});
containerDefinition.addMountPoints({
  containerPath: '/mnt/efs',
  sourceVolume: efsVolumeConfig.name,
  readOnly: false
});

// Create the ECS Fargate service
const service = new ecs.FargateService(stack, 'MyFargateService', {
  cluster: new ecs.Cluster(stack, 'MyCluster', {
    vpc: new ec2.Vpc(stack, 'MyVpc')
  }),
  taskDefinition: taskDefinition,
  desiredCount: 1,
  assignPublicIp: true
});

// Grant the ECS task IAM role access to the EFS file system
fileSystem.connections.allowDefaultPortFrom(service.taskDefinition.taskRole);
