import { Stack, StackProps, aws_ec2, aws_rds, aws_ecs } from "aws-cdk-lib";
import { Construct } from "constructs";
import * as keypair from "cdk-ec2-key-pair";

export class VpcStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const vpc = new aws_ec2.Vpc(this, "vpc");

    // const cluster = new aws_ecs.Cluster(this, "Cluster", {
    //   vpc,
    // });

    // // Add capacity to it
    // cluster.addCapacity("DefaultAutoScalingGroupCapacity", {
    //   instanceType: aws_ec2.InstanceType.of(
    //     aws_ec2.InstanceClass.T2,
    //     aws_ec2.InstanceSize.MEDIUM
    //   ),
    //   desiredCapacity: 3,
    // });

    // const taskDefinition = new aws_ecs.Ec2TaskDefinition(this, "TaskDef");

    // taskDefinition.addContainer("DefaultContainer", {
    //   image: aws_ecs.ContainerImage.fromRegistry("amazon/amazon-ecs-sample"),
    //   memoryLimitMiB: 512,
    // });

    // // Instantiate an Amazon ECS Service
    // const ecsService = new aws_ecs.Ec2Service(this, "Service", {
    //   cluster,
    //   taskDefinition,
    // });

    // const rds = new aws_rds.DatabaseInstance(this, "DBInstance", {
    //   engine: aws_rds.DatabaseInstanceEngine.mysql({
    //     version: aws_rds.MysqlEngineVersion.VER_8_0_26,
    //   }),
    //   instanceType: aws_ec2.InstanceType.of(
    //     aws_ec2.InstanceClass.T2,
    //     aws_ec2.InstanceSize.MEDIUM
    //   ),
    //   vpc,
    //   vpcSubnets: { subnetType: aws_ec2.SubnetType.PRIVATE_WITH_NAT },
    // });
  }
}
