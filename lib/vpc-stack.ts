import { Stack, StackProps, aws_ec2 } from "aws-cdk-lib";
import { KeyPair } from "cdk-ec2-key-pair";
import { Construct } from "constructs";

export class VpcStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const vpc = new aws_ec2.Vpc(this, "vpc", {
      cidr: "10.0.0.0/24",
      maxAzs: 1,
      natGateways: 0,
      subnetConfiguration: [
        { name: "web", subnetType: aws_ec2.SubnetType.PUBLIC },
        { name: "db", subnetType: aws_ec2.SubnetType.PRIVATE_ISOLATED },
      ],
    });

    const securityGroup = new aws_ec2.SecurityGroup(this, "Security Group", {
      vpc,
      allowAllOutbound: true,
    });
    // Allow SSH access on port tcp/22
    securityGroup.addIngressRule(
      aws_ec2.Peer.anyIpv4(),
      aws_ec2.Port.tcp(22),
      "Allow SSH Access"
    );

    // Allow HTTP access on port tcp/80
    securityGroup.addIngressRule(
      aws_ec2.Peer.anyIpv4(),
      aws_ec2.Port.tcp(80),
      "Allow HTTP Access"
    );

    const key = new KeyPair(this, "ssh key pair", {
      name: "watch-duty-manager",
      storePublicKey: true, // by default the public key will not be stored in Secrets Manager
    });

    const ec2 = new aws_ec2.Instance(this, "web server", {
      instanceType: aws_ec2.InstanceType.of(
        aws_ec2.InstanceClass.T2,
        aws_ec2.InstanceSize.MICRO
      ),
      vpc,
      machineImage: aws_ec2.MachineImage.latestAmazonLinux(),
      vpcSubnets: { subnetType: aws_ec2.SubnetType.PUBLIC },
      securityGroup,
      keyName: key.keyPairName,
    });
  }
}
